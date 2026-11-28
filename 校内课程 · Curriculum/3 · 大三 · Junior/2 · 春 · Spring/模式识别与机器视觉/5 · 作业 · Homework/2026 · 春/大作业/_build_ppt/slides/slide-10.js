// Slide 10 - Summary / Closing (dark, key takeaways)
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.primary };
  const YH = 'Microsoft YaHei';

  slide.addText('总结  SUMMARY', { x: 0.7, y: 0.55, w: 8, h: 0.4, fontSize: 14, fontFace: 'Arial', bold: true, color: 'F4A261', charSpacing: 3, margin: 0 });

  // Big quote
  slide.addText('不需要复杂的拓扑, 只需要足够的深度和规范的构建块', {
    x: 0.7, y: 1.05, w: 8.6, h: 1.2, fontSize: 27, fontFace: YH, bold: true, color: 'FFFFFF', margin: 0
  });

  // 2x2 takeaways
  const items = [
    ['深度是核心杠杆', '越深越准, top-1 从 29.6% 降到 24.8%'],
    ['3x3 小核堆叠', '更深, 更省参数, 更强非线性'],
    ['简洁即力量', '成为之后多年的通用 backbone'],
    ['承上启下', '直接启发 ResNet / Inception 等更深网络']
  ];
  const colX = [0.7, 5.05], cw = 4.25, startY = 2.55, gapY = 1.0;
  items.forEach((it, i) => {
    const c = i % 2, r = Math.floor(i / 2);
    const x = colX[c], y = startY + r * gapY;
    slide.addShape(pres.shapes.OVAL, { x, y: y + 0.05, w: 0.34, h: 0.34, fill: { color: theme.accent } });
    slide.addText(String(i + 1), { x, y: y + 0.05, w: 0.34, h: 0.34, fontSize: 13, fontFace: 'Arial', bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', margin: 0 });
    slide.addText(it[0], { x: x + 0.5, y: y - 0.04, w: cw - 0.5, h: 0.4, fontSize: 16, fontFace: YH, bold: true, color: 'FFFFFF', margin: 0 });
    slide.addText(it[1], { x: x + 0.5, y: y + 0.36, w: cw - 0.5, h: 0.4, fontSize: 11.5, fontFace: YH, color: '669bbc', margin: 0 });
  });

  // Footer
  slide.addShape(pres.shapes.LINE, { x: 0.7, y: 4.78, w: 8.6, h: 0, line: { color: '669bbc', width: 0.75 } });
  slide.addText('谢谢观看   |   模式识别与机器视觉  课程论文讲解', { x: 0.7, y: 4.88, w: 7.5, h: 0.4, fontSize: 12, fontFace: YH, color: '669bbc', margin: 0 });

  // Page badge
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fill: { color: theme.accent } });
  slide.addText('10', { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fontSize: 11, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: 'Arial', bold: true, margin: 0 });
}
module.exports = { createSlide };
