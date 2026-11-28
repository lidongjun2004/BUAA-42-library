// Slide 09 - Significance vs Limitations (two columns)
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };
  const YH = 'Microsoft YaHei';
  const makeShadow = () => ({ type: 'outer', color: '003049', blur: 5, offset: 2, angle: 135, opacity: 0.12 });

  slide.addText('历史意义与局限', { x: 0.6, y: 0.4, w: 9, h: 0.6, fontSize: 28, fontFace: YH, bold: true, color: theme.primary, margin: 0 });

  const cardY = 1.3, cardH = 3.75, lw = 4.35;
  const cols = [
    { x: 0.6, head: '贡献  CONTRIBUTIONS', accent: theme.primary, bullets: [
      '用实验证明: 深度是提升表示能力的核心杠杆',
      '多个 3x3 堆叠 = 更强非线性 + 更少参数',
      '结构极简 (conv-pool-fc), 不引入任何新拓扑',
      'VGG-16 / VGG-19 成为通用 backbone, 迁移性极强'
    ] },
    { x: 5.25, head: '局限  LIMITATIONS', accent: theme.accent, bullets: [
      '计算量大: 单张图约 153 亿次浮点运算',
      '参数约 90% 集中在 FC 层 (后被全局平均池化替代)',
      '深度停在 19 层, 更深无增益 (待 ResNet 残差突破)',
      '当时尚无 Batch Norm, 训练依赖精心的初始化'
    ] }
  ];

  cols.forEach((c) => {
    slide.addShape(pres.shapes.RECTANGLE, { x: c.x, y: cardY, w: lw, h: cardH, fill: { color: theme.light }, rectRadius: 0.08, shadow: makeShadow() });
    slide.addShape(pres.shapes.RECTANGLE, { x: c.x, y: cardY, w: lw, h: 0.62, fill: { color: c.accent }, rectRadius: 0.08 });
    // cover bottom rounded corners of header to make it a clean top band
    slide.addShape(pres.shapes.RECTANGLE, { x: c.x, y: cardY + 0.31, w: lw, h: 0.31, fill: { color: c.accent } });
    slide.addText(c.head, { x: c.x + 0.32, y: cardY, w: lw - 0.5, h: 0.62, fontSize: 15, fontFace: YH, bold: true, color: 'FFFFFF', valign: 'middle', margin: 0 });
    slide.addText(
      c.bullets.map((b, i) => ({ text: b, options: { bullet: true, breakLine: i < c.bullets.length - 1 } })),
      { x: c.x + 0.32, y: cardY + 0.85, w: lw - 0.6, h: cardH - 1.05, fontSize: 12, fontFace: YH, color: theme.primary, paraSpaceAfter: 13, margin: 0 }
    );
  });

  // Page badge
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fill: { color: theme.primary } });
  slide.addText('09', { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fontSize: 11, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: 'Arial', bold: true, margin: 0 });
}
module.exports = { createSlide };
