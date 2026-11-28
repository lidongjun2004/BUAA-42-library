import tkinter as tk
import sys
import os
from tkinter import *
from tkinter import ttk
from  tkinter import filedialog

from logisim_tester import Tester


test_type = ""

original_stdout = sys.stdout

class stdoutRedirect:
    def __init__(self, text_box) -> None:
        self.text_box = text_box
    
    def write(self, text):
        self.text_box.insert(tk.END, text)
        self.text_box.see(tk.END)
        self.text_box.update()
        
    
    def flush(self):
        pass

#输入文件路径
def selectPath_file_tb():
    path_ = filedialog.askopenfilename(filetypes=[("circ", [".circ"] )])
    tbPath.set(path_)
    entry_name_a.config(bg='white')
    
def selectPath_file_module():
    path_ = filedialog.askopenfilename(filetypes=[("circ", [".circ"] )])
    modulePath.set(path_)
    entry_name_b.config(bg='white')

def selectPath_file_query():
    path_ = filedialog.askopenfilename(filetypes=[("circ", [".circ"] )])
    queryPath.set(path_)
    entry_name_c.config(bg='white')
    
def selectPath_file_other():
    path_ = filedialog.askopenfilename(filetypes=[("circ", [".circ"] )])
    otherPath.set(path_)
    entry_name_d.config(bg='white')
    
def selectPath_file_rom():
    path_ = filedialog.askopenfilename(filetypes=[("机器码txt", [".txt"] )])
    romPath.set(path_)
    entry_name_e.config(bg='white')
    
def selectPath_file_asm():
    path_ = filedialog.askopenfilename(filetypes=[("汇编代码", [".asm"] )])
    asmPath.set(path_)
    entry_name_f.config(bg='white')
    
def selectPath_file_class():
    path_ = filedialog.askopenfilename(filetypes=[("指令类", [".class"] )])
    classPath.set(path_)
    entry_name_g.config(bg='white')

def entry_clear():
    entry_name_d.config(bg='white')
    entry_name_e.config(bg='white')
    entry_name_f.config(bg='white')
    entry_name_g.config(bg='white')

def on_select(event):
    selected_option = event.widget.get()
    entry_name_a.config(bg='yellow')
    entry_name_b.config(bg='yellow')
    entry_name_c.config(bg='yellow')
    
    if os.path.exists("./CPU_testbench.circ"):
        tbPath.set(os.path.abspath("./CPU_testbench.circ"))
        entry_name_a.config(bg='white')
    if os.path.exists("./module.circ"):
        modulePath.set(os.path.abspath("./module.circ"))
        entry_name_b.config(bg='white')
    
    if (selected_option == "dump"):
        entry_clear()
        entry_name_e.config(bg='yellow')
    elif (selected_option == "comp"):
        entry_clear()
        entry_name_d.config(bg='yellow')
        entry_name_e.config(bg='yellow')
    elif (selected_option == "compp3"):
        entry_clear()
        entry_name_d.config(bg='yellow')
        entry_name_e.config(bg='yellow')
    elif (selected_option == "mars"):
        entry_clear()
        entry_name_f.config(bg='yellow')
    elif (selected_option == "exercise"):
        entry_clear()
        entry_name_f.config(bg='yellow')
        entry_name_g.config(bg='yellow')
    
    if (tbPath.get() != ""):
        entry_name_a.config(bg='white')
    if (modulePath.get() != ""):
        entry_name_b.config(bg='white')
    if (queryPath.get() != ""):
        entry_name_c.config(bg='white')
    if (otherPath.get() != ""):
        entry_name_d.config(bg='white')
    if (romPath.get() != ""):
        entry_name_e.config(bg='white')
    if (asmPath.get() != ""):
        entry_name_f.config(bg='white')
    if (classPath.get() != ""):
        entry_name_g.config(bg='white')
    
    test_type.set(selected_option)

def on_click_st():
    lt = Tester()
    lt.doTest(test_type.get(),
              tbPath.get(), 
              modulePath.get(), 
              queryPath.get(), 
              otherPath.get(), 
              romPath.get(), 
              asmPath.get(), 
              classPath.get())
    
root = Tk()
frame = Frame(root)
frame.grid()

tbPath = tk.StringVar()
modulePath = tk.StringVar()
queryPath = tk.StringVar()
otherPath = tk.StringVar()
romPath = tk.StringVar()
asmPath = tk.StringVar()
classPath = tk.StringVar()

