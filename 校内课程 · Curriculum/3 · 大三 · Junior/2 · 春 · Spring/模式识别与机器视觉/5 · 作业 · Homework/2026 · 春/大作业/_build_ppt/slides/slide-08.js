// Slide 08 - Benchmarks & feature transfer (two-column, stat callouts)
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };
  const YH = 'Microsoft YaHei';
  const makeShadow = () => ({ type: 'outer', color: '003049', blur: 5, offset: 2, angle: 135, opacity: 0.12 });

  slide.addText('横向对比与特征迁移', { x: 0.6, y: 0.4, w: 9, h: 0.6, fontSize: 28, fontFace: YH, bold: true, color: theme.primary, margin: 0 });

  // Left card: ILSVRC-2014
  const lx = 0.6, ly = 1.3, lw = 4.35, lh = 3.72;
  slide.addShape(pres.shapes.RECTANGLE, { x: lx, y: ly, w: lw, h: lh, fill: { color: theme.light }, rectRadius: 0.08, shadow: makeShadow() });
  slide.addShape(pres.shapes.RECTANGLE, { x: lx, y: ly, w: 0.1, h: lh, fill: { color: theme.primary } });
  slide.addText('ILSVRC-2014 战绩', { x: lx + 0.32, y: ly + 0.2, w: lw - 0.5, h: 0.4, fontSize: 16, fontFace: YH, bold: true, color: theme.primary, margin: 0 });
  slide.addText([
    { text: '分类赛: top-5 test 7.3%, 亚军 (冠军 GoogLeNet 6.7%)', options: { bullet: true, breakLine: true } },
    { text: '但单网络对比, VGG 反超 GoogLeNet', options: { bullet: true, breakLine: true } },
    { text: '定位赛: top-5 错误 25.3%, 直接夺冠', options: { bullet: true } }
  ], { x: lx + 0.32, y: ly + 0.72, w: lw - 0.6, h: 1.3, fontSize: 11.5, fontFace: YH, color: theme.primary, paraSpaceAfter: 8, margin: 0 });

  // mini bars: single-net top-5 test error
  slide.addText('单网络 top-5 test error (越低越好)', { x: lx + 0.32, y: ly + 2.45, w: lw - 0.6, h: 0.3, fontSize: 10, fontFace: YH, color: theme.secondary, margin: 0 });
  const bx = lx + 1.55, bmax = 2.0;
  // VGG 7.0
  slide.addShape(pres.shapes.RECTANGLE, { x: bx, y: ly + 2.82, w: bmax * 7.0 / 7.9, h: 0.26, fill: { color: theme.accent }, rectRadius: 0.03 });
  slide.addText('VGG', { x: lx + 0.32, y: ly + 2.8, w: 1.15, h: 0.3, fontSize: 10, fontFace: 'Arial', bold: true, color: theme.primary, align: 'right', valign: 'middle', margin: 0 });
  slide.addText('7.0', { x: bx + bmax * 7.0 / 7.9 + 0.05, y: ly + 2.8, w: 0.6, h: 0.3, fontSize: 10, fontFace: 'Arial', bold: true, color: theme.accent, valign: 'middle', margin: 0 });
  // GoogLeNet 7.9
  slide.addShape(pres.shapes.RECTANGLE, { x: bx, y: ly + 3.2, w: bmax, h: 0.26, fill: { color: theme.secondary }, rectRadius: 0.03 });
  slide.addText('GoogLeNet', { x: lx + 0.15, y: ly + 3.18, w: 1.32, h: 0.3, fontSize: 9, fontFace: 'Arial', color: theme.primary, align: 'right', valign: 'middle', margin: 0 });
  slide.addText('7.9', { x: bx + bmax + 0.05, y: ly + 3.18, w: 0.6, h: 0.3, fontSize: 10, fontFace: 'Arial', color: theme.secondary, valign: 'middle', margin: 0 });

  // Right: feature transfer stat callouts
  const rx = 5.25;
  slide.addText('作为通用特征提取器', { x: rx, y: 1.35, w: 4.35, h: 0.35, fontSize: 16, fontFace: YH, bold: true, color: theme.accent, margin: 0 });
  slide.addText('预训练 VGG + 不微调 + 线性 SVM, 直接迁移到新数据集', { x: rx, y: 1.72, w: 4.35, h: 0.3, fontSize: 10.5, fontFace: YH, color: theme.secondary, margin: 0 });

  const stats = [
    ['89.3', 'VOC-2007 mAP', '此前最好约 82.4'],
    ['85.1', 'Caltech-256 recall', '此前最好 77.6'],
    ['84.0', '动作分类 VOC-2012 mAP', '加入框信息后']
  ];
  let sy = 2.2;
  stats.forEach((s) => {
    slide.addShape(pres.shapes.RECTANGLE, { x: rx, y: sy, w: 4.35, h: 0.82, fill: { color: theme.light }, rectRadius: 0.08, shadow: makeShadow() });
    slide.addText(s[0], { x: rx + 0.2, y: sy, w: 1.25, h: 0.82, fontSize: 30, fontFace: 'Arial', bold: true, color: theme.accent, align: 'center', valign: 'middle', margin: 0 });
    slide.addText(s[1], { x: rx + 1.55, y: sy + 0.13, w: 2.7, h: 0.35, fontSize: 13, fontFace: YH, bold: true, color: theme.primary, valign: 'middle', margin: 0 });
    slide.addText(s[2], { x: rx + 1.55, y: sy + 0.46, w: 2.7, h: 0.3, fontSize: 10, fontFace: YH, color: theme.secondary, valign: 'middle', margin: 0 });
    sy += 0.95;
  });

  // Page badge
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fill: { color: theme.primary } });
  slide.addText('08', { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fontSize: 11, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: 'Arial', bold: true, margin: 0 });
}
module.exports = { createSlide };
