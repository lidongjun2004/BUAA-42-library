import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import math
import matplotlib

font = {'family': 'Microsoft YaHei', 'weight': 'bold'}
matplotlib.rc("font", **font)

# ================= 新卷积核配置 =================
img_location = "images\lenna.bmp"
padding = 2  # 修改padding以适应5x5核
stride = 1

# ================= 新卷积核定义 =================
# 拉普拉斯边缘检测核（精细边缘）
laplacian_kernel = np.array([
    [ 0,  1, 0],
    [ 1, -4, 1],
    [ 0,  1, 0]
], dtype=np.float32)

# 浮雕效果核
emboss_kernel = np.array([
    [-2, -1, 0],
    [-1,  1, 1],
    [ 0,  1, 2]
], dtype=np.float32)

# 高斯模糊核（5x5）
gaussian_blur_kernel = np.array([
    [1,  4,  6,  4, 1],
    [4, 16, 24, 16, 4],
    [6, 24, 36, 24, 6],
    [4, 16, 24, 16, 4],
    [1,  4,  6,  4, 1]
], dtype=np.float32) / 256.0

# 角点检测核
corner_kernel = np.array([
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1]
], dtype=np.float32)

# ================= 修改后的函数定义 =================
def conv2d_multi_channel_rgb(input_img, kernel, padding, stride):
    C, H, W = input_img.shape
    kC, kH, kW = kernel.shape
    assert C == kC, "通道数不匹配"

    # 自动计算所需padding
    pad = (kW - 1) // 2
    input_padded = np.pad(input_img, 
                        ((0, 0), (pad, pad), (pad, pad)),
                        mode='constant')

    out_H = (input_padded.shape[1] - kH) // stride + 1
    out_W = (input_padded.shape[2] - kW) // stride + 1
    output = np.zeros((C, out_H, out_W))

    for c in range(C):
        for i in range(out_H):
            for j in range(out_W):
                region = input_padded[c, i*stride:i*stride+kH, j*stride:j*stride+kW]
                output[c, i, j] = np.sum(region * kernel[c])
    return output
def read_image_pixels(image_path):
    try:
        img = Image.open(image_path).convert('RGBA')
        width, height = img.size
        data = np.array(img.getdata(), dtype=np.float64) / 255.0
        return data.reshape((height, width, 4)), height, width, 'rgba'
    except Exception as e:
        print(f"读取图像失败: {str(e)}")
        return None, None, None, None

def load_rgb_image_from_pixels(pixels):
    return pixels[:, :, :3].transpose((2, 0, 1))  # (C, H, W)
def display_color_results(results, titles, rows, cols, figsize=(15, 10)):
    plt.figure(figsize=figsize)
    for i, (result, title) in enumerate(zip(results, titles)):
        plt.subplot(rows, cols, i+1)
        if result.ndim == 2:
            plt.imshow(result, cmap='gray')
        else:
            # 确保形状为 (H, W, C)
            plt.imshow(np.clip(result, 0, 1))  # 添加clip防止溢出
        plt.title(title)
        plt.axis('off')
    plt.tight_layout()
    plt.show()

# ================= 修改后的主程序 =================
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, img_location)
    
    # 图像加载与预处理
    pixels, h, w, _ = read_image_pixels(image_path)
    img_rgb = load_rgb_image_from_pixels(pixels)
    original_rgb = pixels[:, :, :3]

    # ================= 新特征计算 =================
    # 高斯模糊处理
    gaussian_blur_multi = np.stack([gaussian_blur_kernel]*3, axis=0)
    gaussian_blur_result = conv2d_multi_channel_rgb(img_rgb, gaussian_blur_multi, padding, stride)

    # 浮雕效果处理
    emboss_multi = np.stack([emboss_kernel]*3, axis=0)
    emboss_result = conv2d_multi_channel_rgb(img_rgb, emboss_multi, padding, stride)

    # 角点检测
    corner_multi = np.stack([corner_kernel]*3, axis=0)
    corner_result = np.sum(conv2d_multi_channel_rgb(img_rgb, corner_multi, padding, stride), axis=0)

    # 拉普拉斯边缘检测
    laplacian_multi = np.stack([laplacian_kernel]*3, axis=0)
    laplacian_result = np.sum(conv2d_multi_channel_rgb(img_rgb, laplacian_multi, padding, stride), axis=0)

    # ================= 新结果展示 =================
    # 彩色处理结果
    color_results = [
        original_rgb,
        gaussian_blur_result.transpose(1, 2, 0),
        emboss_result.transpose(1, 2, 0)
    ]
    color_titles = ['原始图像', '高斯模糊', '浮雕效果']
    display_color_results(color_results, color_titles, 1, 3, figsize=(15, 5))

    # 特征检测结果
    feature_results = [
        laplacian_result,
        corner_result,
    ]
    feature_titles = ['拉普拉斯边缘', '角点检测']
    display_color_results(feature_results, feature_titles, 1, 2, figsize=(12, 6))

    # 运行后会自动弹出所有结果窗口