# -*- coding: utf-8 -*-
"""
批量裁切小红书图片底部水印（支持交互式选择文件）
使用方法:
  python 裁切图片.py --input "输入文件夹或文件" --output "输出文件夹"
  或使用交互模式运行后弹出选择对话框：
  python 裁切图片.py --interactive
可选参数:
  --crop N    固定裁切 N 像素（优先）
  --max-scan N 最大检测像素高度（默认400）
  --threshold T 检测阈值（默认8.0）
  --preview   仅打印检测到的裁切高度，不保存
  --interactive 交互式选择图片和输出目录（优先）

依赖: Pillow, numpy
如果缺失请运行: pip install pillow numpy
"""

import os
import sys
import argparse

try:
    from PIL import Image
except Exception:
    print('Missing dependency: Pillow. Run: pip install pillow')
    sys.exit(1)

try:
    import numpy as np
except Exception:
    print('Missing dependency: numpy. Run: pip install numpy')
    sys.exit(1)

# tkinter 是标准库，但在无GUI环境下可能不可用
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    TK_AVAILABLE = True
except Exception:
    TK_AVAILABLE = False


def detect_crop_height(img, max_scan=400, threshold=8.0):
    """从图片底部向上扫描，基于行均值变化检测水印高度。返回要裁切的像素高度（>=0）。"""
    gray = np.array(img.convert('L'))
    h, w = gray.shape
    max_scan = min(int(max_scan), h // 2)
    row_means = gray.mean(axis=1)
    # 平滑减少噪声
    window = 3
    if len(row_means) >= window:
        kernel = np.ones(window) / window
        smoothed = np.convolve(row_means, kernel, mode='same')
    else:
        smoothed = row_means

    bottom_idx = h - 1
    # 从底部向上查找第一个显著变化的行
    for offset in range(1, max_scan):
        i = bottom_idx - offset
        if i <= 0:
            break
        diff = abs(float(smoothed[i]) - float(smoothed[i - 1]))
        if diff > threshold:
            return offset

    # 备用策略：基于行标准差（寻找低方差区域边界）
    stds = gray.std(axis=1)
    for offset in range(1, max_scan):
        i = bottom_idx - offset
        if i <= 0:
            break
        if stds[i] < 10 and stds[i - 1] >= 10:
            return offset

    # 默认回退值
    return min(150, max(0, h // 10))


def crop_image(path, out_path, auto=True, crop_pixels=None, max_scan=400, threshold=8.0):
    img = Image.open(path).convert('RGB')
    w, h = img.size
    if auto:
        crop_pixels = detect_crop_height(img, max_scan=max_scan, threshold=threshold)
    else:
        if crop_pixels is None:
            raise ValueError('crop_pixels required when auto is False')

    new_h = max(0, h - int(crop_pixels))
    cropped = img.crop((0, 0, w, new_h))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    # 保存时保持原格式
    try:
        cropped.save(out_path, quality=95)
    except Exception:
        cropped.convert('RGB').save(out_path)


def is_image_file(fn):
    ext = fn.lower().split('.')[-1]
    return ext in ('jpg', 'jpeg', 'png', 'webp', 'bmp', 'gif')


def choose_files_and_output():
    if not TK_AVAILABLE:
        print('tkinter unavailable: cannot open file dialog. Run with --input and --output instead.')
        sys.exit(1)
    root = tk.Tk()
    root.withdraw()
    files = filedialog.askopenfilenames(title='选择图片文件（可多选）',
                                        filetypes=[('Images', '*.jpg *.jpeg *.png *.webp *.bmp *.gif')])
    if not files:
        return None, None
    outdir = filedialog.askdirectory(title='选择输出文件夹')
    root.destroy()
    if not outdir:
        return files, None
    return files, outdir


def process_file_list(file_list, out_dir, args):
    if out_dir is None:
        print('未指定输出文件夹，跳过保存。')
    for f in file_list:
        if not is_image_file(f):
            print('跳过非图片文件:', f)
            continue
        basename = os.path.basename(f)
        outpath = os.path.join(out_dir, basename) if out_dir else None
        try:
            if args.crop is not None:
                crop_pixels = args.crop
                auto = False
            else:
                crop_pixels = None
                auto = True

            if args.preview:
                img = Image.open(f)
                cp = detect_crop_height(img, max_scan=args.max_scan, threshold=args.threshold)
                print(f'{f} -> detect crop {cp}px')
            else:
                if outpath is None:
                    print('未给定输出路径，跳过保存:', f)
                    continue
                crop_image(f, outpath, auto=auto, crop_pixels=crop_pixels, max_scan=args.max_scan, threshold=args.threshold)
                print('Saved', outpath)
        except Exception as e:
            print('Error processing', f, e)


def process_input_path(inp, outp, args):
    # 支持文件、文件夹
    if os.path.isfile(inp):
        files = [inp]
        out_dir = outp if outp else os.path.dirname(inp)
        process_file_list(files, out_dir, args)
        return
    if os.path.isdir(inp):
        if not outp:
            print('输出目录未指定:', outp)
            return
        os.makedirs(outp, exist_ok=True)
        for root, dirs, files in os.walk(inp):
            rel = os.path.relpath(root, inp)
            for f in files:
                if not is_image_file(f):
                    continue
                inpath = os.path.join(root, f)
                outdir = os.path.join(outp, rel) if rel != '.' else outp
                outpath = os.path.join(outdir, f)
                try:
                    if args.crop is not None:
                        crop_pixels = args.crop
                        auto = False
                    else:
                        crop_pixels = None
                        auto = True

                    if args.preview:
                        img = Image.open(inpath)
                        cp = detect_crop_height(img, max_scan=args.max_scan, threshold=args.threshold)
                        print(f'{inpath} -> detect crop {cp}px')
                    else:
                        crop_image(inpath, outpath, auto=auto, crop_pixels=crop_pixels, max_scan=args.max_scan, threshold=args.threshold)
                        print('Saved', outpath)
                except Exception as e:
                    print('Error processing', inpath, e)
    else:
        print('输入路径无效:', inp)


def main():
    parser = argparse.ArgumentParser(description='批量裁切小红书图片底部水印')
    parser.add_argument('--input', '-i', required=False, help='输入文件夹或文件（可选）')
    parser.add_argument('--output', '-o', required=False, help='输出文件夹（可选）')
    parser.add_argument('--crop', '-c', type=int, default=None, help='固定裁切像素高度(优先于自动检测)')
    parser.add_argument('--max-scan', '-m', type=int, default=400, help='最大检测像素高度')
    parser.add_argument('--threshold', '-t', type=float, default=8.0, help='检测阈值')
    parser.add_argument('--preview', action='store_true', help='仅打印检测到的裁切高度，不保存')
    parser.add_argument('--interactive', action='store_true', help='交互式选择文件和输出目录（优先）')
    args = parser.parse_args()

    # 交互式逻辑：如果要求交互或未提供输入，则弹出文件选择
    if args.interactive or not args.input:
        files, outdir = choose_files_and_output()
        if not files:
            print('未选择任何文件，退出')
            return
        # 如果用户在对话框未选择输出目录但命令行指定了输出，则使用命令行输出
        final_out = outdir if outdir else args.output
        if final_out is None:
            # 如果未指定输出则保存到当前工作目录下的 out_images
            final_out = os.path.join(os.getcwd(), 'out_images')
            os.makedirs(final_out, exist_ok=True)
        process_file_list(files, final_out, args)
        return

    # 非交互式：需要 input 指定
    inp = args.input
    outp = args.output
    if not inp:
        print('请指定 --input 或使用 --interactive')
        return
    if not os.path.exists(inp):
        print('输入路径不存在:', inp)
        return
    if outp:
        os.makedirs(outp, exist_ok=True)

    process_input_path(inp, outp, args)


if __name__ == '__main__':
    main()
