// Slide 08 - Benchmarks & transfer (BUAA style)
const { YH, EN, header, titleBlock, footer } = require('./_buaa.js');
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: 'FFFFFF' };
  header(slide, pres, theme);
  titleBlock(slide, pres, theme, '横向对比与特征迁移');

  // left card: ILSVRC
  const lx = 0.5, ly = 1.62, lw = 4.4, lh = 3.32;
  slide.addShape(pres.shapes.RECTANGLE, { x: lx, y: ly, w: lw, h: lh, fill: { color: theme.light } });
  slide.addShape(pres.shapes.RECTANGLE, { x: lx, y: ly, w: 0.1, h: lh, fill: { color: theme.primary } });
  slide.addShape('parallelogram', { x: lx + 0.32, y: ly + 0.24, w: 0.3, h: 0.28, fill: { color: theme.primary } });
  slide.addText('ILSVRC-2014 战绩', { x: lx + 0.74, y: ly + 0.2, w: lw - 1.0, h: 0.4, fontSize: 15, fontFace: YH, bold: true, color: theme.primary, valign: 'middle', margin: 0 });
  slide.addText([
    { text: '分类赛: top-5 test 7.3%, 亚军 (冠军 GoogLeNet 6.7%)', options: { bullet: true, breakLine: true } },
    { text: '但单网络对比, VGG 反超 GoogLeNet', options: { bullet: true, breakLine: true } },
    { text: '定位赛: top-5 错误 25.3%, 直接夺冠', options: { bullet: true } }
  ], { x: lx + 0.34, y: ly + 0.72, w: lw - 0.6, h: 1.2, fontSize: 11, fontFace: YH, color: '333333', paraSpaceAfter: 7, margin: 0 });

  slide.addText('单网络 top-5 test error (越低越好)', { x: lx + 0.34, y: ly + 2.18, w: lw - 0.6, h: 0.28, fontSize: 9.5, fontFace: YH, color: theme.secondary, margin: 0 });
  const bx = lx + 1.5, bmax = 1.95;
  slide.addShape(pres.shapes.RECTANGLE, { x: bx, y: ly + 2.5, w: bmax * 7.0 / 7.9, h: 0.24, fill: { color: theme.primary } });
  slide.addText('VGG', { x: lx + 0.34, y: ly + 2.48, w: 1.1, h: 0.28, fontSize: 9.5, fontFace: EN, bold: true, color: theme.primary, align: 'right', valign: 'middle', margin: 0 });
  slide.addText('7.0', { x: bx + bmax * 7.0 / 7.9 + 0.05, y: ly + 2.48, w: 0.5, h: 0.28, fontSize: 9.5, fontFace: EN, bold: true, color: theme.primary, valign: 'middle', margin: 0 });
  slide.addShape(pres.shapes.RECTANGLE, { x: bx, y: ly + 2.84, w: bmax, h: 0.24, fill: { color: theme.secondary } });
  slide.addText('GoogLeNet', { x: lx + 0.2, y: ly + 2.82, w: 1.24, h: 0.28, fontSize: 8.5, fontFace: EN, color: '404040', align: 'right', valign: 'middle', margin: 0 });
  slide.addText('7.9', { x: bx + bmax + 0.05, y: ly + 2.82, w: 0.5, h: 0.28, fontSize: 9.5, fontFace: EN, color: theme.secondary, valign: 'middle', margin: 0 });

  // right stat cards
  const rx = 5.25;
  slide.addText('作为通用特征提取器', { x: rx, y: 1.62, w: 4.4, h: 0.35, fontSize: 15, fontFace: YH, bold: true, color: theme.secondary, margin: 0 });
  slide.addText('预训练 + 不微调 + 线性 SVM, 直接迁移到新数据集', { x: rx, y: 1.99, w: 4.4, h: 0.3, fontSize: 10, fontFace: YH, color: '595959', margin: 0 });
  const stats = [
    ['89.3', 'VOC-2007 mAP', '此前最好约 82.4'],
    ['85.1', 'Caltech-256 recall', '此前最好 77.6'],
    ['84.0', '动作分类 VOC-2012', '加入框信息后']
  ];
  let sy = 2.42;
  stats.forEach((s) => {
    slide.addShape(pres.shapes.RECTANGLE, { x: rx, y: sy, w: 4.35, h: 0.78, fill: { color: theme.light } });
    slide.addShape(pres.shapes.RECTANGLE, { x: rx, y: sy, w: 0.08, h: 0.78, fill: { color: theme.primary } });
    slide.addText(s[0], { x: rx + 0.2, y: sy, w: 1.25, h: 0.78, fontSize: 28, fontFace: EN, bold: true, color: theme.primary, align: 'center', valign: 'middle', margin: 0 });
    slide.addText(s[1], { x: rx + 1.55, y: sy + 0.12, w: 2.7, h: 0.34, fontSize: 12.5, fontFace: YH, bold: true, color: '333333', valign: 'middle', margin: 0 });
    slide.addText(s[2], { x: rx + 1.55, y: sy + 0.44, w: 2.7, h: 0.3, fontSize: 9.5, fontFace: YH, color: '808080', valign: 'middle', margin: 0 });
    sy += 0.92;
  });

  footer(slide, pres, theme, 8);
}
module.exports = { createSlide };
