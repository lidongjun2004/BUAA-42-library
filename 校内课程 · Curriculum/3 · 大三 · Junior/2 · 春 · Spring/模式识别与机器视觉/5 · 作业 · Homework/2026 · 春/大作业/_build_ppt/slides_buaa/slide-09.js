// Slide 09 - Significance vs Limitations (BUAA style)
const { YH, EN, header, titleBlock, footer } = require('./_buaa.js');
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: 'FFFFFF' };
  header(slide, pres, theme);
  titleBlock(slide, pres, theme, '历史意义与局限');

  const cardY = 1.62, cardH = 3.4, lw = 4.4;
  const cols = [
    { x: 0.5, head: '贡献  CONTRIBUTIONS', hc: theme.primary, bullets: [
      '用实验证明: 深度是提升表示能力的核心杠杆',
      '多个 3x3 堆叠 = 更强非线性 + 更少参数',
      '结构极简 (conv-pool-fc), 不引入任何新拓扑',
      'VGG-16 / VGG-19 成为通用 backbone, 迁移性极强'
    ] },
    { x: 5.1, head: '局限  LIMITATIONS', hc: theme.accent, bullets: [
      '计算量大: 单张图约 153 亿次浮点运算',
      '参数约 90% 集中在 FC 层 (后被全局平均池化替代)',
      '深度停在 19 层, 更深无增益 (待 ResNet 残差突破)',
      '当时尚无 Batch Norm, 训练依赖精心的初始化'
    ] }
  ];
  cols.forEach((c) => {
    slide.addShape(pres.shapes.RECTANGLE, { x: c.x, y: cardY, w: lw, h: cardH, fill: { color: theme.light } });
    slide.addShape(pres.shapes.RECTANGLE, { x: c.x, y: cardY, w: lw, h: 0.58, fill: { color: c.hc } });
    slide.addText(c.head, { x: c.x + 0.34, y: cardY, w: lw - 0.5, h: 0.58, fontSize: 14.5, fontFace: YH, bold: true, color: 'FFFFFF', valign: 'middle', margin: 0 });
    slide.addText(
      c.bullets.map((b, i) => ({ text: b, options: { bullet: true, breakLine: i < c.bullets.length - 1 } })),
      { x: c.x + 0.34, y: cardY + 0.78, w: lw - 0.62, h: cardH - 0.95, fontSize: 11.5, fontFace: YH, color: '333333', paraSpaceAfter: 12, margin: 0 }
    );
  });

  footer(slide, pres, theme, 9);
}
module.exports = { createSlide };
