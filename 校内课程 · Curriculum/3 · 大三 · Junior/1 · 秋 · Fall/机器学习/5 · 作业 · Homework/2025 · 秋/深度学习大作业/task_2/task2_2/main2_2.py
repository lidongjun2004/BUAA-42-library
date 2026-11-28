import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from tqdm import tqdm
import logging

from task_2.task2_2.modules2_2 import MyLinear, MyBatchNorm1d

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# =====================================================
# 模型定义
# =====================================================
class ResBlock(nn.Module):
    def __init__(self, hidden_dim, act_fn=nn.ReLU):
        super(ResBlock, self).__init__()
        self.layer = nn.Sequential(
            MyLinear(hidden_dim, hidden_dim),
            MyBatchNorm1d(hidden_dim),
            act_fn(),
            MyLinear(hidden_dim, hidden_dim),
            MyBatchNorm1d(hidden_dim)
        )
        self.act = act_fn()

    def forward(self, x):
        return self.act(x + self.layer(x))


class DeepMLP(nn.Module):
    def __init__(self, act_fn=nn.ReLU, num_layers=32):
        super(DeepMLP, self).__init__()
        self.input_layer = nn.Sequential(
            nn.Flatten(),
            MyLinear(784, 64),
            MyBatchNorm1d(64),
            act_fn()
        )
        layers = [ResBlock(64, act_fn) for _ in range((num_layers - 2) // 2)]
        self.res_blocks = nn.Sequential(*layers)
        self.output_layer = MyLinear(64, 10)

    def forward(self, x):
        x = self.input_layer(x)
        x = self.res_blocks(x)
        x = self.output_layer(x)
        return x

# =====================================================
# 权重初始化函数
# =====================================================
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

# =====================================================
# 训练与评估
# =====================================================
def run_epoch(model, loader, optimizer, criterion, is_train=True):
    model.train() if is_train else model.eval()
    total_loss, correct, total = 0, 0, 0
    loop = tqdm(loader, desc="Train" if is_train else "Eval", leave=False)
    with torch.set_grad_enabled(is_train):
        for data, target in loop:
            data, target = data.to(DEVICE), target.to(DEVICE)
            if is_train:
                optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            if is_train:
                loss.backward()
                optimizer.step()
            total_loss += loss.item() * data.size(0)
            correct += output.argmax(1).eq(target).sum().item()
            total += data.size(0)
            loop.set_postfix(loss=total_loss/total, acc=100.*correct/total)
    return total_loss / total, 100. * correct / total

# =====================================================
# 绘图函数
# =====================================================
def plot_results(all_results, filename):
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False

    epochs = range(1, 11)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    for name, data in all_results.items():
        axes[0].plot(epochs, data['train_loss'], '-', label=f'{name} Train')
        axes[0].plot(epochs, data['test_loss'], '--', label=f'{name} Test')
        axes[1].plot(epochs, data['train_acc'], '-', label=f'{name} Train')
        axes[1].plot(epochs, data['test_acc'], '--', label=f'{name} Test')

    axes[0].set_title('Loss Curve')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].set_title('Accuracy Curve')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy (%)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.savefig(os.path.join(ROOT_DIR, filename), dpi=300)
    print(f"Plot saved to {filename}")

# =====================================================
# 主函数
# =====================================================
def main():
    os.makedirs(os.path.join(ROOT_DIR, 'data'), exist_ok=True)
    os.makedirs(os.path.join(ROOT_DIR, 'logs'), exist_ok=True)

    # 日志设置
    logging.basicConfig(
        filename=os.path.join(ROOT_DIR, 'logs', 'task2_2.log'),
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s'
    )

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    train_loader = DataLoader(
        datasets.MNIST(os.path.join(ROOT_DIR,'data'), train=True, download=True, transform=transform),
        batch_size=256, shuffle=True
    )
    test_loader = DataLoader(
        datasets.MNIST(os.path.join(ROOT_DIR,'data'), train=False, download=True, transform=transform),
        batch_size=1000
    )

    # =========================
    # 优化器实验
    # =========================
    logging.info("=== Optimizer Experiment ===")
    optimizers_list = ['SGD', 'Adam', 'RMSprop']
    opt_results = {}
    for opt_name in optimizers_list:
        logging.info(f"Running {opt_name}...")
        print(f"=== Optimizer: {opt_name} ===")
        model = DeepMLP(num_layers=32).to(DEVICE)
        criterion = nn.CrossEntropyLoss()
        if opt_name == 'SGD':
            optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
        elif opt_name == 'Adam':
            optimizer = optim.Adam(model.parameters(), lr=0.001)
        elif opt_name == 'RMSprop':
            optimizer = optim.RMSprop(model.parameters(), lr=0.001)

        logs = {'train_loss': [], 'train_acc': [], 'test_loss': [], 'test_acc': []}
        for epoch in range(1, 11):
            t_loss, t_acc = run_epoch(model, train_loader, optimizer, criterion, is_train=True)
            v_loss, v_acc = run_epoch(model, test_loader, optimizer, criterion, is_train=False)
            logs['train_loss'].append(t_loss); logs['train_acc'].append(t_acc)
            logs['test_loss'].append(v_loss); logs['test_acc'].append(v_acc)
            logging.info(f"{opt_name} Epoch {epoch}: Train Acc {t_acc:.2f}%, Test Acc {v_acc:.2f}%")
        opt_results[opt_name] = logs

    plot_results(opt_results, 'result_optimizer.png')

    # =========================
    # 初始化实验
    # =========================
    logging.info("=== Initialization Experiment ===")
    init_methods = ['Kaiming', 'Xavier', 'Normal', 'Zero']
    init_results = {}
    for method in init_methods:
        logging.info(f"Running {method} Init...")
        print(f"=== Init: {method} ===")
        model = DeepMLP(num_layers=32).to(DEVICE)
        model.apply(lambda m: init_weights(m, method))
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        criterion = nn.CrossEntropyLoss()

        logs = {'train_loss': [], 'train_acc': [], 'test_loss': [], 'test_acc': []}
        for epoch in range(1, 11):
            t_loss, t_acc = run_epoch(model, train_loader, optimizer, criterion, is_train=True)
            v_loss, v_acc = run_epoch(model, test_loader, optimizer, criterion, is_train=False)
            logs['train_loss'].append(t_loss); logs['train_acc'].append(t_acc)
            logs['test_loss'].append(v_loss); logs['test_acc'].append(v_acc)
            logging.info(f"{method} Epoch {epoch}: Train Acc {t_acc:.2f}%, Test Acc {v_acc:.2f}%")
        init_results[method] = logs

    plot_results(init_results, 'result_init.png')

    # =========================
    # 激活函数实验
    # =========================
    logging.info("=== Activation Experiment ===")
    activations = {'ReLU': nn.ReLU, 'Sigmoid': nn.Sigmoid, 'Tanh': nn.Tanh}
    act_results = {}
    for name, act_fn in activations.items():
        logging.info(f"Running {name} Activation...")
        print(f"=== Activation: {name} ===")
        model = DeepMLP(act_fn=act_fn, num_layers=32).to(DEVICE)
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        criterion = nn.CrossEntropyLoss()

        logs = {'train_loss': [], 'train_acc': [], 'test_loss': [], 'test_acc': []}
        for epoch in range(1, 11):
            t_loss, t_acc = run_epoch(model, train_loader, optimizer, criterion, is_train=True)
            v_loss, v_acc = run_epoch(model, test_loader, optimizer, criterion, is_train=False)
            logs['train_loss'].append(t_loss); logs['train_acc'].append(t_acc)
            logs['test_loss'].append(v_loss); logs['test_acc'].append(v_acc)
            logging.info(f"{name} Epoch {epoch}: Train Acc {t_acc:.2f}%, Test Acc {v_acc:.2f}%")
        act_results[name] = logs

    plot_results(act_results, 'result_activation.png')


if __name__ == '__main__':
    main()