if os.path.exists("./CPU_testbench.circ"):
    tbPath.set(os.path.abspath("./CPU_testbench.circ"))
if os.path.exists("./module.circ"):
    modulePath.set(os.path.abspath("./module.circ"))

test_type = tk.StringVar()

root.title("logisim评测机-向滢澔")
root.geometry("850x820")
canvas = Canvas(frame, width=850, height=800)


text = tk.Text(root, height=7, width=42, font=("Arial", 12), bd=0)
text.grid(column=0, row=0)
text.insert(tk.INSERT, """
根据你所选的评测方式不同，你需要输入这些路径：
1. dump：ABCE
2. comp：ABCDE
3. compp3： ABCDE
4. MARS：ABCF
5. exercise：ABCFG""")
text.config(state=tk.DISABLED)

text2 = tk.Text(root, height=7, width=40, font=("Arial", 12), bd=0)
text2.grid(column=1, row=0)
text2.insert(tk.INSERT, """
选择你的评测方式：
1. 导出机器码对应的输出
2. 对拍机器码输入后的输出结果
3. 对拍机器码输入后的输出结果（P3优化版）
4. 输入asm文件和MARS对比结果
5. 添加一条自定义的指令，和MARS对比""")
text2.config(state=tk.DISABLED)


tk.Label(root,text="A. testbench.circ路径：").grid(column=0, row=11)
entry_name_a=tk.Entry(root, textvariable = tbPath,width=55)
entry_name_a.grid(column=1, row=11)
tk.Button(root, text = "选择", command = selectPath_file_tb).grid(column=2, row=11)

tk.Label(root,text="B. module.circ路径：").grid(column=0, row=12)
entry_name_b=tk.Entry(root, textvariable = modulePath,width=55)
entry_name_b.grid(column=1, row=12)
tk.Button(root, text = "选择", command = selectPath_file_module).grid(column=2, row=12)

tk.Label(root,text="C. 待测电路路径：").grid(column=0, row=13)
entry_name_c=tk.Entry(root, textvariable = queryPath,width=55)
entry_name_c.grid(column=1, row=13)
tk.Button(root, text = "选择", command = selectPath_file_query).grid(column=2, row=13)

tk.Label(root,text="D. 对拍电路路径：").grid(column=0, row=14)
entry_name_d=tk.Entry(root, textvariable = otherPath,width=55)
entry_name_d.grid(column=1, row=14)
tk.Button(root, text = "选择", command = selectPath_file_other).grid(column=2, row=14)

tk.Label(root,text="E. 机器码路径：").grid(column=0, row=15)
entry_name_e=tk.Entry(root, textvariable = romPath,width=55)
entry_name_e.grid(column=1, row=15)
tk.Button(root, text = "选择", command = selectPath_file_rom).grid(column=2, row=15)

tk.Label(root,text="F. MIPS汇编文件路径：").grid(column=0, row=16)
entry_name_f=tk.Entry(root, textvariable = asmPath,width=55)
entry_name_f.grid(column=1, row=16)
tk.Button(root, text = "选择", command = selectPath_file_asm).grid(column=2, row=16)

tk.Label(root,text="G. class文件路径：").grid(column=0, row=17)
entry_name_g=tk.Entry(root, textvariable = classPath,width=55)
entry_name_g.grid(column=1, row=17)
tk.Button(root, text = "选择", command = selectPath_file_class).grid(column=2, row=17)

text3 = tk.Text(root, height=2, width=20, font=("Arial", 12), pady=0)
text3.grid(column=0, row=9)
text3.insert(tk.INSERT, """
第一步：选择你的评测""")
text3.config(state=tk.DISABLED)

# 创建第一个下拉菜单
# menu1 = ttk.Combobox(root, values=["dump", "comp", "compp3", "mars"])
menu1 = ttk.Combobox(root, values=["dump", "comp", "compp3", "mars", "exercise"])
menu1.bind("<<ComboboxSelected>>", on_select)
menu1.grid(column=0, row=10)

tk.Button(root, text="开始检测", command=on_click_st).grid(column=0, row=19)

text_box = tk.Text(root)
text_box.grid(column=0,columnspan=2,row=20,rowspan=2)
yscrollbar = tk.Scrollbar(root,width=20)
yscrollbar.config(command=text_box.yview)

text_box.config(yscrollcommand=yscrollbar.set)

sys.stdout = stdoutRedirect(text_box)


# start
root.mainloop()