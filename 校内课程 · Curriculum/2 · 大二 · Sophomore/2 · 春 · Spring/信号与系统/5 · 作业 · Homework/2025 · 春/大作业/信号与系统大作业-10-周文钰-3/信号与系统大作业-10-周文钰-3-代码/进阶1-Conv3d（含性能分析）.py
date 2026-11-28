import torch
import torch.nn as nn
import timeit
from tabulate import tabulate
import matplotlib
font = {
    'family': 'Microsoft YaHei',
    'weight': 'bold'
}
matplotlib.rc("font", **font)
# ================= 可调参数 =================
BATCH_SIZE = 1                 # 批量大小
IN_CHANNELS = 3                # 输入通道数
OUT_CHANNELS = 6               # 输出通道数
KERNEL_SIZE = 3                # 卷积核大小
STRIDE = 1                     # 步长
PADDING = 1                    # 填充（支持整数或三元组）
DILATION = 1                   # 膨胀系数
INPUT_SIZES = [                # 测试输入尺寸 (D, H, W)
    (16, 16, 16),
    (32, 32, 32),
    (64, 64, 32),
    (128, 64, 64)
]
TEST_ITERATIONS = 10           # 每个测试的迭代次数

# ================= 辅助函数 =================
def _triple(x):
    """将输入转换为三元组"""
    if isinstance(x, tuple):
        if len(x) == 3:
            return x
        raise ValueError("参数需要是三元组")
    return (x, x, x)

# ================= 手动Conv3D实现 =================
# ================= 手动Conv3D实现 =================
def manual_conv3d(input, weight, bias=None, stride=1, padding=0, dilation=1):
    # 参数标准化
    stride = _triple(stride)
    padding = _triple(padding)
    dilation = _triple(dilation)
    
    Batch, channel_in, D_in, H_in, W_in = input.shape
    channel_out, _, kD, kH, kW = weight.shape
    
    # 计算输出尺寸
    D_out = (D_in + 2*padding[0] - dilation[0]*(kD-1)-1)//stride[0] +1
    H_out = (H_in + 2*padding[1] - dilation[1]*(kH-1)-1)//stride[1] +1
    W_out = (W_in + 2*padding[2] - dilation[2]*(kW-1)-1)//stride[2] +1

    # 填充处理
    padded = nn.functional.pad(input, 
        (padding[2], padding[2],   # W方向
         padding[1], padding[1],   # H方向
         padding[0], padding[0])   # D方向
    )
    
    # 三维展开（调整展开顺序）
    unfold_d = padded.unfold(2, kD, stride[0])  # D维度展开
    unfold_d = unfold_d.unfold(3, kH, stride[1]) # H维度展开
    unfold_d = unfold_d.unfold(4, kW, stride[2]) # W维度展开
    
    # 维度重组（B, C, D_out, H_out, W_out, kD, kH, kW）
    unfold_d = unfold_d.permute(0, 1, 2, 3, 4, 6, 7, 5)  # 调整最后三个维度顺序
    
    # 修正爱因斯坦求和公式
    output = torch.einsum('bcdhwijk,ocijk->bodhw',  # 索引匹配8维输入和5维权重
                         unfold_d, 
                         weight.view(channel_out, channel_in, kD, kH, kW))
    
    if bias is not None:
        output += bias.view(1, -1, 1, 1, 1)
    
    return output
# ================= 测试流程 =================
def generate_test_case(input_size):
    """生成测试用例"""
    return (
        torch.randn(BATCH_SIZE, IN_CHANNELS, *input_size),
        nn.Conv3d(IN_CHANNELS, OUT_CHANNELS, KERNEL_SIZE,
                 stride=STRIDE, padding=PADDING, dilation=DILATION)
    )

if __name__ == "__main__":
    results = []
    
    for size in INPUT_SIZES:
        print(f"\n=== 测试尺寸 {size} ===")
        input, conv_layer = generate_test_case(size)
        
        # 预热GPU（如果有）
        if torch.cuda.is_available():
            input = input.cuda()
            conv_layer = conv_layer.cuda()
        
        # 验证正确性
        with torch.no_grad():
            manual_out = manual_conv3d(input, conv_layer.weight, conv_layer.bias,
                                      stride=STRIDE, padding=PADDING, dilation=DILATION)
            torch_out = conv_layer(input)
            
        diff = torch.max(torch.abs(manual_out - torch_out)).item()
        print(f"最大误差: {diff:.2e}", "✓" if diff < 1e-5 else "×")
        
        # 性能测试
        manual_time = timeit.timeit(
            lambda: manual_conv3d(input, conv_layer.weight, conv_layer.bias,
                                 stride=STRIDE, padding=PADDING, dilation=DILATION),
            number=TEST_ITERATIONS
        ) / TEST_ITERATIONS
        
        torch_time = timeit.timeit(
            lambda: conv_layer(input),
            number=TEST_ITERATIONS
        ) / TEST_ITERATIONS
        
        results.append([
            f"{size[0]}×{size[1]}×{size[2]}",
            f"{manual_time:.4f}",
            f"{torch_time:.4f}",
            f"{manual_time/torch_time:.1f}x"
        ])
    
    # 打印结果表格
    print("\n性能对比结果:")
    print(tabulate(results, 
                 headers=["输入尺寸", "手动实现(s)", "PyTorch(s)", "耗时倍数"],
                 tablefmt="grid"))
    
    # 绘制性能曲线
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    
    sizes = [f"{s[0]}×{s[1]}×{s[2]}" for s in INPUT_SIZES]
    manual = [float(r[1]) for r in results]
    torch_t = [float(r[2]) for r in results]
    
    plt.plot(sizes, manual, 'o-', label='手动实现')
    plt.plot(sizes, torch_t, 's-', label='PyTorch')
    plt.yscale('log')
    plt.ylabel('单次运算时间 (秒, 对数尺度)')
    plt.xlabel('输入尺寸 (D×H×W)')
    plt.title('Conv3D 不同输入尺寸性能对比')
    plt.legend()
    plt.grid(True, which='both', linestyle='--')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()