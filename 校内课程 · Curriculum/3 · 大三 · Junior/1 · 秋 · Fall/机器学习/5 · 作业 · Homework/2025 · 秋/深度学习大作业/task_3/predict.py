import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# === 在这里修改你要测试的图片路径 ===
TEST_IMAGE_PATH = 'dick.jpg'


# =================================

def predict():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # 1. 类别名称 (一定要和训练时的输出顺序一致，通常是按字母排序)
    class_names = ['hamburger', 'pie', 'sushi']

    # 2. 准备模型
    model = models.resnet18(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, 3)

    # 加载刚才训练好的权重
    try:
        model.load_state_dict(torch.load('food_model_final.pth', map_location=device))
    except FileNotFoundError:
        print("错误：找不到模型文件 food_model_final.pth，请先运行训练脚本！")
        return

    model = model.to(device)
    model.eval()

    # 3. 预处理 (新图片必须 resize，因为它没经过我们的预处理脚本)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        # MY_MEAN = [0.556, 0.469, 0.384]  # <--- 数据集均值
        # MY_STD = [0.234, 0.238, 0.234]  # <--- 数据集方差
    ])

    # 4. 预测
    try:
        img = Image.open(TEST_IMAGE_PATH).convert('RGB')
        input_tensor = transform(img).unsqueeze(0).to(device)  # 加一个维度 Batch Size

        with torch.no_grad():
            outputs = model(input_tensor)
            probs = torch.nn.functional.softmax(outputs, dim=1)  # 计算概率
            conf, predicted = torch.max(probs, 1)

        print(f"🖼️  图片: {TEST_IMAGE_PATH}")
        print(f"🤖 预测结果: {class_names[predicted.item()]}")
        print(f"📊 置信度: {conf.item() * 100:.2f}%")

    except Exception as e:
        print(f"读取图片失败: {e}")


if __name__ == '__main__':
    predict()