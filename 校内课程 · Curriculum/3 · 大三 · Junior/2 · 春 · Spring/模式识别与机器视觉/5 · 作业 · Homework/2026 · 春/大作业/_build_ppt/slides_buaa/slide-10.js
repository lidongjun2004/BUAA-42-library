// Slide 10 - Summary / Closing (BUAA style, deep blue)
const { YH, EN } = require('./_buaa.js');
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.primary };

  slide.addText('总结  SUMMARY', { x: 0.6, y: 0.55, w: 8, h: 0.4, fontSize: 14, fontFace: EN, bold: true, color: 'FFE08A', charSpacing: 3, margin: 0 });
  slide.addText('不需要复杂的拓扑, 只需要足够的深度和规范的构建块', { x: 0.6, y: 1.05, w: 8.9, h: 1.1, fontSize: 26, fontFace: YH, bold: true, color: 'FFFFFF', margin: 0 });

  const items = [
    ['深度是核心杠杆', '越深越准, top-1 从 29.6% 降到 24.8%'],
    ['3x3 小核堆叠', '更深, 更省参数, 更强非线性'],
    ['简洁即力量', '成为之后多年的通用 backbone'],
    ['承上启下', '直接启发 ResNet / Inception 等更深网络']
  ];
  const colX = [0.6, 5.05], cw = 4.3, startY = 2.5, gapY = 0.96;
  items.forEach((it, i) => {
    const c = i % 2, r = Math.floor(i / 2);
    const x = colX[c], y = startY + r * gapY;
    slide.addShape(pres.shapes.OVAL, { x, y: y + 0.04, w: 0.34, h: 0.34, fill: { color: theme.secondary } });
    slide.addText(String(i + 1), { x, y: y + 0.04, w: 0.34, h: 0.34, fontSize: 13, fontFace: EN, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', margin: 0 });
    slide.addText(it[0], { x: x + 0.5, y: y - 0.04, w: cw - 0.5, h: 0.4, fontSize: 16, fontFace: YH, bold: true, color: 'FFFFFF', margin: 0 });
    slide.addText(it[1], { x: x + 0.5, y: y + 0.36, w: cw - 0.5, h: 0.4, fontSize: 11.5, fontFace: YH, color: 'C6D4EA', margin: 0 });
  });

  slide.addShape(pres.shapes.LINE, { x: 0.6, y: 4.72, w: 8.8, h: 0, line: { color: '4F81BD', width: 0.75 } });
  slide.addText('谢谢观看    德才兼备  知行合一    模式识别与机器视觉 课程论文', { x: 0.6, y: 4.84, w: 8.2, h: 0.4, fontSize: 11.5, fontFace: YH, color: 'C6D4EA', margin: 0 });
  slide.addText('10', { x: 8.95, y: 4.84, w: 0.6, h: 0.4, fontSize: 11, fontFace: EN, bold: true, color: 'FFFFFF', align: 'right', valign: 'middle', margin: 0 });
}
module.exports = { createSlide };
