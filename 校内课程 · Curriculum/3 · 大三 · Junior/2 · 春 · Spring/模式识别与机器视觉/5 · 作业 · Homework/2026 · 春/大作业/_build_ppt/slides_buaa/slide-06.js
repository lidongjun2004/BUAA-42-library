// Slide 06 - Training & Testing (BUAA style)
const { YH, EN, header, titleBlock, footer } = require('./_buaa.js');
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: 'FFFFFF' };
  header(slide, pres, theme);
  titleBlock(slide, pres, theme, '训练与测试策略');

  const cardY = 1.62, cardH = 2.9, lw = 4.4;
  const cards = [
    { x: 0.5, tag: '训练  TRAINING', bullets: [
      'SGD + 动量: batch 256, momentum 0.9, L2 = 5e-4, dropout 0.5',
      '学习率 1e-2, 验证停滞则除以 10 (共 3 次), 约 74 个 epoch',
      '预训练初始化: 先训浅层 A, 再初始化更深网络 (后发现 Glorot 亦可)',
      '多尺度训练 (scale jittering): 短边 S 在 [256, 512] 随机采样'
    ] },
    { x: 5.1, tag: '测试  TESTING', bullets: [
      'Dense 评估: 把 3 个 FC 层改写成卷积 (7x7 + 1x1), 整图一次跑完',
      'Multi-crop 评估: 每尺度取 50 个裁剪, 三尺度共 150 个',
      '两种方式边界填充不同, 互补; 融合后精度再提升'
    ] }
  ];
  cards.forEach((c) => {
    slide.addShape(pres.shapes.RECTANGLE, { x: c.x, y: cardY, w: lw, h: cardH, fill: { color: theme.light } });
    slide.addShape(pres.shapes.RECTANGLE, { x: c.x, y: cardY, w: 0.1, h: cardH, fill: { color: theme.primary } });
    slide.addShape('parallelogram', { x: c.x + 0.32, y: cardY + 0.24, w: 0.32, h: 0.3, fill: { color: theme.primary } });
    slide.addText(c.tag, { x: c.x + 0.78, y: cardY + 0.2, w: lw - 1.0, h: 0.4, fontSize: 15, fontFace: YH, bold: true, color: theme.primary, valign: 'middle', margin: 0 });
    slide.addText(
      c.bullets.map((b, i) => ({ text: b, options: { bullet: true, breakLine: i < c.bullets.length - 1 } })),
      { x: c.x + 0.34, y: cardY + 0.78, w: lw - 0.62, h: cardH - 0.95, fontSize: 11, fontFace: YH, color: '333333', paraSpaceAfter: 9, margin: 0 }
    );
  });

  const by = 4.62;
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: by, w: 9.0, h: 0.5, fill: { color: theme.primary } });
  slide.addText([
    { text: '关键  ', options: { bold: true, color: 'FFE08A', fontFace: YH } },
    { text: '预训练初始化 + scale jittering, 是深层网络能稳定训练并涨点的两大功臣', options: { color: 'FFFFFF', fontFace: YH } }
  ], { x: 0.85, y: by, w: 8.5, h: 0.5, fontSize: 12.5, valign: 'middle', margin: 0 });

  footer(slide, pres, theme, 6);
}
module.exports = { createSlide };
