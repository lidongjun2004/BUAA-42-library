// Slide 06 - Training & Testing strategies (two cards + takeaway)
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };
  const YH = 'Microsoft YaHei';
  const makeShadow = () => ({ type: 'outer', color: '003049', blur: 5, offset: 2, angle: 135, opacity: 0.12 });

  slide.addText('训练与测试策略', { x: 0.6, y: 0.4, w: 9, h: 0.6, fontSize: 28, fontFace: YH, bold: true, color: theme.primary, margin: 0 });

  const cardY = 1.3, cardH = 3.05, lw = 4.35;
  const cards = [
    { x: 0.6, tag: '训练  TRAINING', accent: theme.accent, bullets: [
      'SGD + 动量: batch 256, momentum 0.9, L2 = 5e-4, dropout 0.5',
      '学习率 1e-2, 验证停滞则除以 10 (共 3 次), 约 74 个 epoch',
      '预训练初始化: 先训浅层 A, 再去初始化更深网络 (后发现 Glorot 初始化亦可)',
      '多尺度训练 (scale jittering): 短边 S 在 [256, 512] 随机采样, 等效数据增强'
    ] },
    { x: 5.25, tag: '测试  TESTING', accent: '780000', bullets: [
      'Dense 评估: 把 3 个 FC 层改写成卷积 (7x7 + 1x1), 整张图一次跑完',
      'Multi-crop 评估: 每个尺度取 50 个裁剪, 三个尺度共 150 个',
      '两种方式的边界填充不同, 互补; 融合后精度再提升'
    ] }
  ];

  cards.forEach((c) => {
    slide.addShape(pres.shapes.RECTANGLE, { x: c.x, y: cardY, w: lw, h: cardH, fill: { color: theme.light }, rectRadius: 0.08, shadow: makeShadow() });
    slide.addShape(pres.shapes.RECTANGLE, { x: c.x, y: cardY, w: 0.1, h: cardH, fill: { color: c.accent } });
    slide.addText(c.tag, { x: c.x + 0.32, y: cardY + 0.2, w: lw - 0.5, h: 0.4, fontSize: 16, fontFace: YH, bold: true, color: theme.primary, margin: 0 });
    slide.addText(
      c.bullets.map((b, i) => ({ text: b, options: { bullet: true, breakLine: i < c.bullets.length - 1 } })),
      { x: c.x + 0.32, y: cardY + 0.78, w: lw - 0.6, h: cardH - 1.0, fontSize: 11.5, fontFace: YH, color: theme.primary, paraSpaceAfter: 10, margin: 0 }
    );
  });

  // Bottom takeaway
  const by = 4.5;
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: by, w: 9.0, h: 0.55, fill: { color: theme.primary }, rectRadius: 0.06, shadow: makeShadow() });
  slide.addText([
    { text: '关键   ', options: { bold: true, color: 'F4A261', fontFace: YH } },
    { text: '预训练初始化 + scale jittering, 是这些深层网络能稳定训练并涨点的两大功臣', options: { color: 'FFFFFF', fontFace: YH } }
  ], { x: 0.9, y: by, w: 8.5, h: 0.55, fontSize: 13, valign: 'middle', margin: 0 });

  // Page badge
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fill: { color: theme.primary } });
  slide.addText('06', { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fontSize: 11, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: 'Arial', bold: true, margin: 0 });
}
module.exports = { createSlide };
