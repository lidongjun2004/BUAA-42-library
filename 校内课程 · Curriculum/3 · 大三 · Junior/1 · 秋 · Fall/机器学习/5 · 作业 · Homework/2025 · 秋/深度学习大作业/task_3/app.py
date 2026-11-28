import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import torch
import torch.nn as nn
from torchvision import models, transforms
import os

# 尝试导入拖拽库，如果没有安装则自动降级
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD

    HAS_DND = True
    BaseClass = TkinterDnD.Tk
except ImportError:
    print("未检测到 tkinterdnd2，拖拽功能将不可用。建议运行 pip install tkinterdnd2")
    HAS_DND = False
    BaseClass = tk.Tk

# ================= 配置区域 =================
MODEL_PATH = 'food_model_final.pth'  # 你的模型路径
CLASS_NAMES = ['汉堡 (Hamburger)', '饼 (Pie)', '寿司 (Sushi)']  # 对应的中文名

# 美食主题配色
COLOR_BG = "#FFF8E1"  # 奶油色背景
COLOR_ACCENT = "#FF7043"  # 诱人的橙红色 (按钮)
COLOR_TEXT_MAIN = "#3E2723"  # 深咖啡色 (主标题)
COLOR_TEXT_SUB = "#5D4037"  # 浅褐色 (副标题)
COLOR_FRAME = "#FFE0B2"  # 浅橙色边框
FONT_TITLE = ("Microsoft YaHei UI", 20, "bold")
FONT_RESULT = ("Microsoft YaHei UI", 18, "bold")
FONT_NORMAL = ("Microsoft YaHei UI", 10)


# ===========================================

