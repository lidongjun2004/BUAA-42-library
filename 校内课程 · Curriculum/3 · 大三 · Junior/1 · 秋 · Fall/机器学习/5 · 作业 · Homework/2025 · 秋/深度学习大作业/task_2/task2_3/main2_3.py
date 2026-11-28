import os
import logging
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from tqdm import tqdm
import matplotlib.pyplot as plt

from task_2.task2_3.models import DeepMLP, DeepCNN

# =====================================================
# 基本配置
# =====================================================
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")
FIG_DIR = os.path.join(BASE_DIR, "figures")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)


# =====================================================
# 日志系统
# =====================================================
def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    log_path = os.path.join(LOG_DIR, f"{name}.log")
    fh = logging.FileHandler(log_path, mode="w")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.propagate = False
    return logger


# =====================================================
# 训练 + 测试（带 tqdm）
# =====================================================
def train_and_test(model, train_loader, test_loader,
                   epochs, lr, name):
    logger = setup_logger(name)
    logger.info("Experiment started")

    optimizer = optim.SGD(
        model.parameters(),
        lr=lr,
        momentum=0.9,
        weight_decay=1e-4
    )
    scheduler = optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=epochs
    )
    criterion = nn.CrossEntropyLoss()

    history = {
        "train_loss": [],
        "train_acc": [],
        "test_acc": []
    }

    for epoch in range(1, epochs + 1):
        # ---------------- Train ----------------
        model.train()
        correct, total = 0, 0
        running_loss = 0.0

        pbar = tqdm(
            train_loader,
            desc=f"{name} | Epoch [{epoch}/{epochs}]",
            leave=False
        )

        for data, target in pbar:
            data, target = data.to(DEVICE), target.to(DEVICE)

            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, pred = output.max(1)
            correct += pred.eq(target).sum().item()
            total += target.size(0)

            pbar.set_postfix(loss=f"{loss.item():.4f}")

        train_loss = running_loss / len(train_loader)
        train_acc = 100.0 * correct / total

        scheduler.step()

        # ---------------- Test ----------------
        model.eval()
        correct, total = 0, 0
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(DEVICE), target.to(DEVICE)
                output = model(data)
                _, pred = output.max(1)
                correct += pred.eq(target).sum().item()
                total += target.size(0)

        test_acc = 100.0 * correct / total

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["test_acc"].append(test_acc)

        logger.info(
            f"Epoch {epoch:03d} | "
            f"Loss: {train_loss:.4f} | "
            f"Train Acc: {train_acc:.2f}% | "
            f"Test Acc: {test_acc:.2f}% | "
            f"LR: {scheduler.get_last_lr()[0]:.5f}"
        )

    logger.info("Training finished")
    return history


# =====================================================
# 画对比图
# =====================================================
def plot_comparison(cnn_hist, mlp_hist):
    epochs = range(1, len(cnn_hist["train_loss"]) + 1)

    # -------- Loss --------
    plt.figure()
    plt.plot(epochs, cnn_hist["train_loss"], label="CNN Train Loss")
    plt.plot(epochs, mlp_hist["train_loss"], label="MLP Train Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training Loss Comparison")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(FIG_DIR, "loss_comparison.png"))
    plt.close()

    # -------- Accuracy --------
    plt.figure()
    plt.plot(epochs, cnn_hist["test_acc"], label="CNN Test Acc")
    plt.plot(epochs, mlp_hist["test_acc"], label="MLP Test Acc")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy (%)")
    plt.title("Test Accuracy Comparison")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(FIG_DIR, "accuracy_comparison.png"))
    plt.close()


# =====================================================
# 主函数
# =====================================================
def main():
    # CIFAR-10 数据增强
    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(
            (0.4914, 0.4822, 0.4465),
            (0.2023, 0.1994, 0.2010)
        ),
    ])
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(
            (0.4914, 0.4822, 0.4465),
            (0.2023, 0.1994, 0.2010)
        ),
    ])

    train_ds = datasets.CIFAR10(
        DATA_DIR, train=True, download=True,
        transform=transform_train
    )
    test_ds = datasets.CIFAR10(
        DATA_DIR, train=False,
        transform=transform_test
    )

    train_loader = DataLoader(
        train_ds, batch_size=256,
        shuffle=True, num_workers=4
    )
    test_loader = DataLoader(
        test_ds, batch_size=1000,
        shuffle=False, num_workers=4
    )

    # ---------------- CNN ----------------
    cnn_model = DeepCNN(num_classes=10).to(DEVICE)
    cnn_history = train_and_test(
        cnn_model,
        train_loader,
        test_loader,
        epochs=50,
        lr=0.01,
        name="CIFAR_CNN_10Layer"
    )

    # ---------------- MLP ----------------
    mlp_model = DeepMLP(
        input_dim=3072,
        hidden_dim=512,
        num_layers=32
    ).to(DEVICE)

    mlp_history = train_and_test(
        mlp_model,
        train_loader,
        test_loader,
        epochs=80,
        lr=0.1,
        name="CIFAR_ResMLP_32Layer"
    )

    # ---------------- Plot ----------------
    plot_comparison(cnn_history, mlp_history)


if __name__ == "__main__":
    main()
