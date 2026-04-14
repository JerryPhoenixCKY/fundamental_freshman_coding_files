from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import ctypes
import os
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image


WINDOW_TARGET_WIDTH = 1480
WINDOW_TARGET_HEIGHT = 860
WINDOW_MIN_WIDTH = 1080
WINDOW_MIN_HEIGHT = 640
UI_SCALE = 1.5
TITLE_FONT = ("Microsoft YaHei UI", 18, "bold")
TEXT_FONT = ("Microsoft YaHei UI", 14)
BUTTON_FONT = ("Microsoft YaHei UI", 13)
OUTPUT_DIR_NAME = "jpg_converted"


def enable_high_dpi_support():
    """Enable DPI awareness on Windows to keep UI sharp on high-resolution displays."""
    if os.name != "nt":
        return

    try:
        # Prefer Per-Monitor V2 DPI awareness for sharper rendering.
        ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
    except Exception:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass


def convert_single_webp(file_path: str):
    """Convert a single WebP image to JPG."""
    source_path = Path(file_path)
    target_dir = source_path.parent / OUTPUT_DIR_NAME
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{source_path.stem}.jpg"

    try:
        with Image.open(source_path) as img:
            img.convert("RGB").save(target_path, "JPEG", quality=95)
        return True, f"{source_path.name} -> {target_path}"
    except Exception as exc:
        return False, f"{source_path.name}: {exc}"


def select_files_window(root):
    """Show a taller selection window and return selected files."""
    selected_files = []
    selected_set = set()

    picker = tk.Toplevel(root)
    picker.title("WebP 批量转 JPG")

    screen_width = picker.winfo_screenwidth()
    screen_height = picker.winfo_screenheight()
    width = min(WINDOW_TARGET_WIDTH, max(900, screen_width - 260))
    height = min(WINDOW_TARGET_HEIGHT, max(560, screen_height - 260))
    x_offset = max((screen_width - width) // 2, 0)
    y_offset = max((screen_height - height) // 2, 0)

    picker.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
    picker.minsize(min(WINDOW_MIN_WIDTH, width), min(WINDOW_MIN_HEIGHT, height))
    picker.resizable(True, True)

    title_label = tk.Label(
        picker,
        text="请选择一个或多个 WebP 图片",
        font=TITLE_FONT,
    )
    title_label.pack(pady=(20, 10))

    tips_label = tk.Label(
        picker,
        text="提示：可多次点击“选择文件”，从不同文件夹持续追加图片。",
        font=TEXT_FONT,
    )
    tips_label.pack(pady=(0, 10))

    info_text = tk.StringVar(value="尚未选择文件")
    info_label = tk.Label(
        picker,
        textvariable=info_text,
        justify="left",
        wraplength=max(560, width - 60),
        font=TEXT_FONT,
    )
    info_label.pack(padx=20, pady=(0, 16), fill="x")

    def on_resize(event):
        info_label.configure(wraplength=max(560, event.width - 60))

    picker.bind("<Configure>", on_resize)

    start_button = None

    def refresh_info():
        source_folders = sorted({str(Path(path).parent) for path in selected_files})

        if not selected_files:
            info_text.set("尚未选择文件")
            if start_button is not None:
                start_button.configure(state="disabled")
            return

        preview_names = [
            f"{Path(path).parent.name} / {Path(path).name}"
            for path in selected_files[:8]
        ]
        preview_text = "\n".join(preview_names)
        remaining = len(selected_files) - len(preview_names)

        if remaining > 0:
            preview_text += f"\n... 以及另外 {remaining} 个文件"

        info_text.set(
            f"已选择 {len(selected_files)} 个文件，来自 {len(source_folders)} 个文件夹：\n"
            f"{preview_text}"
        )

        if start_button is not None:
            start_button.configure(state="normal")

    def choose_files():
        nonlocal selected_files
        files = filedialog.askopenfilenames(
            parent=picker,
            title="选择 WebP 图片（可多选）",
            filetypes=[("WebP files", "*.webp"), ("All files", "*.*")],
        )

        if not files:
            return

        for path in files:
            if path not in selected_set:
                selected_set.add(path)
                selected_files.append(path)

        refresh_info()

    def clear_files():
        nonlocal selected_files, selected_set
        selected_files = []
        selected_set = set()
        refresh_info()

    def close_window():
        picker.destroy()

    button_frame = tk.Frame(picker)
    button_frame.pack(pady=6)

    choose_button = tk.Button(
        button_frame,
        text="选择文件",
        width=14,
        command=choose_files,
        font=BUTTON_FONT,
    )
    choose_button.grid(row=0, column=0, padx=8)

    clear_button = tk.Button(
        button_frame,
        text="清空选择",
        width=14,
        command=clear_files,
        font=BUTTON_FONT,
    )
    clear_button.grid(row=0, column=1, padx=8)

    start_button = tk.Button(
        button_frame,
        text="开始转换",
        width=14,
        command=close_window,
        font=BUTTON_FONT,
        state="disabled",
    )
    start_button.grid(row=0, column=2, padx=8)

    refresh_info()

    picker.protocol("WM_DELETE_WINDOW", close_window)
    picker.grab_set()
    picker.focus_force()
    root.wait_window(picker)
    return selected_files


def convert_webp_to_jpg():
    """Convert one or multiple WebP images to JPG format."""
    enable_high_dpi_support()
    root = tk.Tk()
    root.withdraw()

    try:
        # Increase UI scaling to improve readability on high-DPI displays.
        root.tk.call("tk", "scaling", UI_SCALE)

        file_paths = select_files_window(root)

        if not file_paths:
            print("No file selected")
            return

        total = len(file_paths)
        success_count = 0
        failed_messages = []

        max_workers = min(8, max(1, os.cpu_count() or 1))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(convert_single_webp, path) for path in file_paths]
            for index, future in enumerate(as_completed(futures), start=1):
                ok, message = future.result()
                status = "Success" if ok else "Failed"
                print(f"[{index}/{total}] {status}: {message}")
                if ok:
                    success_count += 1
                else:
                    failed_messages.append(message)

        failed_count = len(failed_messages)
        summary = f"Completed: {total}, Success: {success_count}, Failed: {failed_count}"

        output_dirs = sorted({str(Path(path).parent / OUTPUT_DIR_NAME) for path in file_paths})
        summary += f"\nOutput folders: {len(output_dirs)}"
        if output_dirs:
            summary += "\n" + "\n".join(output_dirs[:8])
            if len(output_dirs) > 8:
                summary += f"\n... and {len(output_dirs) - 8} more"

        if failed_messages:
            summary += "\nFailed files:\n" + "\n".join(failed_messages[:8])

        print(summary)
        messagebox.showinfo("Conversion Result", summary, parent=root)

    finally:
        root.destroy()

if __name__ == "__main__":
    convert_webp_to_jpg()