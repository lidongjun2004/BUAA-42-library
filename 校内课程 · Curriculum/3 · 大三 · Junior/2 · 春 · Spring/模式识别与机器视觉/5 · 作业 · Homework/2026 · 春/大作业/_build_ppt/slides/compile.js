const path = require('path');
const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Mavis';
pres.title = 'VGGNet paper walkthrough (7 min)';

const theme = {
  primary: '003049',   // deep blue - titles / dark panels
  secondary: '669bbc', // light blue - secondary text
  accent: 'c1121f',    // academic red - emphasis
  light: 'ffffff',     // white - cards / panels
  bg: 'fdf0d5'         // cream - slide background
};

// Speaker notes (7-min walkthrough). Full-width punctuation is fine inside JS
// string literals; it only breaks compilation when used as JS syntax, not as content.
const notes = [
  '开场：今天我分享深度学习里一篇奠基性的论文 —— VGGNet，来自 2014 年牛津大学的 VGG 组。它的核心一句话就能讲清楚：想让卷积网络更强，就把它做得更深，而且只用最小的 3x3 卷积核一层层堆起来。下面我用大概七分钟，把它的设计思路和实验结论讲清楚。',
  '整个分享分六部分：先讲研究背景和它要回答的问题，然后是为什么选 3x3 卷积核这个核心设计，接着看 A 到 E 六种网络配置，再讲训练和测试的策略，重点是实验结果，最后聊聊它的历史意义和局限。',
  '先看背景。2014 年，卷积网络已经远超传统手工特征，但主流网络都很浅，大概只有 8 个权重层，而且第一层喜欢用 11x11、7x7 这样的大卷积核。一个关键问题始终没被系统回答：网络到底需要多深？这篇论文的做法很干净 —— 固定其它所有设置，只把深度从 11 层一路加到 19 层，卷积核全部统一成最小的 3x3，这样就能单独量化深度的贡献。',
  '为什么是 3x3？三个理由。第一，感受野等价：两个 3x3 叠起来等于一个 5x5，三个等于一个 7x7，小核堆叠能覆盖同样大的范围。第二，非线性更强：三层之间夹了三个 ReLU，而单个 7x7 只有一个。第三，参数更少：三层 3x3 是 27 个 C 平方，单个 7x7 要 49 个，省了大约 44%。论文还试过 1x1 卷积，它只增加非线性、不看空间，效果不如 3x3，说明空间上下文很重要。',
  '网络结构非常规整：五个卷积块，通道从 64 开始，每过一次池化翻倍，到 512 为止；一共五次 2x2 池化，把 224 的图一路降到 7x7，最后接三个全连接层。从 A 到 E 只是不断加卷积层，16 层的就是 VGG-16，19 层的是 VGG-19。所有卷积都是步长 1、padding 1，尺寸只由池化改变。参数大约 1.38 亿，其中约 90% 都集中在全连接层。另外 A-LRN 证明了 LRN 没用，后面全弃掉了。',
  '训练上有两个关键技巧：一是预训练初始化，深网络不好训，他们先训最浅的 A，再用它去初始化更深的网络；二是 scale jittering，训练时把图片短边在 256 到 512 之间随机缩放，相当于多尺度数据增强。测试时用 dense 评估，把三个全连接层改写成卷积，整张图一次跑完；再配合 multi-crop 多裁剪，两者边界处理不同、互补，融合后还能再涨点。',
  '这是最关键的结果。看这张柱状图，top-1 错误率随着层数加深一路下降，从 A 的 29.6% 降到最佳设置下 E 的 25.5%，这就是深度有效最直接的证据。还能读出四点：同样 16 层，用 3x3 的 D 全面优于用了 1x1 的 C；LRN 反而拖后腿；多尺度训练明显有效；不过到 19 层之后收益开始递减。最好的单个模型能做到 top-1 24.8%、top-5 7.5%。',
  '横向比一下。在 2014 年的 ILSVRC 分类赛，VGG 拿了第二，7.3%，冠军是 GoogLeNet 的 6.7%；但单个网络比，VGG 的 7.0% 反而优于 GoogLeNet 的 7.9%，定位赛 VGG 还拿了冠军。更深远的是迁移能力：把预训练好的 VGG 当特征提取器，不微调、直接接一个线性 SVM，在 VOC、Caltech 这些数据集上全面刷新了纪录。这也是 VGG 后来被到处复用的原因。',
  '意义和局限。贡献是：用扎实的实验证明了深度是提升能力的核心杠杆，而且结构极简，没有任何新拓扑，成了多年的通用骨干网。局限也很清楚：计算量大，一张图要 153 亿次运算；参数太多，90% 堆在全连接层；深度卡在 19 层，再深就没增益，这要等 2015 年的 ResNet 残差连接才突破；而且当时还没有 Batch Norm，训练全靠精心的初始化。',
  '总结一句话：不需要复杂的拓扑，只需要足够的深度和规范的构建块。四个要点：深度是核心杠杆、3x3 小核堆叠更深更省、简洁即力量成为通用 backbone、承上启下直接启发了 ResNet 和 Inception。我的分享到这里，谢谢大家。'
];

// Capture the slide created inside each module so we can attach notes
// without modifying any slide file.
let lastSlide = null;
const _addSlide = pres.addSlide.bind(pres);
pres.addSlide = function (...a) { lastSlide = _addSlide(...a); return lastSlide; };

for (let i = 1; i <= 10; i++) {
  const id = String(i).padStart(2, '0');
  require(path.join(__dirname, 'slide-' + id + '.js')).createSlide(pres, theme);
  if (lastSlide && notes[i - 1]) lastSlide.addNotes(notes[i - 1]);
}

pres.writeFile({ fileName: path.join(__dirname, 'output', 'VGGNet-paper-7min.pptx') })
  .then((f) => console.log('written:', f))
  .catch((e) => { console.error(e); process.exit(1); });
