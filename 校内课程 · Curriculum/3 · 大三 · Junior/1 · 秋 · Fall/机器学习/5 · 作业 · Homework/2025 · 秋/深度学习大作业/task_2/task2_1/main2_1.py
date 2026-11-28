import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import time
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
from datetime import datetime

from .modules2_1 import MyLinear, MyBatchNorm1d

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ==========================================
# 1. ResBlock
# ==========================================
class ResBlock(nn.Module):
    def __init__(self, hidden_dim):
        super().__init__()
        self.layer = nn.Sequential(
            MyLinear(hidden_dim, hidden_dim),
            MyBatchNorm1d(hidden_dim),
            nn.ReLU(),
            MyLinear(hidden_dim, hidden_dim),
            MyBatchNorm1d(hidden_dim)
        )
        self.relu = nn.ReLU()

    def forward(self, x):
        return self.relu(self.layer(x) + x)


# ==========================================
# 2. 32-layer ResMLP
# ==========================================
class DeepMLP(nn.Module):
    def __init__(self, input_dim=784, output_dim=10, hidden_dim=64, num_layers=32):
        super().__init__()

        self.input_layer = nn.Sequential(
            nn.Flatten(),
            MyLinear(input_dim, hidden_dim),
            MyBatchNorm1d(hidden_dim),
            nn.ReLU()
        )

        num_blocks = (num_layers - 2) // 2
        self.res_blocks = nn.Sequential(
            *[ResBlock(hidden_dim) for _ in range(num_blocks)]
        )

        self.output_layer = MyLinear(hidden_dim, output_dim)

    def forward(self, x):
        x = self.input_layer(x)
        x = self.res_blocks(x)
        return self.output_layer(x)


# ==========================================
# 3. 主函数
# ==========================================
def main():
    print(f"\n=== MNIST 32-Layer ResMLP on {DEVICE} ===")

    BATCH_SIZE = 256
    LR = 0.001
    EPOCHS = 10

    # ---------- BASE_DIR ----------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # ---------- 数据 ----------
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    data_dir = os.path.join(BASE_DIR, "data")
    train_ds = datasets.MNIST(data_dir, train=True, download=True, transform=transform)
    test_ds = datasets.MNIST(data_dir, train=False, transform=transform)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=1000)

    # ---------- 日志 ----------
    log_dir = os.path.join(BASE_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "train.log")

    with open(log_path, "w") as f:
        f.write("=== Training Log ===\n")

    # ---------- 模型 ----------
    model = DeepMLP(num_layers=32).to(DEVICE)
    optimizer = optim.Adam(model.parameters(), lr=LR)
    criterion = nn.CrossEntropyLoss()

    # ---------- 用于画图 ----------
    history = {
        "epoch": [],
        "train_loss": [],
        "train_acc": [],
        "test_acc": []
    }

    # ---------- 训练 ----------
    for epoch in range(1, EPOCHS + 1):
        start_time = time.time()
        model.train()

        total_loss = 0.0
        correct = total = 0

        pbar = tqdm(train_loader, desc=f"Epoch [{epoch}/{EPOCHS}]", ncols=100)

        for data, target in pbar:
            data, target = data.to(DEVICE), target.to(DEVICE)

            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * target.size(0)
            pred = output.argmax(1)
            correct += pred.eq(target).sum().item()
            total += target.size(0)

            pbar.set_postfix(loss=loss.item())

        train_loss = total_loss / total
        train_acc = 100. * correct / total

        # ---------- 测试 ----------
        model.eval()
        correct_test = 0
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(DEVICE), target.to(DEVICE)
                pred = model(data).argmax(1)
                correct_test += pred.eq(target).sum().item()

        test_acc = 100. * correct_test / len(test_loader.dataset)
        duration = time.time() - start_time

        # ---------- 终端输出 ----------
        print(f"Epoch {epoch} | "
              f"Loss {train_loss:.4f} | "
              f"Train {train_acc:.2f}% | "
              f"Test {test_acc:.2f}% | "
              f"Time {duration:.1f}s")

        # ---------- 写入 log ----------
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a") as f:
            f.write(
                f"[{now}] "
                f"Epoch {epoch}/{EPOCHS} | "
                f"Loss: {train_loss:.4f} | "
                f"Train Acc: {train_acc:.2f}% | "
                f"Test Acc: {test_acc:.2f}% | "
                f"Time: {duration:.1f}s\n"
            )

        # ---------- 保存曲线数据 ----------
        history["epoch"].append(epoch)
        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["test_acc"].append(test_acc)

    plot_curves(history, log_dir)


# ==========================================
# 4. 绘图
# ==========================================
def plot_curves(history, log_dir):
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.plot(history["epoch"], history["train_loss"], marker="o")
    plt.title("Training Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")

    plt.subplot(1, 2, 2)
    plt.plot(history["epoch"], history["train_acc"], label="Train Acc")
    plt.plot(history["epoch"], history["test_acc"], label="Test Acc")
    plt.legend()
    plt.title("Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy (%)")

    plt.tight_layout()
    plt.savefig(os.path.join(log_dir, "curves.png"))
    plt.show()


if __name__ == "__main__":
    main()
