// Slide 04 - Why 3x3 (benefits + receptive-field viz + param bars)
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };
  const YH = 'Microsoft YaHei';
  const makeShadow = () => ({ type: 'outer', color: '003049', blur: 5, offset: 2, angle: 135, opacity: 0.12 });

  slide.addText('为什么是 3x3 卷积核', { x: 0.6, y: 0.4, w: 9, h: 0.6, fontSize: 28, fontFace: YH, bold: true, color: theme.primary, margin: 0 });
  slide.addText('VGG 把所有卷积核统一缩到最小的 3x3, 再用堆叠去换取深度', { x: 0.62, y: 1.0, w: 9, h: 0.35, fontSize: 13, fontFace: YH, color: theme.secondary, margin: 0 });

  // Left: three numbered benefits
  const rows = [
    ['1', '感受野等价', '两个 3x3 等于一个 5x5, 三个 3x3 等于一个 7x7 -- 用小核堆叠覆盖同样的空间范围'],
    ['2', '更强的非线性', '三层之间嵌入 3 个 ReLU, 单个 7x7 只有 1 个, 判别函数更具表达力'],
    ['3', '更少的参数', '27C^2 (三层 3x3) 对比 49C^2 (单层 7x7), 小核堆叠省约 44% 参数']
  ];
  let yy = 1.6;
  rows.forEach((r) => {
    slide.addShape(pres.shapes.OVAL, { x: 0.62, y: yy, w: 0.5, h: 0.5, fill: { color: theme.accent } });
    slide.addText(r[0], { x: 0.62, y: yy, w: 0.5, h: 0.5, fontSize: 18, fontFace: 'Arial', bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', margin: 0 });
    slide.addText(r[1], { x: 1.28, y: yy - 0.04, w: 3.7, h: 0.35, fontSize: 15, fontFace: YH, bold: true, color: theme.primary, margin: 0 });
    slide.addText(r[2], { x: 1.28, y: yy + 0.32, w: 3.75, h: 0.62, fontSize: 11, fontFace: YH, color: theme.secondary, margin: 0 });
    yy += 1.0;
  });

  // 1x1 note card
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.62, y: yy + 0.02, w: 4.4, h: 0.62, fill: { color: theme.light }, rectRadius: 0.06, shadow: makeShadow() });
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.62, y: yy + 0.02, w: 0.1, h: 0.62, fill: { color: '780000' } });
  slide.addText([
    { text: '1x1 卷积   ', options: { bold: true, color: '780000', fontFace: YH } },
    { text: '只加非线性, 不看空间, 实测不如 3x3 -- 空间上下文更重要', options: { color: theme.primary, fontFace: YH } }
  ], { x: 0.84, y: yy + 0.02, w: 4.1, h: 0.62, fontSize: 10.5, valign: 'middle', margin: 0 });

  // Right visual panel background
  const rx = 5.45, rpw = 4.15;
  slide.addShape(pres.shapes.RECTANGLE, { x: rx, y: 1.6, w: rpw, h: 3.5, fill: { color: theme.light }, rectRadius: 0.1, shadow: makeShadow() });

  // (a) receptive-field equivalence
  slide.addText('感受野等价', { x: rx + 0.25, y: 1.78, w: 3.6, h: 0.3, fontSize: 13, fontFace: YH, bold: true, color: theme.accent, margin: 0 });
  for (let i = 0; i < 3; i++) {
    const sx = rx + 0.45 + i * 0.16, sy = 2.2 + i * 0.16, sw = 0.9;
    slide.addShape(pres.shapes.RECTANGLE, { x: sx, y: sy, w: sw, h: sw, fill: { color: theme.secondary, transparency: 35 }, line: { color: theme.primary, width: 1 } });
  }
  slide.addText('3 层 3x3', { x: rx + 0.35, y: 3.55, w: 1.4, h: 0.3, fontSize: 10.5, fontFace: YH, color: theme.primary, align: 'center', margin: 0 });
  slide.addText('=', { x: rx + 1.78, y: 2.3, w: 0.5, h: 0.9, fontSize: 30, fontFace: 'Arial', bold: true, color: theme.accent, align: 'center', valign: 'middle', margin: 0 });
  // equivalent 7x7 grid
  const gx = rx + 2.4, gy = 2.2, gs = 1.2, n = 7;
  slide.addShape(pres.shapes.RECTANGLE, { x: gx, y: gy, w: gs, h: gs, fill: { color: theme.accent, transparency: 80 }, line: { color: theme.accent, width: 1.25 } });
  for (let i = 1; i < n; i++) {
    const off = gs * i / n;
    slide.addShape(pres.shapes.LINE, { x: gx + off, y: gy, w: 0, h: gs, line: { color: theme.accent, width: 0.5, transparency: 40 } });
    slide.addShape(pres.shapes.LINE, { x: gx, y: gy + off, w: gs, h: 0, line: { color: theme.accent, width: 0.5, transparency: 40 } });
  }
  slide.addText('7x7 感受野', { x: gx, y: 3.55, w: gs, h: 0.3, fontSize: 10.5, fontFace: YH, color: theme.primary, align: 'center', margin: 0 });

  // (b) parameter comparison bars
  slide.addText('参数更少', { x: rx + 0.25, y: 3.95, w: 3.6, h: 0.3, fontSize: 13, fontFace: YH, bold: true, color: theme.accent, margin: 0 });
  const barX = rx + 1.35, barMax = 2.1, w27 = barMax * 27 / 49;
  // bar A: 27 (red), value inside-right white
  slide.addShape(pres.shapes.RECTANGLE, { x: barX, y: 4.35, w: w27, h: 0.26, fill: { color: theme.accent }, rectRadius: 0.03 });
  slide.addText('3x3 x3', { x: rx + 0.25, y: 4.33, w: 1.05, h: 0.3, fontSize: 10, fontFace: 'Arial', color: theme.primary, align: 'right', valign: 'middle', margin: 0 });
  slide.addText('27C^2', { x: barX, y: 4.33, w: w27 - 0.08, h: 0.3, fontSize: 10, fontFace: 'Arial', bold: true, color: 'FFFFFF', align: 'right', valign: 'middle', margin: 0 });
  // bar B: 49 (blue), value inside-right
  slide.addShape(pres.shapes.RECTANGLE, { x: barX, y: 4.72, w: barMax, h: 0.26, fill: { color: theme.secondary }, rectRadius: 0.03 });
  slide.addText('7x7 x1', { x: rx + 0.25, y: 4.7, w: 1.05, h: 0.3, fontSize: 10, fontFace: 'Arial', color: theme.primary, align: 'right', valign: 'middle', margin: 0 });
  slide.addText('49C^2', { x: barX, y: 4.7, w: barMax - 0.08, h: 0.3, fontSize: 10, fontFace: 'Arial', bold: true, color: '003049', align: 'right', valign: 'middle', margin: 0 });

  // Page badge
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fill: { color: theme.primary } });
  slide.addText('04', { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fontSize: 11, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: 'Arial', bold: true, margin: 0 });
}
module.exports = { createSlide };
