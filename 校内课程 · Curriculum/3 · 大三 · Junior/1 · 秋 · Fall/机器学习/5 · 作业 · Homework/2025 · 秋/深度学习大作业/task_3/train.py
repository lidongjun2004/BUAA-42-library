import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from tqdm import tqdm
import logging
import matplotlib.pyplot as plt


def main():
    # ================== 基本配置 ==================
    data_dir = 'dataset'
    num_classes = 3
    batch_size = 32
    num_epochs = 10

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    os.makedirs('.', exist_ok=True)

    # ================== 日志配置 ==================
    logging.basicConfig(
        filename='train.log',
        filemode='w',
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s'
    )

    logging.info("========== Training Started ==========")
    logging.info(f"Device: {device}")
    logging.info(f"Epochs: {num_epochs}, Batch size: {batch_size}")

    print(f"使用设备: {device}")

    # ================== 数据增强 ==================
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ToTensor(),
            transforms.Normalize(
                [0.485, 0.456, 0.406],
                [0.229, 0.224, 0.225]
            )
        ]),
        'val': transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(
                [0.485, 0.456, 0.406],
                [0.229, 0.224, 0.225]
            )
        ]),
    }

    image_datasets = {
        x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x])
        for x in ['train', 'val']
    }

    dataloaders = {
        x: torch.utils.data.DataLoader(
            image_datasets[x],
            batch_size=batch_size,
            shuffle=True,
            num_workers=0
        )
        for x in ['train', 'val']
    }

    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
    class_names = image_datasets['train'].classes

    logging.info(f"Class names: {class_names}")
    print(f"类别映射: {class_names}")

    # ================== 构建模型 ==================
    model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    # ================== 记录曲线数据 ==================
    train_losses, val_losses = [], []
    train_accs, val_accs = [], []

    # ================== 训练循环 ==================
    for epoch in range(num_epochs):
        print(f"\nEpoch {epoch + 1}/{num_epochs}")
        logging.info(f"Epoch {epoch + 1}/{num_epochs}")

        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            loader = dataloaders[phase]
            pbar = tqdm(loader, desc=f"Epoch {epoch + 1}/{num_epochs} [{phase}]")

            for inputs, labels in pbar:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

                pbar.set_postfix(
                    Loss=loss.item(),
                    Acc=(torch.sum(preds == labels.data).item() / inputs.size(0))
                )

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double().item() / dataset_sizes[phase]

            logging.info(
                f"{phase.upper()} | Loss: {epoch_loss:.4f} | Acc: {epoch_acc:.4f}"
            )

            print(f"{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")

            if phase == 'train':
                train_losses.append(epoch_loss)
                train_accs.append(epoch_acc)
            else:
                val_losses.append(epoch_loss)
                val_accs.append(epoch_acc)

    # ================== 保存模型 ==================
    torch.save(model.state_dict(), 'food_model_final.pth')
    logging.info("Model saved as food_model_final.pth")
    print("模型已保存为 food_model_final.pth")

    # ================== 绘制 Loss 曲线 ==================
    plt.figure()
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label='Val Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training & Validation Loss')
    plt.legend()
    plt.grid()
    plt.savefig('loss_curve.png')
    plt.close()

    # ================== 绘制 Acc 曲线 ==================
    plt.figure()
    plt.plot(train_accs, label='Train Acc')
    plt.plot(val_accs, label='Val Acc')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('Training & Validation Accuracy')
    plt.legend()
    plt.grid()
    plt.savefig('acc_curve.png')
    plt.close()

    logging.info("Training finished successfully.")
    print("训练完成，已保存 loss_curve.png 和 acc_curve.png")


if __name__ == '__main__':
    main()
