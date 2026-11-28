import torch
from torchvision import datasets, transforms
import os


def get_mean_std(data_dir):
    print(f"正在计算 {data_dir} 的均值和方差，请稍候...")

    # 只需要 ToTensor，不需要 Resize (因为你已经处理过尺寸了)
    # 也不需要 Normalize，因为我们正是要求它
    transform = transforms.Compose([
        transforms.ToTensor()
    ])

    # 加载训练集
    train_dataset = datasets.ImageFolder(os.path.join(data_dir, 'train'), transform)

    # 使用 DataLoader 批量读取
    loader = torch.utils.data.DataLoader(train_dataset, batch_size=32, shuffle=False, num_workers=0)

    mean = 0.
    std = 0.
    total_images_count = 0

    for images, _ in loader:
        # images 形状: [batch_size, 3, 224, 224]
        batch_samples = images.size(0)
        images = images.view(batch_samples, images.size(1), -1)

        # 累加均值和方差
        mean += images.mean(2).sum(0)
        std += images.std(2).sum(0)
        total_images_count += batch_samples

    mean /= total_images_count
    std /= total_images_count

    return mean, std


if __name__ == '__main__':
    data_dir = 'dataset'  # 你的数据集路径

    if os.path.exists(data_dir):
        my_mean, my_std = get_mean_std(data_dir)

        print("\n" + "=" * 30)
        print("计算完成！请把下面这两行数字复制到训练代码中：")
        print("=" * 30)
        print(f"mean = {my_mean.tolist()}")
        print(f"std  = {my_std.tolist()}")
        print("=" * 30)
    else:
        print("错误：找不到 dataset 文件夹")