import torch
import torch.nn as nn

# ==========================================
# 1. 自定义 BatchNorm 核心逻辑 (复用以支持 2D)
# ==========================================
class MyBatchNormFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input, gamma, beta, running_mean, running_var, eps=1e-5, momentum=0.1, training=True):
        # input shape: [N, C] (N可以是 BatchSize*H*W)
        ctx.eps = eps
        N = input.shape[0]

        if training:
            mean = input.mean(dim=0)
            var = input.var(dim=0, unbiased=False)
            std = torch.sqrt(var + eps)
            x_hat = (input - mean) / std

            with torch.no_grad():
                running_mean.mul_(1 - momentum).add_(mean * momentum)
                running_var.mul_(1 - momentum).add_(var * momentum)
        else:
            mean = running_mean
            var = running_var
            std = torch.sqrt(var + eps)
            x_hat = (input - mean) / std

        output = gamma * x_hat + beta
        ctx.save_for_backward(input, x_hat, mean, std, gamma)
        return output

    @staticmethod
    def backward(ctx, grad_output):
        input, x_hat, mean, std, gamma = ctx.saved_tensors
        N = input.shape[0]

        grad_gamma = (grad_output * x_hat).sum(dim=0)
        grad_beta = grad_output.sum(dim=0)
        grad_x_hat = grad_output * gamma

        term1 = N * grad_x_hat
        term2 = grad_x_hat.sum(dim=0)
        term3 = x_hat * (grad_x_hat * x_hat).sum(dim=0)
        grad_input = (term1 - term2 - term3) / (N * std)

        return grad_input, grad_gamma, grad_beta, None, None, None, None, None


# ==========================================
# 2. 封装模块: MyBatchNorm2d (CNN 专用)
# ==========================================
class MyBatchNorm2d(nn.Module):
    def __init__(self, num_features, eps=1e-5, momentum=0.1):
        super(MyBatchNorm2d, self).__init__()
        self.eps = eps
        self.momentum = momentum
        self.gamma = nn.Parameter(torch.ones(num_features))
        self.beta = nn.Parameter(torch.zeros(num_features))
        self.register_buffer('running_mean', torch.zeros(num_features))
        self.register_buffer('running_var', torch.ones(num_features))

    def forward(self, input):
        # input: [Batch, Channel, Height, Width]
        # 变换为 [B*H*W, C] 以复用 1D BN 逻辑
        N, C, H, W = input.shape
        # Permute: [B, C, H, W] -> [B, H, W, C] -> Flatten -> [N*H*W, C]
        input_reshaped = input.permute(0, 2, 3, 1).contiguous().view(-1, C)

        # 调用核心 Function
        out_reshaped = MyBatchNormFunction.apply(
            input_reshaped, self.gamma, self.beta,
            self.running_mean, self.running_var,
            self.eps, self.momentum, self.training
        )

        # 还原形状: [N*H*W, C] -> [B, H, W, C] -> [B, C, H, W]
        output = out_reshaped.view(N, H, W, C).permute(0, 3, 1, 2)
        return output


# ==========================================
# 3. 自定义线性层 (用于 CNN 的分类头)
# ==========================================
# 即使是 CNN，最后通常也需要全连接层进行分类，因此这里包含 Linear
class MyLinearFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input, weight, bias=None):
        ctx.save_for_backward(input, weight, bias)
        output = input.mm(weight.t())
        if bias is not None:
            output += bias.unsqueeze(0).expand_as(output)
        return output

    @staticmethod
    def backward(ctx, grad_output):
        input, weight, bias = ctx.saved_tensors
        grad_input = grad_weight = grad_bias = None

        if ctx.needs_input_grad[0]:
            grad_input = grad_output.mm(weight)
        if ctx.needs_input_grad[1]:
            grad_weight = grad_output.t().mm(input)
        if bias is not None and ctx.needs_input_grad[2]:
            grad_bias = grad_output.sum(0)

        return grad_input, grad_weight, grad_bias


class MyLinear(nn.Module):
    def __init__(self, in_features, out_features, bias=True):
        super(MyLinear, self).__init__()
        self.weight = nn.Parameter(torch.Tensor(out_features, in_features))
        if bias:
            self.bias = nn.Parameter(torch.Tensor(out_features))
        else:
            self.register_parameter('bias', None)
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.kaiming_uniform_(self.weight, a=5 ** 0.5)
        if self.bias is not None:
            fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.weight)
            bound = 1 / (fan_in ** 0.5)
            nn.init.uniform_(self.bias, -bound, bound)

    def forward(self, input):
        return MyLinearFunction.apply(input, self.weight, self.bias)