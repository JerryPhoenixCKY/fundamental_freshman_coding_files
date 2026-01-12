import cv2
import os

# 设置参数
input_folder = r"C:\tmp"
output_video = r"C:\tmp\output.mp4"
fps = 24  # 每秒24帧

# 获取所有 PNG 文件，并按文件名排序（确保顺序正确）
images = [img for img in os.listdir(input_folder) if img.lower().endswith('.png')]
images.sort()  # 按文件名排序，避免乱序

if not images:
    raise ValueError("指定目录中没有找到 PNG 图片！")

# 读取第一张图片以获取尺寸
first_image_path = os.path.join(input_folder, images[0])
frame = cv2.imread(first_image_path)
if frame is None:
    raise IOError(f"无法读取图像: {first_image_path}")
height, width, layers = frame.shape
size = (width, height)

# 创建 VideoWriter 对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用 mp4v 编码器
videowrite = cv2.VideoWriter(output_video, fourcc, fps, size)

# 逐个写入图片
for image_name in images:
    img_path = os.path.join(input_folder, image_name)
    img = cv2.imread(img_path)
    if img is None:
        print(f"警告：跳过无效图像 {img_path}")
        continue
    # 确保图像尺寸与首帧一致（可选：可添加 resize）
    if img.shape[1] != size[0] or img.shape[0] != size[1]:
        print(f"警告：图像尺寸不匹配，跳过 {img_path}")
        continue
    videowrite.write(img)

# 释放资源
videowrite.release()
print(f'✅ 视频已成功保存至: {output_video}')