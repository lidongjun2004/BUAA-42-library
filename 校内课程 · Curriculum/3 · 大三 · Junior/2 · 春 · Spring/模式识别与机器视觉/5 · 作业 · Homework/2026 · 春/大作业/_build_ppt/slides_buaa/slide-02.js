// Slide 02 - BUAA-style Table of Contents (left blue column + right list)
const { YH, EN } = require('./_buaa.js');
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: 'FFFFFF' };

  // Left deep-blue column (~1/3)
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 3.3, h: 5.625, fill: { color: theme.primary } });
  slide.addText('目录', { x: 0.5, y: 1.55, w: 2.5, h: 0.7, fontSize: 36, fontFace: YH, bold: true, color: 'FFFFFF', margin: 0 });
  slide.addShape(pres.shapes.LINE, { x: 0.55, y: 2.32, w: 1.2, h: 0, line: { color: 'FFFFFF', width: 1.5 } });
  slide.addText('CONTENTS', { x: 0.53, y: 2.42, w: 2.5, h: 0.4, fontSize: 13, fontFace: EN, color: 'D6E0F0', charSpacing: 3, margin: 0 });

  const items = [
    ['01', '研究背景与核心问题'],
    ['02', '为什么是 3x3 卷积核'],
    ['03', '网络配置: 从 A 到 E'],
    ['04', '训练与测试策略'],
    ['05', '实验结果: 深度的胜利'],
    ['06', '历史意义与局限']
  ];
  const startY = 0.78, gap = 0.73;
  items.forEach((it, i) => {
    const y = startY + i * gap;
    slide.addShape('parallelogram', { x: 2.88, y: y, w: 0.82, h: 0.54, fill: { color: 'FFFFFF' }, line: { color: theme.secondary, width: 0.75 } });
    slide.addText(it[0], { x: 2.88, y: y, w: 0.82, h: 0.54, fontSize: 17, fontFace: EN, bold: true, color: theme.primary, align: 'center', valign: 'middle', margin: 0 });
    slide.addText(it[1], { x: 4.0, y: y, w: 5.4, h: 0.54, fontSize: 17, fontFace: YH, bold: true, color: theme.primary, valign: 'middle', margin: 0 });
    slide.addShape(pres.shapes.LINE, { x: 4.0, y: y + 0.58, w: 5.3, h: 0, line: { color: 'DCE6F1', width: 0.75 } });
  });

  // page number
  slide.addText('02', { x: 8.95, y: 5.18, w: 0.6, h: 0.32, fontSize: 11, fontFace: EN, bold: true, color: theme.primary, align: 'right', valign: 'middle', margin: 0 });
}
module.exports = { createSlide };
