import torch
import torch.nn as nn


# ==========================================
# 1. 自定义自动求导函数 (核心数学逻辑)
# ==========================================
class MyLinearFunction(torch.autograd.Function):
    """
    手动实现全连接层的前向和反向传播
    """

    @staticmethod
    def forward(ctx, input, weight, bias=None):
        # input shape: [batch_size, in_features]
        # weight shape: [out_features, in_features]

        # 保存tensor用于backward阶段计算梯度
        ctx.save_for_backward(input, weight, bias)

        # 前向计算: Y = X * W^T + b
        output = input.mm(weight.t())

        if bias is not None:
            # bias shape: [out_features] -> 广播到 [batch_size, out_features]
            output += bias.unsqueeze(0).expand_as(output)

        return output

    @staticmethod
    def backward(ctx, grad_output):
        # grad_output: 上一层传回来的梯度 dL/dY
        # shape: [batch_size, out_features]

        # 获取保存的tensor
        input, weight, bias = ctx.saved_tensors

        grad_input = grad_weight = grad_bias = None

        # 1. 计算对输入的梯度: dL/dX = dL/dY * W
        # shape: [batch_size, in] = [batch, out] * [out, in]
        if ctx.needs_input_grad[0]:
            grad_input = grad_output.mm(weight)

        # 2. 计算对权重的梯度: dL/dW = (dL/dY)^T * X
        # shape: [out, in] = [out, batch] * [batch, in]
        if ctx.needs_input_grad[1]:
            grad_weight = grad_output.t().mm(input)

        # 3. 计算对偏置的梯度: dL/db = sum(dL/dY, dim=0)
        # shape: [out]
        if bias is not None and ctx.needs_input_grad[2]:
            grad_bias = grad_output.sum(0)

        return grad_input, grad_weight, grad_bias


# ==========================================
# 2. 封装为 nn.Module (方便放入模型中)
# ==========================================
class MyLinear(nn.Module):
    def __init__(self, in_features, out_features, bias=True):
        super(MyLinear, self).__init__()
        self.in_features = in_features
        self.out_features = out_features

        # 定义可训练参数 Parameters
        self.weight = nn.Parameter(torch.Tensor(out_features, in_features))
        if bias:
            self.bias = nn.Parameter(torch.Tensor(out_features))
        else:
            self.register_parameter('bias', None)

        self.reset_parameters()

    def reset_parameters(self):
        # 使用 Kaiming 初始化 对应relu
        nn.init.kaiming_uniform_(self.weight, a=5 ** 0.5)
        if self.bias is not None:
            fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.weight)
            bound = 1 / (fan_in ** 0.5)
            nn.init.uniform_(self.bias, -bound, bound)

    def forward(self, input):
        # 调用我们写的自定义Function
        return MyLinearFunction.apply(input, self.weight, self.bias)

    def extra_repr(self):
        return 'in_features={}, out_features={}, bias={}'.format(
            self.in_features, self.out_features, self.bias is not None
        )