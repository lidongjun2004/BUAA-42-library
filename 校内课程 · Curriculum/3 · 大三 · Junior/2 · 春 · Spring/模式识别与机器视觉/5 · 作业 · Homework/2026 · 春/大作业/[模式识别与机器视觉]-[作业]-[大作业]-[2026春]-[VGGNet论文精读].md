# Very Deep Convolutional Networks for Large-Scale Image Recognition

Karen Simonyan, Andrew Zisserman (Visual Geometry Group, University of Oxford)

---

## 一、这篇论文想回答什么问题

在 2014 年前后，卷积神经网络（ConvNet）已在大规模图像识别中展现出远超传统手工特征的能力，但围绕网络结构的核心设计问题仍然开放：**网络究竟需要多深才能充分发挥其表示能力？** 当时的主流架构（AlexNet 8 层、ZFNet 8 层、OverFeat 8 层）大多只有 8 个权重层，且普遍在第一层使用较大的卷积核（<equation>11\times11</equation> 或 <equation>7\times7</equation>）来获取足够的感受野。这种设计虽然直觉上合理，但在深度方向上几乎没有被系统探索过。

本文的核心贡献非常清晰：**在控制其他变量的前提下，系统地评估网络深度对图像分类精度的影响。** 作者的做法是将所有卷积核统一为最小的 <equation>3\times3</equation>（以及部分配置中使用 <equation>1\times1</equation>），然后逐步把网络从 11 个权重层加深到 19 个权重层，观察精度的变化。这一实验结论——"深度至关重要"——成为后续 ResNet、Inception 等更深网络的理论前提之一，也使 VGG-16 和 VGG-19 成为计算机视觉领域最广泛复用的预训练特征提取器。

---

## 二、为什么选择 <equation>3\times3</equation> 卷积核：核心设计直觉

### 感受野等价性

一个关键的几何观察是：两个连续的 <equation>3\times3</equation> 卷积层（中间不做空间池化）等效于一个 <equation>5\times5</equation> 的感受野；三个连续的 <equation>3\times3</equation> 卷积层等效于一个 <equation>7\times7</equation> 的感受野。因此，将一个大卷积核拆分成多个 <equation>3\times3</equation> 的堆叠，在覆盖相同空间范围的前提下可以获得两个明确的好处：

**好处一：更强的非线性建模能力。** 三层 <equation>3\times3</equation> 之间嵌入了三个 ReLU 激活函数，而单个 <equation>7\times7</equation> 层只有一个。更多的非线性变换意味着判别函数更具表达力。

**好处二：更少的参数。** 假设输入和输出的通道数都是 <equation>C</equation>，三层 <equation>3\times3</equation> 的参数量为：

<equation>3 \times (3^2 C^2) = 27C^2</equation>

而一层 <equation>7\times7</equation> 的参数量为：

<equation>7^2 C^2 = 49C^2</equation>

后者比前者多出约 81%。从正则化角度看，将一个 <equation>7\times7</equation> 的滤波器强制分解为三个 <equation>3\times3</equation> 的滤波器（中间插入非线性），相当于对大滤波器施加了一种结构化的低秩约束，有助于减少过拟合。

<equation>1\times1</equation> 卷积的角色

在部分配置中（如 configuration C），作者还使用了 <equation>1\times1</equation> 卷积。<equation>1\times1</equation> 卷积不改变感受野大小，本质上是对同一空间位置上的通道做线性变换——但由于后接 ReLU，它实际引入了额外的非线性。这一设计思想与 Network in Network（Lin et al., 2014）一脉相承。后续实验表明，<equation>1\times1</equation> 卷积虽然通过增加非线性带来了一定改善，但效果不如 <equation>3\times3</equation> 卷积——说明空间上下文信息（即非平凡感受野）对分类精度同样重要。

---

## 三、网络配置全览：从 A 到 E

作者设计了六种网络配置（A、A-LRN、B、C、D、E），它们共享相同的宏观结构——卷积层堆叠 + 三个全连接层——只在卷积层的数量上递增。Table 1 给出了完整的逐层描述。

