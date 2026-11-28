import os
import logging
from datetime import datetime

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from tqdm import tqdm
import matplotlib.pyplot as plt

from modules1 import MyLinear


# ===============================
# 1. SixLayerMLP 定义
# ===============================
class SixLayerMLP(nn.Module):
    def __init__(self):
        super(SixLayerMLP, self).__init__()
        self.layers = nn.Sequential(
            MyLinear(784, 512),
            nn.ReLU(),
            MyLinear(512, 256),
            nn.ReLU(),
            MyLinear(256, 128),
            nn.ReLU(),
            MyLinear(128, 64),
            nn.ReLU(),
            MyLinear(64, 32),
            nn.ReLU(),
            MyLinear(32, 10)
        )

    def forward(self, x):
        x = x.view(-1, 784)
        x = self.layers(x)
        return x


# ===============================
# 2. 日志和实验目录
# ===============================
def setup_experiment_logger(exp_dir, hyperparams):
    os.makedirs(exp_dir, exist_ok=True)
    log_file = os.path.join(exp_dir, "train.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logging.info("=" * 60)
    logging.info("Experiment Started")
    logging.info(f"Time: {datetime.now()}")
    logging.info("Hyperparameters:")
    for k, v in hyperparams.items():
        logging.info(f"  {k}: {v}")
    logging.info("=" * 60)


# ===============================
# 3. 训练与测试函数
# ===============================
def train(model, device, train_loader, optimizer, epoch, epochs):
    model.train()
    correct, total = 0, 0
    running_loss = 0.0
    pbar = tqdm(train_loader, desc=f"Epoch {epoch}/{epochs}", ncols=100, leave=False)

    for data, target in pbar:
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.cross_entropy(output, target)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * data.size(0)
        pred = output.argmax(dim=1)
        correct += pred.eq(target).sum().item()
        total += data.size(0)

        pbar.set_postfix({"loss": f"{running_loss/total:.4f}", "acc": f"{100.*correct/total:.2f}%"})

    train_loss = running_loss / total
    train_acc = 100. * correct / total
    logging.info(f"Train Epoch {epoch}: Loss={train_loss:.4f}, Accuracy={train_acc:.2f}%")
    return train_loss, train_acc


def test(model, device, test_loader, epoch):
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.cross_entropy(output, target, reduction='sum').item()
            pred = output.argmax(dim=1)
            correct += pred.eq(target).sum().item()

    test_loss /= len(test_loader.dataset)
    acc = 100. * correct / len(test_loader.dataset)
    logging.info(f"Test Epoch {epoch}: Loss={test_loss:.4f}, Accuracy={acc:.2f}%")
    return test_loss, acc


# ===============================
# 4. 绘图函数
# ===============================
def plot_curves(train_vals, test_vals, ylabel, title, save_path, labels=None):
    plt.figure()
    if labels is None:
        labels = ["Train", "Test"]
    for i, vals in enumerate(train_vals):
        plt.plot(vals, label=f"{labels[i]} (Train)")
    for i, vals in enumerate(test_vals):
        plt.plot(vals, '--', label=f"{labels[i]} (Test)")
    plt.xlabel("Epoch")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(save_path)
    plt.close()


# ===============================
# 5. 主程序
# ===============================
if __name__ == '__main__':
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {DEVICE}")

    # ---------------- 超参数列表 ----------------
    BATCH_SIZES = [64, 128]
    LEARNING_RATES = [0.001, 0.005]
    EPOCHS = 20

    # ---------------- 数据 ----------------
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST('./data', train=False, transform=transform)

    # ---------------- 存储对比曲线数据 ----------------
    all_lr_results = {}  # key=lr, value=(train_loss_list, test_loss_list, train_acc_list, test_acc_list)
    all_bs_results = {}  # key=bs, value=同上

    # =========================
    # 6. 固定 bs，改变 lr
    # =========================
    fixed_bs = BATCH_SIZES[0]
    for lr in LEARNING_RATES:
        exp_name = f"mlp_bs{fixed_bs}_lr{lr}_ep{EPOCHS}"
        exp_dir = os.path.join("experiments", exp_name)
        hyperparams = {"batch_size": fixed_bs, "learning_rate": lr, "epochs": EPOCHS}
        setup_experiment_logger(exp_dir, hyperparams)

        train_loader = DataLoader(train_dataset, batch_size=fixed_bs, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)

        model = SixLayerMLP().to(DEVICE)
        optimizer = optim.Adam(model.parameters(), lr=lr)

        train_losses, train_accs, test_losses, test_accs = [], [], [], []

        for epoch in range(1, EPOCHS + 1):
            t_loss, t_acc = train(model, DEVICE, train_loader, optimizer, epoch, EPOCHS)
            te_loss, te_acc = test(model, DEVICE, test_loader, epoch)
            train_losses.append(t_loss)
            train_accs.append(t_acc)
            test_losses.append(te_loss)
            test_accs.append(te_acc)

        # 保存曲线图
        plot_curves([train_losses], [test_losses], "Loss", f"Loss Curve (lr={lr}, bs={fixed_bs})",
                    os.path.join(exp_dir, "loss_curve.png"))
        plot_curves([train_accs], [test_accs], "Accuracy (%)", f"Acc Curve (lr={lr}, bs={fixed_bs})",
                    os.path.join(exp_dir, "acc_curve.png"))

        all_lr_results[lr] = (train_losses, test_losses, train_accs, test_accs)

    # =========================
    # 7. 固定 lr，改变 bs
    # =========================
    fixed_lr = LEARNING_RATES[0]
    for bs in BATCH_SIZES:
        exp_name = f"mlp_bs{bs}_lr{fixed_lr}_ep{EPOCHS}"
        exp_dir = os.path.join("experiments", exp_name)
        hyperparams = {"batch_size": bs, "learning_rate": fixed_lr, "epochs": EPOCHS}
        setup_experiment_logger(exp_dir, hyperparams)

        train_loader = DataLoader(train_dataset, batch_size=bs, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)

        model = SixLayerMLP().to(DEVICE)
        optimizer = optim.Adam(model.parameters(), lr=fixed_lr)

        train_losses, train_accs, test_losses, test_accs = [], [], [], []

        for epoch in range(1, EPOCHS + 1):
            t_loss, t_acc = train(model, DEVICE, train_loader, optimizer, epoch, EPOCHS)
            te_loss, te_acc = test(model, DEVICE, test_loader, epoch)
            train_losses.append(t_loss)
            train_accs.append(t_acc)
            test_losses.append(te_loss)
            test_accs.append(te_acc)

        plot_curves([train_losses], [test_losses], "Loss", f"Loss Curve (bs={bs}, lr={fixed_lr})",
                    os.path.join(exp_dir, "loss_curve.png"))
        plot_curves([train_accs], [test_accs], "Accuracy (%)", f"Acc Curve (bs={bs}, lr={fixed_lr})",
                    os.path.join(exp_dir, "acc_curve.png"))

        all_bs_results[bs] = (train_losses, test_losses, train_accs, test_accs)

    # =========================
    # 8. 对比图（改变 lr）- loss & acc
    # =========================
    plt.figure()
    for lr in LEARNING_RATES:
        plt.plot(all_lr_results[lr][0], label=f"Train lr={lr}")
        plt.plot(all_lr_results[lr][1], '--', label=f"Test lr={lr}")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title(f"Loss vs lr (bs={fixed_bs})")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join("experiments", f"Loss_vs_lr_bs{fixed_bs}.png"))
    plt.close()

    plt.figure()
    for lr in LEARNING_RATES:
        plt.plot(all_lr_results[lr][2], label=f"Train lr={lr}")
        plt.plot(all_lr_results[lr][3], '--', label=f"Test lr={lr}")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy (%)")
    plt.title(f"Acc vs lr (bs={fixed_bs})")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join("experiments", f"Acc_vs_lr_bs{fixed_bs}.png"))
    plt.close()

    # =========================
    # 9. 对比图（改变 bs）- loss & acc
    # =========================
    plt.figure()
    for bs in BATCH_SIZES:
        plt.plot(all_bs_results[bs][0], label=f"Train bs={bs}")
        plt.plot(all_bs_results[bs][1], '--', label=f"Test bs={bs}")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title(f"Loss vs bs (lr={fixed_lr})")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join("experiments", f"Loss_vs_bs_lr{fixed_lr}.png"))
    plt.close()

    plt.figure()
    for bs in BATCH_SIZES:
        plt.plot(all_bs_results[bs][2], label=f"Train bs={bs}")
        plt.plot(all_bs_results[bs][3], '--', label=f"Test bs={bs}")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy (%)")
    plt.title(f"Acc vs bs (lr={fixed_lr})")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join("experiments", f"Acc_vs_bs_lr{fixed_lr}.png"))
    plt.close()

    print("All experiments finished! All logs and plots saved in ./experiments/")