class FoodClassifierApp(BaseClass):
    def __init__(self):
        super().__init__()

        self.title("🍔 汉堡 vs 🥧 馅饼 vs 🍣 寿司 - 智能识别")
        self.geometry("600x750")
        self.configure(bg=COLOR_BG)
        self.resizable(False, False)

        # 1. 初始化模型
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = self.load_model()
        self.transform = self.get_transforms()

        # 2. 搭建界面
        self.setup_ui()

        # 3. 启用拖拽 (如果库存在)
        if HAS_DND:
            self.drop_target_register(DND_FILES)
            self.dnd_bind('<<Drop>>', self.drop_image)

    def load_model(self):
        """加载训练好的 ResNet 模型"""
        try:
            print("正在加载模型...")
            model = models.resnet18(pretrained=False)
            model.fc = nn.Linear(model.fc.in_features, 3)  # 3类
            model.load_state_dict(torch.load(MODEL_PATH, map_location=self.device))
            model.to(self.device)
            model.eval()
            print("模型加载成功！")
            return model
        except Exception as e:
            messagebox.showerror("错误", f"无法加载模型文件：{MODEL_PATH}\n请确保模型文件在同一目录下！\n错误信息: {e}")
            return None

    def get_transforms(self):
        """预测时的预处理"""
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def setup_ui(self):
        # --- 顶部：标题区域 ---
        top_frame = tk.Frame(self, bg=COLOR_BG, pady=20)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text="今天吃什么？", font=("Microsoft YaHei UI", 12),
                 bg=COLOR_BG, fg=COLOR_TEXT_SUB).pack()
        tk.Label(top_frame, text="AI 美食鉴别器", font=FONT_TITLE,
                 bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(pady=5)

        # --- 中部：结果显示 ---
        self.result_var = tk.StringVar()
        self.result_var.set("等待输入图片...")
        self.conf_var = tk.StringVar()
        self.conf_var.set("")

        result_frame = tk.Frame(self, bg=COLOR_FRAME, padx=20, pady=10)
        result_frame.pack(fill="x", padx=40, pady=10)

        self.lbl_result = tk.Label(result_frame, textvariable=self.result_var,
                                   font=FONT_RESULT, bg=COLOR_FRAME, fg=COLOR_ACCENT)
        self.lbl_result.pack()

        self.lbl_conf = tk.Label(result_frame, textvariable=self.conf_var,
                                 font=("Arial", 10), bg=COLOR_FRAME, fg=COLOR_TEXT_SUB)
        self.lbl_conf.pack()

        # --- 中部：图片显示区域 (拖拽区) ---
        canvas_frame = tk.Frame(self, bg=COLOR_BG, pady=10)
        canvas_frame.pack()

        # 创建一个虚线边框的区域，暗示这里可以拖拽
        self.canvas = tk.Canvas(canvas_frame, width=400, height=400,
                                bg="#FFF", highlightthickness=2, highlightbackground=COLOR_FRAME)
        self.canvas.pack()

        # 默认显示的文字
        self.placeholder_text = self.canvas.create_text(200, 200,
                                                        text="拖动图片到这里\n或者点击下方按钮",
                                                        font=("Microsoft YaHei UI", 14), fill="#AAA")

        self.image_on_canvas = None  # 用于保存图片引用防止被回收

        # --- 底部：控制区 ---
        bottom_frame = tk.Frame(self, bg=COLOR_BG, pady=30)
        bottom_frame.pack(fill="x")

        # 路径输入框
        self.entry_path = tk.Entry(bottom_frame, width=40, font=("Arial", 10), fg="#555")
        self.entry_path.pack(pady=5)
        self.entry_path.insert(0, "在此输入图片路径...")

        # 按钮
        btn_select = tk.Button(bottom_frame, text="📂 选择图片", command=self.select_image,
                               bg=COLOR_ACCENT, fg="white", font=("Microsoft YaHei UI", 12, "bold"),
                               relief="flat", padx=20, pady=5, cursor="hand2")
        btn_select.pack(pady=10)

    def process_image(self, file_path):
        """核心逻辑：读取图片 -> 显示 -> 预测"""
        if not os.path.isfile(file_path):
            return

        # 1. 清理并显示文件路径
        file_path = file_path.replace("{", "").replace("}", "")  # 修复 tkinterdnd 路径带括号的bug
        self.entry_path.delete(0, tk.END)
        self.entry_path.insert(0, file_path)

        try:
            # 2. UI显示图片 (缩放到 400x400 以适应界面)
            pil_img = Image.open(file_path)

            # 保持比例缩放
            display_img = pil_img.copy()
            display_img.thumbnail((400, 400))

            self.tk_img = ImageTk.PhotoImage(display_img)

            # 清空画布并绘制新图
            self.canvas.delete("all")
            self.canvas.create_image(200, 200, image=self.tk_img)  # 居中显示

            # 3. AI 预测
            self.predict(pil_img)

        except Exception as e:
            messagebox.showerror("错误", f"无法处理图片：{e}")

    def predict(self, pil_img):
        """调用模型进行预测"""
        if self.model is None:
            return

        try:
            # 预处理：转RGB -> Resize -> Tensor -> Norm
            img_tensor = pil_img.convert('RGB')
            img_tensor = self.transform(img_tensor).unsqueeze(0).to(self.device)

            with torch.no_grad():
                outputs = self.model(img_tensor)
                probs = torch.nn.functional.softmax(outputs, dim=1)  # 计算概率
                conf, predicted = torch.max(probs, 1)

            class_idx = predicted.item()
            confidence = conf.item() * 100

            # 更新 UI 文字
            self.result_var.set(f"这是：{CLASS_NAMES[class_idx]}")
            self.conf_var.set(f"置信度: {confidence:.2f}%")

            # 根据置信度改变颜色 (如果很确定则是绿色，不确定是红色)
            if confidence > 80:
                self.lbl_result.config(fg="#4CAF50")  # 绿色
            elif confidence > 50:
                self.lbl_result.config(fg=COLOR_ACCENT)  # 橙色
            else:
                self.lbl_result.config(fg="#F44336")  # 红色

        except Exception as e:
            print(e)
            self.result_var.set("预测出错")

    # --- 事件处理 ---
    def select_image(self):
        """点击按钮触发"""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.process_image(file_path)

    def drop_image(self, event):
        """拖拽触发"""
        if event.data:
            self.process_image(event.data)


if __name__ == "__main__":
    app = FoodClassifierApp()
    app.mainloop()