<lark-table rows="13" cols="7" column-widths="105,105,105,105,105,105,105">

  <lark-tr>
    <lark-td>
      配置 {align="center"}
    </lark-td>
    <lark-td>
      A {align="center"}
    </lark-td>
    <lark-td>
      A-LRN {align="center"}
    </lark-td>
    <lark-td>
      B {align="center"}
    </lark-td>
    <lark-td>
      C {align="center"}
    </lark-td>
    <lark-td>
      D (VGG-16) {align="center"}
    </lark-td>
    <lark-td>
      E (VGG-19) {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      权重层数 {align="center"}
    </lark-td>
    <lark-td>
      11 {align="center"}
    </lark-td>
    <lark-td>
      11 {align="center"}
    </lark-td>
    <lark-td>
      13 {align="center"}
    </lark-td>
    <lark-td>
      16 {align="center"}
    </lark-td>
    <lark-td>
      16 {align="center"}
    </lark-td>
    <lark-td>
      19 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **block 1** {align="center"}
    </lark-td>
    <lark-td>
      conv3-64 {align="center"}
    </lark-td>
    <lark-td>
      conv3-64, LRN {align="center"}
    </lark-td>
    <lark-td>
      conv3-64 ×2 {align="center"}
    </lark-td>
    <lark-td>
      conv3-64 ×2 {align="center"}
    </lark-td>
    <lark-td>
      conv3-64 ×2 {align="center"}
    </lark-td>
    <lark-td>
      conv3-64 ×2 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      maxpool {align="center"}
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **block 2** {align="center"}
    </lark-td>
    <lark-td>
      conv3-128 {align="center"}
    </lark-td>
    <lark-td>
      conv3-128 {align="center"}
    </lark-td>
    <lark-td>
      conv3-128 ×2 {align="center"}
    </lark-td>
    <lark-td>
      conv3-128 ×2 {align="center"}
    </lark-td>
    <lark-td>
      conv3-128 ×2 {align="center"}
    </lark-td>
    <lark-td>
      conv3-128 ×2 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      maxpool {align="center"}
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **block 3** {align="center"}
    </lark-td>
    <lark-td>
      conv3-256 ×2 {align="center"}
    </lark-td>
    <lark-td>
      conv3-256 ×2 {align="center"}
    </lark-td>
    <lark-td>
      conv3-256 ×2 {align="center"}
    </lark-td>
    <lark-td>
      conv3-256 ×2, conv1-256 {align="center"}
    </lark-td>
    <lark-td>
      conv3-256 ×3 {align="center"}
    </lark-td>
    <lark-td>
      conv3-256 ×4 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      maxpool {align="center"}
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **block 4** {align="center"}
    </lark-td>
    <lark-td>
      conv3-512 ×2 {align="center"}
    </lark-td>
    <lark-td>
      conv3-512 ×2 {align="center"}
    </lark-td>
    <lark-td>
      conv3-512 ×2 {align="center"}
    </lark-td>
    <lark-td>
      conv3-512 ×2, conv1-512 {align="center"}
    </lark-td>
    <lark-td>
      conv3-512 ×3 {align="center"}
    </lark-td>
    <lark-td>
      conv3-512 ×4 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      maxpool {align="center"}
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **block 5** {align="center"}
    </lark-td>
    <lark-td>
      conv3-512 ×2 {align="center"}
    </lark-td>
    <lark-td>
      conv3-512 ×2 {align="center"}
    </lark-td>
    <lark-td>
      conv3-512 ×2 {align="center"}
    </lark-td>
    <lark-td>
      conv3-512 ×2, conv1-512 {align="center"}
    </lark-td>
    <lark-td>
      conv3-512 ×3 {align="center"}
    </lark-td>
    <lark-td>
      conv3-512 ×4 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      maxpool {align="center"}
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      FC-4096 → FC-4096 → FC-1000 → softmax {align="center"}
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
</lark-table>

其中 `conv3-N` 表示卷积核大小为 <equation>3\times3</equation>、输出通道数为 <equation>N</equation>。每个卷积层后均接 ReLU 激活（表中省略）。通道数从第一个 block 的 64 开始，每经过一个 maxpool 翻倍，直到 512 为止。Maxpool 使用 <equation>2\times2</equation> 窗口、步幅 2，总共 5 次，空间分辨率从 <equation>224\times224</equation> 降至 <equation>7\times7</equation>。

**几个值得注意的设计细节：**

- **无 Local Response Normalisation (LRN)。** A-LRN 是唯一使用 LRN 的配置，实验表明它不仅不能提升精度，还增加了计算量和显存开销，因此后续所有配置均不使用 LRN。
- **所有卷积步幅为 1，padding 为 1。** 这确保 <equation>3\times3</equation> 卷积不改变空间尺寸，尺寸变化完全由 maxpool 控制。
- **三个全连接层配置固定。** 前两层各 4096 个神经元（配 dropout 0.5），最后一层 1000 维对应 ImageNet 的 1000 个类别。

### 参数量

尽管深度大幅增加，VGGNet 的参数量并未爆炸，因为参数主要集中在全连接层而非卷积层。

<lark-table rows="2" cols="6" column-widths="122,122,122,122,122,122">

  <lark-tr>
    <lark-td>
      配置 {align="center"}
    </lark-td>
    <lark-td>
      A, A-LRN {align="center"}
    </lark-td>
    <lark-td>
      B {align="center"}
    </lark-td>
    <lark-td>
      C {align="center"}
    </lark-td>
    <lark-td>
      D {align="center"}
    </lark-td>
    <lark-td>
      E {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      参数量（百万） {align="center"}
    </lark-td>
    <lark-td>
      133 {align="center"}
    </lark-td>
    <lark-td>
      133 {align="center"}
    </lark-td>
    <lark-td>
      134 {align="center"}
    </lark-td>
    <lark-td>
      138 {align="center"}
    </lark-td>
    <lark-td>
      144 {align="center"}
    </lark-td>
  </lark-tr>
</lark-table>

作为对比，OverFeat 的一个更浅但使用更大卷积核的配置包含 1.44 亿参数，与 VGG-19 相当——这说明"深但窄"的网络并不比"浅但宽"的网络更重。

---

## 四、训练策略

### 优化与正则化

训练采用带动量的 mini-batch SGD，具体超参数为：

- batch size = 256
- 动量 = 0.9
- 权重衰减（<equation>L_2</equation> 正则）= <equation>5 \times 10^{-4}</equation>
- 前两个全连接层使用 dropout，比例 0.5
- 初始学习率 <equation>10^{-2}</equation>，当验证集精度不再提升时衰减为原来的 1/10，共衰减 3 次
- 训练总迭代 370K 次（约 74 个 epoch）

作者指出，尽管 VGGNet 比 AlexNet 更深、参数更多，但收敛所需的 epoch 更少，原因可能有二：(a) 更深的结构和更小的卷积核隐式地施加了正则化效果；(b) 部分层采用了预训练初始化。

### 权重初始化策略

深层网络的初始化是一个关键技术难点——不当的初始化会导致梯度消失或爆炸，训练无法启动。作者采用了一种**逐步预训练**策略：先训练最浅的 configuration A（11 层，浅到可以用随机初始化直接训练），然后将 A 的前四个卷积层和三个全连接层的权重作为更深网络的初始化，中间新增的层则随机初始化（权重从均值为 0、方差为 <equation>10^{-2}</equation> 的正态分布采样，偏置初始化为 0）。预初始化的层在训练中不冻结，仍然参与学习率调度。

论文提交后，作者发现 Glorot & Bengio (2010) 提出的随机初始化方法也足以让这些深层网络收敛，无需预训练引导。

### 训练阶段的尺度处理

训练图像的预处理流程为：先将图像等比缩放至最短边为 <equation>S</equation>，然后从中随机裁剪 <equation>224\times224</equation> 的区域，再进行随机水平翻转和随机 RGB 颜色偏移。

对于 <equation>S</equation> 的设置，作者探索了两种策略：

1. **固定尺度训练（single-scale）。** 固定 <equation>S=256</equation> 或 <equation>S=384</equation>。<equation>S=384</equation> 的网络用 <equation>S=256</equation> 的权重初始化，学习率降至 <equation>10^{-3}</equation>。
2. **随机尺度抖动训练（scale jittering）。** 每张图像的 <equation>S</equation> 从 <equation>[256, 512]</equation> 区间均匀采样。这种做法等效于一种多尺度数据增强，使单一模型能够学会识别不同大小的目标。为了训练效率，多尺度模型以 <equation>S=384</equation> 的固定尺度模型为起点进行微调。

### 实现细节

基于 Caffe 框架（2013 年 12 月分支）进行了大量修改以支持多 GPU 数据并行训练：将每个 batch 分到多块 GPU 上并行前向传播和梯度计算，然后同步汇总梯度。在 4 块 NVIDIA Titan Black GPU 上，这种方案带来 3.75 倍加速。单个网络的训练时间约 2–3 周。

---

## 五、测试策略：Dense 评估与 Multi-crop 评估

### Dense 评估

测试时，图像被等比缩放至最短边为 <equation>Q</equation>（测试尺度），然后**将全连接层转换为等价的卷积层**——第一个 FC 层变成 <equation>7\times7</equation> 卷积层，后两个 FC 层变成 <equation>1\times1</equation> 卷积层——使整个网络成为全卷积网络（fully-convolutional network），直接作用于完整图像。输出是一个与类别数相同通道数的空间 score map，对该 map 做全局均值池化得到最终分类得分。此外，原图和水平翻转图的 softmax 概率取平均作为最终预测。

这种方式避免了传统多裁剪方法（如 AlexNet 的 10 crops）的重复计算，效率更高。

### Multi-crop 评估

作者也评估了传统的多裁剪方式：每个尺度取 <equation>5\times5</equation> 的规则网格 + 2 次翻转 = 50 个 crops，三个尺度共 150 个 crops。

Dense 评估和 multi-crop 评估之间存在互补性：Dense 评估中，特征图的 padding 来自图像的邻域信息（自然上下文），而 multi-crop 评估中 padding 为零。将两者的 softmax 概率取平均可以进一步提升精度。

---

## 六、分类实验结果

### 6.1 单尺度测试

在单一测试尺度下，固定 <equation>Q=S</equation>（单尺度训练时）或 <equation>Q=0.5(S_{min}+S_{max})</equation>（多尺度训练时），各配置的验证集结果如下：

<lark-table rows="13" cols="5" column-widths="146,146,146,146,146">

  <lark-tr>
    <lark-td>
      配置 {align="center"}
    </lark-td>
    <lark-td>
      训练 <equation>S</equation> {align="center"}
    </lark-td>
    <lark-td>
      测试 <equation>Q</equation> {align="center"}
    </lark-td>
    <lark-td>
      top-1 error (%) {align="center"}
    </lark-td>
    <lark-td>
      top-5 error (%) {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      A {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      29.6 {align="center"}
    </lark-td>
    <lark-td>
      10.4 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      A-LRN {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      29.7 {align="center"}
    </lark-td>
    <lark-td>
      10.5 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      B {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      28.7 {align="center"}
    </lark-td>
    <lark-td>
      9.9 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      C {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      28.1 {align="center"}
    </lark-td>
    <lark-td>
      9.4 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      C {align="center"}
    </lark-td>
    <lark-td>
      384 {align="center"}
    </lark-td>
    <lark-td>
      384 {align="center"}
    </lark-td>
    <lark-td>
      28.1 {align="center"}
    </lark-td>
    <lark-td>
      9.3 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      C {align="center"}
    </lark-td>
    <lark-td>
      [256;512] {align="center"}
    </lark-td>
    <lark-td>
      384 {align="center"}
    </lark-td>
    <lark-td>
      27.3 {align="center"}
    </lark-td>
    <lark-td>
      8.8 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      D {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      27.0 {align="center"}
    </lark-td>
    <lark-td>
      8.8 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      D {align="center"}
    </lark-td>
    <lark-td>
      384 {align="center"}
    </lark-td>
    <lark-td>
      384 {align="center"}
    </lark-td>
    <lark-td>
      26.8 {align="center"}
    </lark-td>
    <lark-td>
      8.7 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      D {align="center"}
    </lark-td>
    <lark-td>
      [256;512] {align="center"}
    </lark-td>
    <lark-td>
      384 {align="center"}
    </lark-td>
    <lark-td>
      25.6 {align="center"}
    </lark-td>
    <lark-td>
      8.1 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      E {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      27.3 {align="center"}
    </lark-td>
    <lark-td>
      9.0 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      E {align="center"}
    </lark-td>
    <lark-td>
      384 {align="center"}
    </lark-td>
    <lark-td>
      384 {align="center"}
    </lark-td>
    <lark-td>
      26.9 {align="center"}
    </lark-td>
    <lark-td>
      8.7 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      E {align="center"}
    </lark-td>
    <lark-td>
      [256;512] {align="center"}
    </lark-td>
    <lark-td>
      384 {align="center"}
    </lark-td>
    <lark-td>
      **25.5** {align="center"}
    </lark-td>
    <lark-td>
      **8.0** {align="center"}
    </lark-td>
  </lark-tr>
</lark-table>

从这张表中可以读出以下关键结论：

1. **LRN 无用。** A-LRN 与 A 相比不仅没有提升，反而略有下降（29.7% vs 29.6%）。此后所有配置不再使用 LRN。
2. **深度越深，精度越高。** top-1 error 从 A 的 29.6% 一路降至 E 的 25.5%（同为 scale jittering 训练），每增加 2–3 个卷积层都带来可量化的改善。

<equation>3\times3</equation>**优于**<equation>1\times1</equation>**。** C 和 D 同为 16 层，但 C 在 block 3–5 各使用了一个 <equation>1\times1</equation> 卷积代替 <equation>3\times3</equation>。D 在所有三种训练尺度下都优于 C，说明空间上下文的捕获（非平凡感受野）比纯粹增加非线性更有价值。

1. **Scale jittering 显著有效。** 对每种配置，<equation>S \in [256, 512]</equation> 的多尺度训练均大幅优于固定 <equation>S</equation>。
2. **深度收益的边际递减。** D（16 层）和 E（19 层）之间的差距已经很小，暗示在 ImageNet 的数据规模下，19 层左右深度收益趋于饱和。

作者还做了一个额外实验：将 configuration B 的每对 <equation>3\times3</equation> 卷积替换为一个 <equation>5\times5</equation> 卷积，构造出一个具有相同感受野但更浅的网络。结果该浅层网络的 top-1 error 比 B 高出 7%，直接验证了"深层小滤波器优于浅层大滤波器"这一核心论点。

### 6.2 多尺度测试

在测试阶段使用多个尺度 <equation>Q</equation>，将各尺度的 softmax 概率取平均：

<lark-table rows="11" cols="5" column-widths="146,146,146,146,146">

  <lark-tr>
    <lark-td>
      配置 {align="center"}
    </lark-td>
    <lark-td>
      训练 <equation>S</equation> {align="center"}
    </lark-td>
    <lark-td>
      测试 <equation>Q</equation> {align="center"}
    </lark-td>
    <lark-td>
      top-1 error (%) {align="center"}
    </lark-td>
    <lark-td>
      top-5 error (%) {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      B {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      224,256,288 {align="center"}
    </lark-td>
    <lark-td>
      28.2 {align="center"}
    </lark-td>
    <lark-td>
      9.6 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      C {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      224,256,288 {align="center"}
    </lark-td>
    <lark-td>
      27.7 {align="center"}
    </lark-td>
    <lark-td>
      9.2 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      C {align="center"}
    </lark-td>
    <lark-td>
      384 {align="center"}
    </lark-td>
    <lark-td>
      352,384,416 {align="center"}
    </lark-td>
    <lark-td>
      27.8 {align="center"}
    </lark-td>
    <lark-td>
      9.2 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      C {align="center"}
    </lark-td>
    <lark-td>
      [256;512] {align="center"}
    </lark-td>
    <lark-td>
      256,384,512 {align="center"}
    </lark-td>
    <lark-td>
      26.3 {align="center"}
    </lark-td>
    <lark-td>
      8.2 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      D {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      224,256,288 {align="center"}
    </lark-td>
    <lark-td>
      26.6 {align="center"}
    </lark-td>
    <lark-td>
      8.6 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      D {align="center"}
    </lark-td>
    <lark-td>
      384 {align="center"}
    </lark-td>
    <lark-td>
      352,384,416 {align="center"}
    </lark-td>
    <lark-td>
      26.5 {align="center"}
    </lark-td>
    <lark-td>
      8.6 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      D {align="center"}
    </lark-td>
    <lark-td>
      [256;512] {align="center"}
    </lark-td>
    <lark-td>
      256,384,512 {align="center"}
    </lark-td>
    <lark-td>
      **24.8** {align="center"}
    </lark-td>
    <lark-td>
      **7.5** {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      E {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      224,256,288 {align="center"}
    </lark-td>
    <lark-td>
      26.9 {align="center"}
    </lark-td>
    <lark-td>
      8.7 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      E {align="center"}
    </lark-td>
    <lark-td>
      384 {align="center"}
    </lark-td>
    <lark-td>
      352,384,416 {align="center"}
    </lark-td>
    <lark-td>
      26.7 {align="center"}
    </lark-td>
    <lark-td>
      8.6 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      E {align="center"}
    </lark-td>
    <lark-td>
      [256;512] {align="center"}
    </lark-td>
    <lark-td>
      256,384,512 {align="center"}
    </lark-td>
    <lark-td>
      **24.8** {align="center"}
    </lark-td>
    <lark-td>
      **7.5** {align="center"}
    </lark-td>
  </lark-tr>
</lark-table>

测试尺度的选取原则是：固定尺度训练的模型使用与训练尺度相近的三个值 <equation>Q = \{S-32, S, S+32\}</equation>；多尺度训练的模型由于在训练时已经见过更大的尺度范围，因此可以使用跨度更大的 <equation>Q = \{256, 384, 512\}</equation>。

多尺度测试对所有配置都带来了一致的改善。D 和 E 在多尺度训练 + 多尺度测试下达到了相同的最佳单网络性能：top-1 24.8%、top-5 7.5%。

### 6.3 Dense 评估 vs. Multi-crop 评估

<lark-table rows="7" cols="4" column-widths="183,183,183,183">

  <lark-tr>
    <lark-td>
      配置 {align="center"}
    </lark-td>
    <lark-td>
      评估方式 {align="center"}
    </lark-td>
    <lark-td>
      top-1 error (%) {align="center"}
    </lark-td>
    <lark-td>
      top-5 error (%) {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      D {align="center"}
    </lark-td>
    <lark-td>
      dense {align="center"}
    </lark-td>
    <lark-td>
      24.8 {align="center"}
    </lark-td>
    <lark-td>
      7.5 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      D {align="center"}
    </lark-td>
    <lark-td>
      multi-crop {align="center"}
    </lark-td>
    <lark-td>
      24.6 {align="center"}
    </lark-td>
    <lark-td>
      7.5 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      D {align="center"}
    </lark-td>
    <lark-td>
      multi-crop & dense {align="center"}
    </lark-td>
    <lark-td>
      **24.4** {align="center"}
    </lark-td>
    <lark-td>
      **7.2** {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      E {align="center"}
    </lark-td>
    <lark-td>
      dense {align="center"}
    </lark-td>
    <lark-td>
      24.8 {align="center"}
    </lark-td>
    <lark-td>
      7.5 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      E {align="center"}
    </lark-td>
    <lark-td>
      multi-crop {align="center"}
    </lark-td>
    <lark-td>
      24.6 {align="center"}
    </lark-td>
    <lark-td>
      7.4 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      E {align="center"}
    </lark-td>
    <lark-td>
      multi-crop & dense {align="center"}
    </lark-td>
    <lark-td>
      **24.4** {align="center"}
    </lark-td>
    <lark-td>
      **7.1** {align="center"}
    </lark-td>
  </lark-tr>
</lark-table>

三个要点：(1) Multi-crop 略优于 dense，可能因为 150 个 crops 对图像的采样更密集；(2) 两者确实互补，合并后精度进一步提升；(3) 互补性的来源在于边界条件的差异——dense 评估时特征图的 padding 来自相邻图像区域的真实信息，而 multi-crop 评估使用零填充。

### 6.4 模型融合

多个模型的 softmax 概率取平均：

<lark-table rows="5" cols="4" column-widths="183,183,183,183">

  <lark-tr>
    <lark-td>
      模型组合
    </lark-td>
    <lark-td>
      top-1 val {align="center"}
    </lark-td>
    <lark-td>
      top-5 val {align="center"}
    </lark-td>
    <lark-td>
      top-5 test {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      ILSVRC 提交版（7 个网络，dense）
    </lark-td>
    <lark-td>
      24.7 {align="center"}
    </lark-td>
    <lark-td>
      7.5 {align="center"}
    </lark-td>
    <lark-td>
      7.3 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      赛后：D + E（dense）
    </lark-td>
    <lark-td>
      24.0 {align="center"}
    </lark-td>
    <lark-td>
      7.1 {align="center"}
    </lark-td>
    <lark-td>
      7.0 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      赛后：D + E（multi-crop）
    </lark-td>
    <lark-td>
      23.9 {align="center"}
    </lark-td>
    <lark-td>
      7.2 {align="center"}
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      赛后：D + E（multi-crop & dense）
    </lark-td>
    <lark-td>
      **23.7** {align="center"}
    </lark-td>
    <lark-td>
      **6.8** {align="center"}
    </lark-td>
    <lark-td>
      **6.8** {align="center"}
    </lark-td>
  </lark-tr>
</lark-table>

值得注意的是，比赛提交时用了 7 个模型但只达到 7.3% test error，而赛后仅用 2 个最好的多尺度模型就达到了 6.8%。这说明模型质量比数量更重要——scale jittering 训练出的模型本身足够强，融合收益来自模型间的互补性而非简单叠加。

### 6.5 与业界最优方法的对比

<lark-table rows="14" cols="4" column-widths="183,183,183,183">

  <lark-tr>
    <lark-td>
      方法
    </lark-td>
    <lark-td>
      top-1 val (%) {align="center"}
    </lark-td>
    <lark-td>
      top-5 val (%) {align="center"}
    </lark-td>
    <lark-td>
      top-5 test (%) {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **VGG（2 网络，multi-crop & dense）**
    </lark-td>
    <lark-td>
      **23.7** {align="center"}
    </lark-td>
    <lark-td>
      **6.8** {align="center"}
    </lark-td>
    <lark-td>
      **6.8** {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VGG（1 网络，multi-crop & dense）
    </lark-td>
    <lark-td>
      24.4 {align="center"}
    </lark-td>
    <lark-td>
      7.1 {align="center"}
    </lark-td>
    <lark-td>
      7.0 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VGG（ILSVRC 提交，7 网络）
    </lark-td>
    <lark-td>
      24.7 {align="center"}
    </lark-td>
    <lark-td>
      7.5 {align="center"}
    </lark-td>
    <lark-td>
      7.3 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      GoogLeNet（7 网络）
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
    <lark-td>
      **6.7** {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      GoogLeNet（1 网络）
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
    <lark-td>
      7.9 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      MSRA（11 网络）
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
    <lark-td>
      8.1 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      MSRA（1 网络）
    </lark-td>
    <lark-td>
      27.9 {align="center"}
    </lark-td>
    <lark-td>
      9.1 {align="center"}
    </lark-td>
    <lark-td>
      9.1 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Clarifai（多网络）
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
    <lark-td>
      11.7 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Clarifai（1 网络）
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
    <lark-td>
      12.5 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Zeiler & Fergus（6 网络）
    </lark-td>
    <lark-td>
      36.0 {align="center"}
    </lark-td>
    <lark-td>
      14.7 {align="center"}
    </lark-td>
    <lark-td>
      14.8 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Zeiler & Fergus（1 网络）
    </lark-td>
    <lark-td>
      37.5 {align="center"}
    </lark-td>
    <lark-td>
      16.0 {align="center"}
    </lark-td>
    <lark-td>
      16.1 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      OverFeat（7 网络）
    </lark-td>
    <lark-td>
      34.0 {align="center"}
    </lark-td>
    <lark-td>
      13.2 {align="center"}
    </lark-td>
    <lark-td>
      13.6 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Krizhevsky et al.（5 网络）
    </lark-td>
    <lark-td>
      38.1 {align="center"}
    </lark-td>
    <lark-td>
      16.4 {align="center"}
    </lark-td>
    <lark-td>
      16.4 {align="center"}
    </lark-td>
  </lark-tr>
</lark-table>

VGG 在 ILSVRC-2014 分类赛道获得第二名（7.3% test error），仅次于 GoogLeNet（6.7%）。但在**单网络**性能上，VGG 以 7.0% test error 超过 GoogLeNet 的 7.9%，差距达 0.9 个百分点。

这一结果的意义在于：VGG 完全遵循经典的 ConvNet 范式（卷积→池化→全连接），没有引入任何新的拓扑结构（如 GoogLeNet 的 Inception 模块），仅通过增加深度就取得了当时最强的单网络分类能力。这证明了"深度"本身就是提升表示能力的核心杠杆。

---

## 七、定位任务（Localisation）

除分类之外，作者还将 VGGNet 应用于 ILSVRC-2014 的目标定位赛道并夺冠（25.3% test error）。定位任务要求对 top-5 预测类别各输出一个 bounding box。

### 方法

在 VGG-16（configuration D）的基础上，将最后一个全连接层替换为回归层，输出一个 4 维向量（中心坐标 + 宽 + 高）。作者比较了两种回归方式：

- **Single-class regression (SCR)：** 所有类共享一个 4-D 回归头。
- **Per-class regression (PCR)：** 每个类有独立的回归头，输出 4000-D（1000 类 × 4）。

训练时用 Euclidean loss 替代分类的 logistic regression loss，以预训练好的分类网络初始化，初始学习率 <equation>10^{-3}</equation>。

### 配置对比

<lark-table rows="4" cols="3" column-widths="244,244,244">

  <lark-tr>
    <lark-td>
      微调范围 {align="center"}
    </lark-td>
    <lark-td>
      回归方式 {align="center"}
    </lark-td>
    <lark-td>
      定位 error (%) {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      前两个 FC 层 {align="center"}
    </lark-td>
    <lark-td>
      SCR {align="center"}
    </lark-td>
    <lark-td>
      36.4 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      前两个 FC 层 {align="center"}
    </lark-td>
    <lark-td>
      PCR {align="center"}
    </lark-td>
    <lark-td>
      34.3 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      所有层 {align="center"}
    </lark-td>
    <lark-td>
      PCR {align="center"}
    </lark-td>
    <lark-td>
      **33.1** {align="center"}
    </lark-td>
  </lark-tr>
</lark-table>

两个发现：(1) PCR 优于 SCR，与 OverFeat 的结论相反；(2) 微调所有层优于仅微调 FC 层。后者说明定位任务需要卷积层也学习与空间位置相关的更精细的特征表示。

### 完整定位流程结果

完整测试时，分类分支提供 top-5 类别预测，定位分支对全图做 dense 推理得到多个 bounding box 预测，然后用 OverFeat 的 greedy merging 算法合并空间上接近的预测框。

<lark-table rows="5" cols="4" column-widths="183,183,183,183">

  <lark-tr>
    <lark-td>
      训练 <equation>S</equation> {align="center"}
    </lark-td>
    <lark-td>
      测试 <equation>Q</equation> {align="center"}
    </lark-td>
    <lark-td>
      top-5 定位 error (val, %) {align="center"}
    </lark-td>
    <lark-td>
      top-5 定位 error (test, %) {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      256 {align="center"}
    </lark-td>
    <lark-td>
      29.5 {align="center"}
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      384 {align="center"}
    </lark-td>
    <lark-td>
      384 {align="center"}
    </lark-td>
    <lark-td>
      28.2 {align="center"}
    </lark-td>
    <lark-td>
      26.7 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      384 {align="center"}
    </lark-td>
    <lark-td>
      352, 384 {align="center"}
    </lark-td>
    <lark-td>
      27.5 {align="center"}
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      融合：256/256 + 384/352,384 {align="center"}
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      **26.9** {align="center"}
    </lark-td>
    <lark-td>
      **25.3** {align="center"}
    </lark-td>
  </lark-tr>
</lark-table>

Dense 推理相比 center crop 带来了显著提升（从 33.1% 降至约 28%），多尺度测试和模型融合又进一步降低了 error。

### 定位赛道的对比

<lark-table rows="5" cols="3" column-widths="244,244,244">

  <lark-tr>
    <lark-td>
      方法
    </lark-td>
    <lark-td>
      top-5 val error (%) {align="center"}
    </lark-td>
    <lark-td>
      top-5 test error (%) {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **VGG**
    </lark-td>
    <lark-td>
      **26.9** {align="center"}
    </lark-td>
    <lark-td>
      **25.3** {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      GoogLeNet
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
    <lark-td>
      26.7 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      OverFeat
    </lark-td>
    <lark-td>
      30.0 {align="center"}
    </lark-td>
    <lark-td>
      29.9 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Krizhevsky et al.
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
    <lark-td>
      34.2 {align="center"}
    </lark-td>
  </lark-tr>
</lark-table>

VGG 以 25.3% 赢得 ILSVRC-2014 定位赛道冠军，比 GoogLeNet 低 1.4%，比上一届冠军 OverFeat 低近 5%。值得强调的是，VGG 使用了比 OverFeat 更简单的定位方法（没有使用 OverFeat 的多池化偏移技术），完全凭借更强的特征表示取得了更好的结果。

---

## 八、特征迁移：VGG 作为通用视觉特征提取器

深度网络在 ImageNet 上学到的特征究竟有多大的通用性？为回答这个问题，作者将预训练好的 VGG-16（Net-D）和 VGG-19（Net-E）作为固定的特征提取器，评估在多个不同数据集和任务上的迁移效果。

### 特征提取方式

移除最后一个分类全连接层，取倒数第二层的 4096-D 激活作为图像特征。特征在多个尺度 <equation>Q</equation> 下提取并聚合（通过 stacking 或 averaging）。输出特征经 <equation>L_2</equation> 归一化后直接送入线性 SVM，**不做任何微调**。

### 图像分类：VOC 和 Caltech

<lark-table rows="8" cols="5" column-widths="146,146,146,146,146">

  <lark-tr>
    <lark-td>
      方法
    </lark-td>
    <lark-td>
      VOC-2007 (mAP) {align="center"}
    </lark-td>
    <lark-td>
      VOC-2012 (mAP) {align="center"}
    </lark-td>
    <lark-td>
      Caltech-101 (recall) {align="center"}
    </lark-td>
    <lark-td>
      Caltech-256 (recall) {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Zeiler & Fergus
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
    <lark-td>
      79.0 {align="center"}
    </lark-td>
    <lark-td>
      86.5 ± 0.5 {align="center"}
    </lark-td>
    <lark-td>
      74.2 ± 0.3 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Chatfield et al.
    </lark-td>
    <lark-td>
      82.4 {align="center"}
    </lark-td>
    <lark-td>
      83.2 {align="center"}
    </lark-td>
    <lark-td>
      88.4 ± 0.6 {align="center"}
    </lark-td>
    <lark-td>
      77.6 ± 0.1 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      He et al.
    </lark-td>
    <lark-td>
      82.4 {align="center"}
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
    <lark-td>
      **93.4 ± 0.5** {align="center"}
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Wei et al.
    </lark-td>
    <lark-td>
      81.5 (85.2*) {align="center"}
    </lark-td>
    <lark-td>
      81.7 (**90.3***) {align="center"}
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
    <lark-td>
      — {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VGG Net-D (16 层)
    </lark-td>
    <lark-td>
      89.3 {align="center"}
    </lark-td>
    <lark-td>
      89.0 {align="center"}
    </lark-td>
    <lark-td>
      91.8 ± 1.0 {align="center"}
    </lark-td>
    <lark-td>
      85.0 ± 0.2 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VGG Net-E (19 层)
    </lark-td>
    <lark-td>
      89.3 {align="center"}
    </lark-td>
    <lark-td>
      89.0 {align="center"}
    </lark-td>
    <lark-td>
      92.3 ± 0.5 {align="center"}
    </lark-td>
    <lark-td>
      85.1 ± 0.3 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **VGG Net-D & Net-E**
    </lark-td>
    <lark-td>
      **89.7** {align="center"}
    </lark-td>
    <lark-td>
      **89.3** {align="center"}
    </lark-td>
    <lark-td>
      92.7 ± 0.5 {align="center"}
    </lark-td>
    <lark-td>
      **86.2 ± 0.3** {align="center"}
    </lark-td>
  </lark-tr>
</lark-table>

（* 号结果使用了扩展的 2000 类 ILSVRC 数据集预训练）

在 VOC-2007/2012 上，VGG 的迁移特征比此前最好的方法高出 6% 以上的 mAP。在 Caltech-256 上的优势更为显著（86.2% vs 77.6%，提升 8.6%）。

一个有趣的细节：在 VOC 数据集上，多尺度特征的 averaging 和 stacking 表现相当，因为 VOC 中目标出现在各种尺度上，没有特定的尺度语义可供利用；而在 Caltech 数据集上，stacking 明显优于 averaging，因为 Caltech 中目标通常占据整张图像，不同尺度的特征捕获的是不同层次的语义信息（全局 vs 局部），stacking 允许分类器分别利用各尺度的表示。

### 动作分类：VOC-2012

<lark-table rows="6" cols="2" column-widths="365,365">

  <lark-tr>
    <lark-td>
      方法
    </lark-td>
    <lark-td>
      VOC-2012 (mAP) {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Oquab et al. (2014)*
    </lark-td>
    <lark-td>
      70.2 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Gkioxari et al. (2014)
    </lark-td>
    <lark-td>
      73.6 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Hoai (2014)
    </lark-td>
    <lark-td>
      76.3 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **VGG（仅图像）**
    </lark-td>
    <lark-td>
      **79.2** {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **VGG（图像 + bounding box）**
    </lark-td>
    <lark-td>
      **84.0** {align="center"}
    </lark-td>
  </lark-tr>
</lark-table>

VGG 甚至在不使用人物 bounding box 信息的情况下就超越了所有之前的方法。加入 bounding box 后进一步提升至 84.0%。作者强调这里没有引入任何任务特定的启发式设计，纯粹依靠更深网络学到的更强特征表示。

### 更广泛的影响

模型公开后，被广泛用于目标检测（R-CNN 将 AlexNet 替换为 VGG-16 后取得了当时最好的检测结果）、语义分割、图像字幕生成、纹理和材质识别等任务，证明了 VGG 特征的通用性。

---

## 九、整体评价与历史意义

### 核心贡献

这篇论文的贡献可以归结为一个被充分实验验证的核心发现：**在保持网络其他设计不变的前提下，单纯增加深度（通过堆叠**<equation>3\times3</equation>**卷积层）能够持续且显著地提升图像分类性能。**

这个结论在今天看来已是常识，但在 2014 年并非显而易见。在此之前，研究者普遍认为更大的卷积核（如 <equation>11\times11</equation>）对于捕获大范围的图像结构是必要的，而增加层数会导致训练困难（梯度消失、过拟合等问题）。VGGNet 用实验证明了一种更经济的替代方案：用多个小卷积核的堆叠替代大卷积核，同时获得更强的非线性和更少的参数。

### 方法论贡献

除了架构本身，本文的实验方法论也值得注意：

- **变量控制的系统性。** 从 A 到 E 的配置序列，在保持其余结构不变的前提下逐步增加卷积层数，使深度效应可以被干净地度量。
- **多维度评估。** 不仅评估最终精度，还系统考察了 LRN 的效用、<equation>1\times1</equation> vs <equation>3\times3</equation>、单尺度 vs 多尺度、dense vs multi-crop、单模型 vs 融合等设计选择的边际效果。
- **迁移实验。** 将 ImageNet 上训练的模型作为特征提取器应用到多个下游数据集，验证了深层特征的通用性。

### 局限性与后续发展

1. **计算成本高。** VGG-16 需要约 153 亿次浮点运算处理一张图像，远高于后来的 GoogLeNet（约 15 亿次），这限制了其在资源受限环境中的部署。
2. **参数量集中在全连接层。** 三个 FC 层贡献了约 1.24 亿参数（占总量的约 90%），这在后续工作中被全局平均池化所替代。
3. **深度瓶颈未被突破。** VGGNet 停在 19 层，作者观察到更深的网络没有带来更多增益。这一瓶颈直到 2015 年 ResNet 引入残差连接才被真正突破。
4. **无 Batch Normalisation。** 论文发表时 BN 尚未问世，训练依赖精心的初始化策略和学习率调度。BN 的出现后来使更深网络的训练变得容易得多。

尽管存在这些局限，VGGNet 以其结构的简洁性和特征的通用性，在相当长一段时间内仍是计算机视觉研究中最常用的骨干网络之一。它的设计哲学——"不需要复杂的拓扑结构，只需要足够的深度和规范的构建块"——对后续深度学习架构的设计产生了深远影响。
