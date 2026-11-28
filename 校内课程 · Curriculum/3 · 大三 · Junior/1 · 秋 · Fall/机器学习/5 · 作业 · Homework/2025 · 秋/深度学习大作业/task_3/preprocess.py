import os
from PIL import Image

# 你的数据集目录
data_dir = 'dataset'


def preprocess_images(root_dir):
    print(f"正在处理 {root_dir} 下的所有图片...")
    print("操作：格式检查 + 转RGB + 强制缩放224x224 + 覆盖原文件")

    count = 0
    errors = 0

    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)

            # 只处理图片文件
            if not file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                continue

            try:
                # 1. 打开图片
                img = Image.open(file_path)

                # 2. 强制转为 RGB
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # 3. 强制调整尺寸 (LANCZOS 是高质量缩放算法)
                img = img.resize((224, 224), Image.Resampling.LANCZOS)

                # 4. 覆盖保存
                img.save(file_path, quality=95)
                count += 1

                if count % 100 == 0:
                    print(f"已处理 {count} 张...")

            except Exception as e:
                print(f"删除损坏文件: {file_path} (错误: {e})")
                os.remove(file_path)
                errors += 1

    print(f"✅ 处理完成！成功: {count} 张, 删除坏图: {errors} 张。")
    print("现在所有图片都是标准的 224x224 像素了。")


if __name__ == '__main__':
    preprocess_images(data_dir)