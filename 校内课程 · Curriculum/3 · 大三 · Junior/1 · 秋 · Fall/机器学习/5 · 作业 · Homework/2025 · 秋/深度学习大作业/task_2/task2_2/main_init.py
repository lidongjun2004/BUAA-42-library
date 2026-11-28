import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from task_2.task2_2.modules2_2 import MyLinear, MyBatchNorm1d

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ==========================================
# 模型定义
# ==========================================
class ResBlock(nn.Module):
    def __init__(self, hidden_dim):
        super(ResBlock, self).__init__()
        self.layer = nn.Sequential(
            MyLinear(hidden_dim, hidden_dim),
            MyBatchNorm1d(hidden_dim),
            nn.ReLU(),
            MyLinear(hidden_dim, hidden_dim),
            MyBatchNorm1d(hidden_dim)
        )
        self.relu = nn.ReLU()

    def forward(self, x): return self.relu(x + self.layer(x))


class DeepMLP(nn.Module):
    def __init__(self, num_layers=32):
        super(DeepMLP, self).__init__()
        self.input_layer = nn.Sequential(nn.Flatten(), MyLinear(784, 64), MyBatchNorm1d(64), nn.ReLU())
        layers = [ResBlock(64) for _ in range((num_layers - 2) // 2)]
        self.res_blocks = nn.Sequential(*layers)
        self.output_layer = MyLinear(64, 10)

    def forward(self, x):
        x = self.input_layer(x)
        x = self.res_blocks(x)
        x = self.output_layer(x)
        return x


# ==========================================
# 初始化与绘图
# ==========================================
def init_weights(m, method):
    if isinstance(m, MyLinear):
        if method == 'Kaiming':
            nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
        elif method == 'Xavier':
            nn.init.xavier_normal_(m.weight)
        elif method == 'Normal':
            nn.init.normal_(m.weight, mean=0, std=0.01)
        elif method == 'Zero':
            nn.init.constant_(m.weight, 0)
        if m.bias is not None:
            nn.init.constant_(m.bias, 0)


def run_epoch(model, loader, optimizer, criterion, is_train=True):
    model.train() if is_train else model.eval()
    total_loss, correct, total = 0, 0, 0
    with torch.set_grad_enabled(is_train):
        for data, target in loader:
            data, target = data.to(DEVICE), target.to(DEVICE)
            if is_train: optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            if is_train:
                loss.backward()
                optimizer.step()
            total_loss += loss.item() * data.size(0)
            correct += output.argmax(1).eq(target).sum().item()
            total += data.size(0)
    return total_loss / total, 100. * correct / total


def plot_results(results, filename="result_init.png"):
    # === 设置字体 ===
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False

    epochs = range(1, 11)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    for name, data in results.items():
        ax1.plot(epochs, data['train_loss'], linestyle='-', label=f'{name} Train')
        ax1.plot(epochs, data['test_loss'], linestyle='--', label=f'{name} Test')

        ax2.plot(epochs, data['train_acc'], linestyle='-', label=f'{name} Train')
        ax2.plot(epochs, data['test_acc'], linestyle='--', label=f'{name} Test')

    ax1.set_title('Loss Curve (Initialization)')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.set_title('Accuracy Curve (Initialization)')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.savefig(filename, dpi=300)
    print(f"Plot saved to {filename}")


def main():
    print(f"=== Initialization Experiment on {DEVICE} ===")
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
    train_loader = DataLoader(datasets.MNIST('./data', train=True, transform=transform), batch_size=256, shuffle=True)
    test_loader = DataLoader(datasets.MNIST('./data', train=False, transform=transform), batch_size=1000)

    init_methods = ['Kaiming', 'Xavier', 'Normal', 'Zero']
    all_results = {}

    for method in init_methods:
        print(f"Running {method} Init...")
        model = DeepMLP(num_layers=32).to(DEVICE)
        model.apply(lambda m: init_weights(m, method))

        optimizer = optim.Adam(model.parameters(), lr=0.001)
        criterion = nn.CrossEntropyLoss()

        logs = {'train_loss': [], 'train_acc': [], 'test_loss': [], 'test_acc': []}
        for epoch in range(1, 11):
            t_loss, t_acc = run_epoch(model, train_loader, optimizer, criterion, is_train=True)
            v_loss, v_acc = run_epoch(model, test_loader, optimizer, criterion, is_train=False)
            logs['train_loss'].append(t_loss);
            logs['train_acc'].append(t_acc)
            logs['test_loss'].append(v_loss);
            logs['test_acc'].append(v_acc)
            print(f"  Epoch {epoch}: Train Acc {t_acc:.2f}%, Test Acc {v_acc:.2f}%")
        all_results[method] = logs

    plot_results(all_results)


if __name__ == '__main__':
    main()