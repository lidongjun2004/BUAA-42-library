# P3评测机-向滢澔-22375354-230617

本文为评测机的简单说明。
运行环境：**java 22** && **Python3.12**（其他版本未测试，但是大概率支持）

## 功能说明

对于学生来说可以作为debug工具，对于课程组来说可以作为评测用具，包含以下几个功能：

1. 导出机器码对应的输出
2. 对拍机器码输入后的输出结果
3. 对拍机器码输入后的输出结果（P3优化版）
4. 输入asm文件和MARS对比结果
5. 添加一条自定义的指令，和MARS对比

## 文件树说明

- CPU_P3_tester_source_code
  - circ
    - CPU_testbench.circ                  *P3的评测电路*
    - module.circ                         *替代用module*
  - class                                 *存储添加指令的文件夹（必须存在）*
  - mylib
    - dumpTable.py                        *导出logisim评测结果的class*
    - insertRom.py                        *向ROM插入机器码的class*
    - marslib.py                          *和魔改MARS联动导出的class*
    - p3translate.py                      *翻译logisim结果为指令的class*
  - tools
    - generate_random_insrt.py            *生成asm指令小工具*
    - result.asm                          *示例asm文件*
  - fernflower.jar                        **非本人编写** *反编译依赖*
  - logisim_tester.py                     *❤️主程序接口*
  - logisim-generic-2.7.1.jar             **非本人编写** *logisim程序jar*
  - Mars_CO_v0.5.0.1.jar                  *本人二次开发魔改MARS程序jar*
  - README.md                             *本文档*
  - tester_gui.py                         *❤️❤️❤️❤️❤️GUI界面*

## 运行前准备

1. 运行环境：**java 22** 和 **Python3.12**（其他环境似乎也可，未测试）
2. 准备好你的电路
   - 你自己的CPU（**.circ文件**）
   - 别人的CPU对拍（**.circ文件**）（comp模式）
   - ROM机器码（**.txt文件**）（dump和comp模式）
   - 汇编asm文件（**.asm文件**）（mars模式和exercise模式）
   - 课程组提供的指令class文件（**.class文件**）（exercise模式）
3. 检查一下你的CPU电路是否输出xxxxxx，如果是，请先自行修改一下或参阅*已知问题*

## 运行方法

运行以下指令即可：

```bash

python tester_gui.py
```

GUI界面打开之后按照**文字说明**进行操作，结果会产生在下面的输出框内。

## 已知问题

- 在.circ电路的输出为高阻态（x）或者错误（E）的时候，输出框不会输出（未捕获stderr输出）
  - 临时解决方法：保留控制台输出，查看控制台信息即可
- 在各个circ的ROM部件中如果存在异常数据会导致程序无法运行
  - 临时解决方法：评测前请保证各个circ文件可以被logisim正常打开即可
- 电脑性能太差会导致反编译错误（暂未观测到，已打补丁）

## 以下为本人在CO讨论区的帖子

