// Slide 01 - BUAA-style Cover
const { YH, EN } = require('./_buaa.js');
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: 'FFFFFF' };

  // Top deep-blue band (~71%)
  const bandH = 4.0;
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: bandH, fill: { color: theme.primary } });

  // School lockup (top center, white)
  slide.addText([
    { text: '北京航空航天大学    ', options: { fontFace: YH, bold: true, color: 'FFFFFF', fontSize: 15 } },
    { text: 'BEIHANG UNIVERSITY', options: { fontFace: EN, color: 'D6E0F0', fontSize: 10 } }
  ], { x: 1.0, y: 0.52, w: 8, h: 0.4, align: 'center', valign: 'middle', margin: 0 });

  // Main title
  slide.addText('VGGNet', { x: 1, y: 1.25, w: 8, h: 1.0, fontSize: 58, fontFace: EN, bold: true, color: 'FFFFFF', align: 'center', margin: 0 });
  // CN subtitle
  slide.addText('用极小卷积核把网络做深', { x: 1, y: 2.32, w: 8, h: 0.5, fontSize: 22, fontFace: YH, bold: true, color: 'FFFFFF', align: 'center', margin: 0 });
  // White deco line
  slide.addShape(pres.shapes.LINE, { x: 3.6, y: 2.98, w: 2.8, h: 0, line: { color: 'FFFFFF', width: 1 } });
  // English paper name
  slide.addText('Very Deep Convolutional Networks for Large-Scale Image Recognition', { x: 1, y: 3.08, w: 8, h: 0.4, fontSize: 11, fontFace: EN, italic: true, color: 'D6E0F0', align: 'center', margin: 0 });

  // White date/course label straddling the blue-white boundary
  slide.addShape(pres.shapes.RECTANGLE, { x: 3.0, y: 3.78, w: 4.0, h: 0.44, fill: { color: 'FFFFFF' }, line: { color: theme.secondary, width: 0.75 } });
  slide.addText('模式识别与机器视觉  课程论文讲解', { x: 3.0, y: 3.78, w: 4.0, h: 0.44, fontSize: 12, fontFace: YH, bold: true, color: theme.primary, align: 'center', valign: 'middle', margin: 0 });

  // Two parallelogram info blocks in the bottom white area
  slide.addShape('parallelogram', { x: 2.05, y: 4.5, w: 2.5, h: 0.58, fill: { color: theme.primary } });
  slide.addText('汇报人: Lee', { x: 2.05, y: 4.5, w: 2.5, h: 0.58, fontSize: 13, fontFace: YH, color: 'FFFFFF', align: 'center', valign: 'middle', margin: 0 });
  slide.addShape('parallelogram', { x: 5.45, y: 4.5, w: 2.5, h: 0.58, fill: { color: theme.secondary } });
  slide.addText('arXiv: 1409.1556', { x: 5.45, y: 4.5, w: 2.5, h: 0.58, fontSize: 12.5, fontFace: EN, color: 'FFFFFF', align: 'center', valign: 'middle', margin: 0 });
}
module.exports = { createSlide };
