import os
import re
import matplotlib.pyplot as plt

# =====================================================
# 配置路径
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
FIG_DIR = os.path.join(BASE_DIR, "figures")

# 确保图片保存目录存在
os.makedirs(FIG_DIR, exist_ok=True)

# 你的 Log 文件名 (根据 main2_3.py 中的 name 参数)
CNN_LOG_NAME = "CIFAR_CNN_10Layer.log"
MLP_LOG_NAME = "CIFAR_ResMLP_32Layer.log"


# =====================================================
# 解析 Log 函数
# =====================================================
def parse_log_file(filename):
    path = os.path.join(LOG_DIR, filename)

    if not os.path.exists(path):
        print(f"Error: Log file not found at {path}")
        return None

    print(f"Parsing {filename}...")

    history = {
        "epochs": [],
        "loss": [],
        "train_acc": [],
        "test_acc": []
    }

    # Log 行格式:
    # Epoch 001 | Loss: 2.3026 | Train Acc: 10.00% | Test Acc: 12.50%
    pattern = re.compile(
        r"Epoch\s+(\d+)\s+\|\s+"
        r"Loss:\s+([\d\.]+)\s+\|\s+"
        r"Train Acc:\s+([\d\.]+)%\s+\|\s+"
        r"Test Acc:\s+([\d\.]+)%"
    )

    with open(path, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                history["epochs"].append(int(match.group(1)))
                history["loss"].append(float(match.group(2)))
                history["train_acc"].append(float(match.group(3)))
                history["test_acc"].append(float(match.group(4)))

    print(f"  -> Found {len(history['epochs'])} epochs.")
    return history


# =====================================================
# 绘图函数
# =====================================================
def plot_comparison(cnn_hist, mlp_hist):
    if cnn_hist is None or mlp_hist is None:
        print("Skipping plots because log parsing failed.")
        return

    # ---------------- Loss 对比 ----------------
    plt.figure(figsize=(10, 6))
    plt.plot(cnn_hist["epochs"], cnn_hist["loss"],
             label="CNN Train Loss", linewidth=2)
    plt.plot(mlp_hist["epochs"], mlp_hist["loss"],
             label="MLP Train Loss", linewidth=2)

    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training Loss Comparison (CNN vs MLP)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)

    loss_path = os.path.join(FIG_DIR, "loss_comparison_from_log.png")
    plt.savefig(loss_path)
    plt.close()
    print(f"Saved loss plot to: {loss_path}")

    # ---------------- Accuracy 四线对比 ----------------
    plt.figure(figsize=(10, 6))

    # CNN
    plt.plot(cnn_hist["epochs"], cnn_hist["train_acc"],
             label="CNN Train Acc", linestyle="--", linewidth=2)
    plt.plot(cnn_hist["epochs"], cnn_hist["test_acc"],
             label="CNN Test Acc", linestyle="-", linewidth=2)

    # MLP
    plt.plot(mlp_hist["epochs"], mlp_hist["train_acc"],
             label="MLP Train Acc", linestyle="--", linewidth=2)
    plt.plot(mlp_hist["epochs"], mlp_hist["test_acc"],
             label="MLP Test Acc", linestyle="-", linewidth=2)

    plt.xlabel("Epoch")
    plt.ylabel("Accuracy (%)")
    plt.title("Accuracy Comparison (Train & Test, CNN vs MLP)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)

    acc_path = os.path.join(FIG_DIR, "accuracy_comparison_from_log.png")
    plt.savefig(acc_path)
    plt.close()
    print(f"Saved accuracy plot to: {acc_path}")


# =====================================================
# 主执行逻辑
# =====================================================
if __name__ == "__main__":
    cnn_data = parse_log_file(CNN_LOG_NAME)
    mlp_data = parse_log_file(MLP_LOG_NAME)

    plot_comparison(cnn_data, mlp_data)