```markdown
# 🌐Logisim+MARS联动评测（EOL）

> EOL，上次更新：2024.10.27 11:19 EOL

！❤重大更新，支持导入课程组class文件：

[下载链接🔗✅modified](https://bhpan.buaa.edu.cn/link/AAFA439BAF127D4E56B040C1162FC087F0)

注意：本项目基本EOL，未来大概率不再进行内容性更新，只进行错误修复，程序基本趋于完善，感谢大家的支持，如果喜欢请留下你的点赞❤。

文件结构
- logisim_tester
  - tools
    - generate_random_insrt.py （随机asm生成器）
    - 许多asm（示例asm）
  - class
    - qaq.class (示例class)
  - CPU_testbench.circ （testbench示例）
  - module.circ （testbench下的子电路module模板）
  - tester_gui.exe （程序本体）
  - logisim-generic-2.7.1.jar （Logisim依赖）
  - Mars_CO_v0.5.0.1.jar (二次魔改MARS依赖）
  - fernflower.jar (反编译依赖)

## 更新日志
- 2024.10.24 19:57 原始版本
- 2024.10.25 0:03 修改了mars的bug，增加小工具
- 2024.10.25 9:46 修改依赖结构，便于运行
- 2024.10.25 16:20 重大更新
  - 修复了循环过多的asm卡死的问题
  - 小工具问题暂未修复
  - 可视化界面！
  - 显示前十个错误，防止错误过多不好找
- 2024.10.25 19:00 修复了由于CompactDataAtZero的问题，修复了一个小工具的bug
- 2024.10.26 18:56 修复了circ文件gbk编码的问题（疑似），修复了寄存器编号误翻译为十六进制的问题（不影响评测结果）
- 2024.10.27 0:32 修改了提示语，以及增加了鲁棒性，已加入自定义指令的代码，但存在问题暂未实装
- 2024.10.27 11:19 支持课程组自定义指令，EOL

## 功能介绍

### 程序主体

可视化界面：
![57460538f688b637af8393079965e17.png](/assets/cscore-image/22375354/82ed6524-8466-4d6f-ae3a-8b611d37d54c/57460538f688b637af8393079965e17.png)
> 注：图缺失——原图（57460538f688b637af8393079965e17.png）未随资料入库；原链接是课程网站 cscore 的站点根路径，本地无法解析。

由此可以很方便的使用了，再也不需要晕头转向！

目前内置四个功能：
1. 导出电路的评测数据
2. 和其他人的电路对拍
3. 和其他人数据对拍+结果翻译
![028fbcf19340cd7358df5baa020d1653.png](/assets/cscore-image/22375354/2c3243e6-3283-4e82-9898-14c795a4b947/028fbcf19340cd7358df5baa020d1653.png)
> 注：图缺失——原图（028fbcf19340cd7358df5baa020d1653.png）未随资料入库；原链接是课程网站 cscore 的站点根路径，本地无法解析。

4. 提供asm文件和circ电路，利用MARS进行结果对比
![ef6f2a13f8099cdaacd539295a58e26.png](/assets/cscore-image/22375354/f8b4d318-663b-4c77-a7b5-fc42297dd466/ef6f2a13f8099cdaacd539295a58e26.png)
> 注：图缺失——原图（ef6f2a13f8099cdaacd539295a58e26.png）未随资料入库；原链接是课程网站 cscore 的站点根路径，本地无法解析。

## 使用说明
解压得到exe文件和一个文件夹，请不要改变文件结构，请在解压后的目录打开命令行或者cd到解压的文件夹内，命令行运行exe并提供参数：
`logisim_tester.exe [参数]`

可选参数：
- dump
- comp
- compp3
- mars
- exercise

分别对应五个功能。

运行启动后只需要按照要求提供“测试电路”、“电路模块模版”（此二者就是每道题的图片里面的测试电路和顶层模块的外形）、“待测电路”以及其他即可。

使用问题和bug反馈可以评论区或者微信直接戳我😋👆

### 小工具

> 警告⚠：小工具不太好使，开始测试之前记得先单独用一下MARS测试一下会不会死循环，如果死循环了要么重新生成一次要么手调一下就好。建议每次生成**最多500行**

制作了一个配合MARS评测的asm生成小工具，运行python并且输入一个数就可以生成大致为这个数量的asm文件，经测验效果很好，甚至帮我自己找到了bug。
本小工具仅针对p3课下数据进行生成，你也可以修改它让它支持更多的指令，目前支持：

`add, sub, ori, lw, sw, beq, lui, nop`

效果截图：
![image.png](/assets/cscore-image/22375354/9c8b1cd7-6268-490d-9b20-4bbcdaf582d5/image.png)
> 注：图缺失——原图（image.png）未随资料入库；原链接是课程网站 cscore 的站点根路径，本地无法解析。

## 近期计划
1. ~~加入数据生成功能，进行随机评测并与MARS对比。~~(check！)
2. ~~更加易用~~（check！）
3. ~~GUI界面~~（check！）
4. 持续更新本文档。
5. ~~魔改一下MARS以支持课程组的class~~（check！）

## 致谢

学长的魔改MARS帮大忙了，虽然是MIT license，但是还是在这里贴一下链接：https://github.com/Toby-Shi-cloud/Mars-with-BUAA-CO-extension
```
