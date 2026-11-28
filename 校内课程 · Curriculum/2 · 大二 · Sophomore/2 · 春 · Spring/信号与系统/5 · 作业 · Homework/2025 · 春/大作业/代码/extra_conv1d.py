import torch
import numpy as np
import matplotlib.pyplot as plt
import timeit
from tabulate import tabulate  # 新增表格库
import matplotlib
font = {
    'family': 'Microsoft YaHei',
    'weight': 'bold'
}
matplotlib.rc("font", **font)
# ================= 可调参数 =================
BATCH_SIZE = 2                 # 批量大小
IN_CHANNELS = 3                # 输入通道数
OUT_CHANNELS = 5               # 输出通道数
SIGNAL_LENGTHS = [100, 500, 1000, 2000, 5000]  # 不同信号长度
KERNEL_SIZE = 7                # 卷积核大小
STRIDE = 2                     # 步长
PADDING = 3                    # 填充
TEST_CASE_VERBOSE = 0          # 关闭可视化

# ================= 手动Conv1D实现 =================
def manual_conv1d(inputs, weight, stride=1, padding=0):
    """手动实现1D卷积"""
    L_in = inputs.shape
    k = weight.shape
    
    # 计算输出长度
    L_out = (L_in + 2*padding - k) // stride + 1
    
    # 处理padding
    if isinstance(padding, int):
        pad = (padding, padding)
    else:
        pad = padding
    padded = torch.nn.functional.pad(inputs, pad)
    
    # 展开输入张量 [B, in_C, L_out, k]
    unfolded = padded.unfold(-1, k, stride)
    
    # 矩阵乘法计算卷积结果
    output = torch.einsum('bclk,ock->bol', unfolded, weight)
    
    return output

# ================= 性能测试案例生成器 =================
def generate_perf_test_case(signal_length):
    """生成指定长度的性能测试案例"""
    inputs = torch.randn(BATCH_SIZE, IN_CHANNELS, signal_length)
    weight = torch.randn(OUT_CHANNELS, IN_CHANNELS, KERNEL_SIZE)
    return inputs, weight

# ================= 主测试流程 =================
if __name__ == "__main__":
    performance_data = []
    
    for signal_length in SIGNAL_LENGTHS:
        print(f"\n{'='*40}")
        print(f"Testing Signal Length: {signal_length}")
        print(f"{'='*40}")
        
        # 生成测试数据
        inputs, weight = generate_perf_test_case(signal_length)
        
        # 验证正确性（修复参数顺序）
        manual_out = manual_conv1d(inputs, weight, STRIDE, PADDING)
        official_out = torch.nn.functional.conv1d(
            inputs, weight, 
            stride=STRIDE,  # 显式使用关键字参数
            padding=PADDING
        )
        
        # 计算误差
        mse = torch.mean((manual_out - official_out)**2).item()
        max_err = torch.max(torch.abs(manual_out - official_out)).item()
        print(f"验证结果 | MSE: {mse:.2e}, MaxErr: {max_err:.2e}")
        
        # 性能测试（保持与验证一致的参数）
        manual_time = timeit.timeit(
            lambda: manual_conv1d(inputs, weight, STRIDE, PADDING),
            number=100
        ) / 100
        
        official_time = timeit.timeit(
            lambda: torch.nn.functional.conv1d(
                inputs, weight, 
                stride=STRIDE, 
                padding=PADDING
            ),
            number=100
        ) / 100
        
        # 记录数据
        performance_data.append([
            signal_length,
            f"{manual_time:.4f}",
            f"{official_time:.4f}",
            f"{manual_time/official_time:.1f}x"
        ])
        
    # 打印表格结果
    headers = ["信号长度", "手动实现(s)", "官方实现(s)", "耗时倍数"]
    print("\n性能数据汇总:")
    print(tabulate(performance_data, headers=headers, tablefmt="grid"))
    
    # 绘制性能对比图
    plt.figure(figsize=(10, 6))
    lengths = [x[0] for x in performance_data]
    manual_times = [float(x[1]) for x in performance_data]
    official_times = [float(x[2]) for x in performance_data]
    
    plt.plot(lengths, manual_times, 'o-', label='手动实现')
    plt.plot(lengths, official_times, 's-', label='官方实现')
    
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('信号长度 (对数尺度)')
    plt.ylabel('单次运算平均耗时 (秒, 对数尺度)')
    plt.title('不同输入尺寸下的Conv1D性能对比')
    plt.legend()
    plt.grid(True, which='both', linestyle='--')
    plt.tight_layout()
    plt.show()