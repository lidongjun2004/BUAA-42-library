// Slide 04 - Why 3x3 (BUAA style)
const { YH, EN, header, titleBlock, footer } = require('./_buaa.js');
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: 'FFFFFF' };
  header(slide, pres, theme);
  titleBlock(slide, pres, theme, '为什么是 3x3 卷积核');

  const rows = [
    ['1', '感受野等价', '两个 3x3 等于一个 5x5, 三个等于一个 7x7, 小核堆叠覆盖同样范围'],
    ['2', '更强的非线性', '三层间嵌入 3 个 ReLU, 单个 7x7 只有 1 个, 表达力更强'],
    ['3', '更少的参数', '27C^2 (三层 3x3) 对比 49C^2 (单层 7x7), 省约 44% 参数']
  ];
  let yy = 1.66;
  rows.forEach((r) => {
    slide.addShape(pres.shapes.OVAL, { x: 0.5, y: yy, w: 0.46, h: 0.46, fill: { color: theme.primary } });
    slide.addText(r[0], { x: 0.5, y: yy, w: 0.46, h: 0.46, fontSize: 17, fontFace: EN, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', margin: 0 });
    slide.addText(r[1], { x: 1.12, y: yy - 0.02, w: 3.8, h: 0.34, fontSize: 14.5, fontFace: YH, bold: true, color: theme.primary, margin: 0 });
    slide.addText(r[2], { x: 1.12, y: yy + 0.3, w: 3.85, h: 0.56, fontSize: 10.5, fontFace: YH, color: '595959', margin: 0 });
    yy += 0.92;
  });
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: yy, w: 4.45, h: 0.56, fill: { color: theme.light } });
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: yy, w: 0.09, h: 0.56, fill: { color: theme.accent } });
  slide.addText([
    { text: '1x1 卷积  ', options: { bold: true, color: theme.accent, fontFace: YH } },
    { text: '只加非线性不看空间, 不如 3x3, 空间上下文更重要', options: { color: theme.primary, fontFace: YH } }
  ], { x: 0.7, y: yy, w: 4.15, h: 0.56, fontSize: 10.5, valign: 'middle', margin: 0 });

  // right panel (light blue)
  const rx = 5.35, rpw = 4.15, rpy = 1.62, rph = 3.3;
  slide.addShape(pres.shapes.RECTANGLE, { x: rx, y: rpy, w: rpw, h: rph, fill: { color: theme.light } });
  slide.addText('感受野等价', { x: rx + 0.25, y: rpy + 0.15, w: 3.6, h: 0.3, fontSize: 13, fontFace: YH, bold: true, color: theme.primary, margin: 0 });
  for (let i = 0; i < 3; i++) {
    const sx = rx + 0.5 + i * 0.15, sy = rpy + 0.6 + i * 0.15, sw = 0.8;
    slide.addShape(pres.shapes.RECTANGLE, { x: sx, y: sy, w: sw, h: sw, fill: { color: theme.secondary, transparency: 30 }, line: { color: theme.primary, width: 1 } });
  }
  slide.addText('3 层 3x3', { x: rx + 0.35, y: rpy + 1.82, w: 1.3, h: 0.28, fontSize: 10, fontFace: YH, color: theme.primary, align: 'center', margin: 0 });
  slide.addText('=', { x: rx + 1.78, y: rpy + 0.82, w: 0.45, h: 0.8, fontSize: 26, fontFace: EN, bold: true, color: theme.primary, align: 'center', valign: 'middle', margin: 0 });
  const gx = rx + 2.35, gy = rpy + 0.6, gs = 1.05, n = 7;
  slide.addShape(pres.shapes.RECTANGLE, { x: gx, y: gy, w: gs, h: gs, fill: { color: theme.secondary, transparency: 75 }, line: { color: theme.primary, width: 1.25 } });
  for (let i = 1; i < n; i++) {
    const off = gs * i / n;
    slide.addShape(pres.shapes.LINE, { x: gx + off, y: gy, w: 0, h: gs, line: { color: theme.primary, width: 0.4, transparency: 45 } });
    slide.addShape(pres.shapes.LINE, { x: gx, y: gy + off, w: gs, h: 0, line: { color: theme.primary, width: 0.4, transparency: 45 } });
  }
  slide.addText('7x7 感受野', { x: gx - 0.05, y: rpy + 1.82, w: gs + 0.1, h: 0.28, fontSize: 10, fontFace: YH, color: theme.primary, align: 'center', margin: 0 });

  slide.addText('参数更少', { x: rx + 0.25, y: rpy + 2.28, w: 3.6, h: 0.3, fontSize: 13, fontFace: YH, bold: true, color: theme.primary, margin: 0 });
  const barX = rx + 1.3, barMax = 2.2, w27 = barMax * 27 / 49;
  slide.addShape(pres.shapes.RECTANGLE, { x: barX, y: rpy + 2.66, w: w27, h: 0.24, fill: { color: theme.primary } });
  slide.addText('3x3 x3', { x: rx + 0.2, y: rpy + 2.64, w: 1.0, h: 0.28, fontSize: 9.5, fontFace: EN, color: theme.primary, align: 'right', valign: 'middle', margin: 0 });
  slide.addText('27C^2', { x: barX, y: rpy + 2.64, w: w27 - 0.06, h: 0.28, fontSize: 9.5, fontFace: EN, bold: true, color: 'FFFFFF', align: 'right', valign: 'middle', margin: 0 });
  slide.addShape(pres.shapes.RECTANGLE, { x: barX, y: rpy + 2.96, w: barMax, h: 0.24, fill: { color: theme.secondary } });
  slide.addText('7x7 x1', { x: rx + 0.2, y: rpy + 2.94, w: 1.0, h: 0.28, fontSize: 9.5, fontFace: EN, color: theme.primary, align: 'right', valign: 'middle', margin: 0 });
  slide.addText('49C^2', { x: barX, y: rpy + 2.94, w: barMax - 0.06, h: 0.28, fontSize: 9.5, fontFace: EN, bold: true, color: 'FFFFFF', align: 'right', valign: 'middle', margin: 0 });

  footer(slide, pres, theme, 4);
}
module.exports = { createSlide };
