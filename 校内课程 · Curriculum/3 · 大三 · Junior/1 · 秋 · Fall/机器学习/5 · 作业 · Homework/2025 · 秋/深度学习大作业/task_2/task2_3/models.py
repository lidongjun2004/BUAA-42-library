import torch
import torch.nn as nn

# 1. 从 modules2 (MLP专用) 导入
from task_2.task2_3.modules2_3_MLP import MyLinear, MyBatchNorm1d

# 2. 从 modules3 (CNN专用) 导入 (保留兼容性)
from task_2.task2_3.modules2_3_CNN import MyBatchNorm2d


# ==========================================
# 1. 定义 ResNet 风格的 MLP Block (Zero Gamma 优化版)
# ==========================================
class ResMLPBlock(nn.Module):
    def __init__(self, hidden_dim):
        super(ResMLPBlock, self).__init__()

        self.linear1 = MyLinear(hidden_dim, hidden_dim)
        self.bn1 = MyBatchNorm1d(hidden_dim)
        self.relu = nn.ReLU()
        self.linear2 = MyLinear(hidden_dim, hidden_dim)
        self.bn2 = MyBatchNorm1d(hidden_dim)  # 最后一个BN

        # 【关键优化】Zero Gamma Initialization
        # 将残差块中最后一个 BN 的 gamma 初始化为 0
        # 这样初始状态下，out = x + 0，梯度可以无损穿透 30 层
        nn.init.constant_(self.bn2.gamma, 0)

    def forward(self, x):
        residual = x

        out = self.linear1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.linear2(out)
        out = self.bn2(out)

        out += residual
        out = self.relu(out)
        return out


# ==========================================
# 2. 30层以上的 MLP (ResNet 架构)
# ==========================================
class DeepMLP(nn.Module):
    def __init__(self, input_dim=3072, output_dim=10, hidden_dim=512, num_layers=32):
        super(DeepMLP, self).__init__()

        # 1. 输入层
        layers = [
            nn.Flatten(),
            MyLinear(input_dim, hidden_dim),
            MyBatchNorm1d(hidden_dim),
            nn.ReLU()
        ]

        # 2. 堆叠残差块
        num_blocks = (num_layers - 2) // 2
        for _ in range(num_blocks):
            layers.append(ResMLPBlock(hidden_dim))

        self.features = nn.Sequential(*layers)

        # 3. 输出层
        self.classifier = MyLinear(hidden_dim, output_dim)

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


# ==========================================
# 3. 10层以上的 CNN (保持不变，供 main_CoC 使用)
# ==========================================
class DeepCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(DeepCNN, self).__init__()

        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(3, 32, 3, padding=1), MyBatchNorm2d(32), nn.ReLU(),
            nn.Conv2d(32, 32, 3, padding=1), MyBatchNorm2d(32), nn.ReLU(),
            nn.MaxPool2d(2, 2),
            # Block 2
            nn.Conv2d(32, 64, 3, padding=1), MyBatchNorm2d(64), nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1), MyBatchNorm2d(64), nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1), MyBatchNorm2d(64), nn.ReLU(),
            nn.MaxPool2d(2, 2),
            # Block 3
            nn.Conv2d(64, 128, 3, padding=1), MyBatchNorm2d(128), nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1), MyBatchNorm2d(128), nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1), MyBatchNorm2d(128), nn.ReLU(),
            nn.MaxPool2d(2, 2),
            # Block 4
            nn.Conv2d(128, 256, 3, padding=1), MyBatchNorm2d(256), nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=1), MyBatchNorm2d(256), nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * 2 * 2, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x