import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import math
import matplotlib
from numpy.lib.stride_tricks import sliding_window_view

font = {
    'family': 'Microsoft YaHei',
    'weight': 'bold'
}
matplotlib.rc("font", **font)
# ================= 配置参数 =================
img_location = "images\lenna.bmp"  # 图片位置
padding = 1
stride = 1

# ================= 卷积核定义 =================
# 边缘检测核
sobel_x = np.array([[1, 0, -1], 
                   [2, 0, -2], 
                   [1, 0, -1]], dtype=np.float32)

sobel_y = np.array([[1, 2, 1],
                   [0, 0, 0],
                   [-1, -2, -1]], dtype=np.float32)

# 模糊核（3x3均值滤波）
blur_kernel = np.ones((3, 3)) / 9.0

# 锐化核
sharpen_kernel = np.array([[0, -1, 0],
                          [-1, 5, -1],
                          [0, -1, 0]])

# Gabor参数配置
gabor_params = {
    'ksize': 5,
    'sigma': 2.0,
    'lambd': 5.0,
    'gamma': 0.5,
    'angles': [0, math.pi/4, math.pi/2, 3*math.pi/4]
}

# ================= 函数定义 =================
def generate_gabor_kernel(ksize=5, sigma=1.0, theta=0, lambd=10.0, gamma=0.5):
    kernel = np.zeros((ksize, ksize))
    center = ksize // 2
    
    for x in range(ksize):
        for y in range(ksize):
            x_hat = x - center
            y_hat = y - center
            x_theta = x_hat * math.cos(theta) + y_hat * math.sin(theta)
            y_theta = -x_hat * math.sin(theta) + y_hat * math.cos(theta)
            gaussian = math.exp(-(x_theta**2 + gamma**2 * y_theta**2)/(2*sigma**2))
            cosine = math.cos(2 * math.pi * x_theta / lambd)
            kernel[x, y] = gaussian * cosine
    kernel = kernel - np.mean(kernel)
    return kernel / np.abs(kernel).sum()

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

def conv2d_multi_channel_rgb(input_img, kernel, padding, stride):
    C, H, W = input_img.shape
    kC, kH, kW = kernel.shape
    assert C == kC, "通道数不匹配"

    if padding > 0:
        input_padded = np.pad(input_img, 
                            ((0, 0), (padding, padding), (padding, padding)),
                            mode='constant')
    else:
        input_padded = input_img

    out_H = (input_padded.shape[1] - kH) // stride + 1
    out_W = (input_padded.shape[2] - kW) // stride + 1
    output = np.zeros((C, out_H, out_W))  # (C, H, W)

    for c in range(C):
        for i in range(out_H):
            for j in range(out_W):
                region = input_padded[c, i*stride:i*stride+kH, j*stride:j*stride+kW]
                output[c, i, j] = np.sum(region * kernel[c])
    return output

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

# ================= 主程序 =================
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, img_location)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图像路径 {image_path} 不存在！")
    
    pixels, h, w, _ = read_image_pixels(image_path)
    if pixels is None:
        exit()
    
    # 预处理
    img_rgb = load_rgb_image_from_pixels(pixels)  # (C, H, W) = (3, H, W)
    original_rgb = pixels[:, :, :3]               # (H, W, C) = (H, W, 3)

    # ================= 特征计算 =================
    # RGB通道分离（单通道灰度）
    rgb_channels = [original_rgb[:, :, i] for i in range(3)]
    
    # 模糊处理（彩色）
    blur_kernel_multi = np.stack([blur_kernel]*3, axis=0)
    blur_result = conv2d_multi_channel_rgb(img_rgb, blur_kernel_multi, padding, stride)
    
    # 锐化处理（彩色）
    sharpen_kernel_multi = np.stack([sharpen_kernel]*3, axis=0)
    sharpen_result = conv2d_multi_channel_rgb(img_rgb, sharpen_kernel_multi, padding, stride)
    
    # 边缘检测
    edge_x = np.sum(conv2d_multi_channel_rgb(img_rgb, np.stack([sobel_x]*3, axis=0), padding, stride), axis=0)
    edge_y = np.sum(conv2d_multi_channel_rgb(img_rgb, np.stack([sobel_y]*3, axis=0), padding, stride), axis=0)
    edge_combined = np.sqrt(edge_x**2 + edge_y**2)
    
    # 纹理检测
    texture_maps = []
    for theta in gabor_params['angles']:
        kernel = generate_gabor_kernel(
            gabor_params['ksize'],
            gabor_params['sigma'],
            theta,
            gabor_params['lambd'],
            gabor_params['gamma']
        )
        texture_map = np.sum(conv2d_multi_channel_rgb(
            img_rgb,
            np.stack([kernel]*3, axis=0),
            padding,
            stride
        ), axis=0)
        texture_maps.append(texture_map)
    texture_combined = np.mean(texture_maps, axis=0)

    # ================= 结果展示 =================
    # 彩色处理结果（正确形状转换）
    color_results = [
        original_rgb,  # 原始形状 (H, W, 3)
        blur_result.transpose(1, 2, 0),  # (H, W, 3)
        sharpen_result.transpose(1, 2, 0)
    ]
    color_titles = ['原始图像', '模糊处理', '锐化处理']
    display_color_results(color_results, color_titles, 1, 3, figsize=(15, 5))

    mono_results = [edge_combined, texture_combined]
    mono_titles = ['边缘特征', '纹理特征']
    display_color_results(mono_results, mono_titles, 1, 2, figsize=(12, 6))

    # RGB通道分离展示
    channel_results = [
        original_rgb[:, :, 0],
        original_rgb[:, :, 1],
        original_rgb[:, :, 2]
    ]
    display_color_results(channel_results, ['红色通道', '绿色通道', '蓝色通道'], 1, 3, figsize=(15, 5))