// Slide 02 - Table of Contents (Two-column card grid)
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };
  const YH = 'Microsoft YaHei';
  const makeShadow = () => ({ type: 'outer', color: '003049', blur: 5, offset: 2, angle: 135, opacity: 0.12 });

  // Title
  slide.addText('目录', { x: 0.6, y: 0.5, w: 4, h: 0.7, fontSize: 34, fontFace: YH, bold: true, color: theme.primary, margin: 0 });
  slide.addText('CONTENTS', { x: 0.63, y: 1.18, w: 4, h: 0.4, fontSize: 13, fontFace: 'Arial', color: theme.accent, bold: true, charSpacing: 3, margin: 0 });

  const items = [
    ['01', '研究背景与核心问题', '网络到底要多深'],
    ['02', '为什么是 3x3 卷积核', '感受野等价 + 更深更省'],
    ['03', '网络配置: 从 A 到 E', '11 层逐步加到 19 层'],
    ['04', '训练与测试策略', '预训练初始化 / 多尺度'],
    ['05', '实验结果: 深度的胜利', '越深越准的实验铁证'],
    ['06', '历史意义与局限', '奠基者与未竟之路']
  ];

  const colX = [0.6, 5.15], cardW = 4.25, cardH = 1.0, startY = 1.85, gapY = 1.18;
  items.forEach((it, i) => {
    const c = i % 2, r = Math.floor(i / 2);
    const x = colX[c], y = startY + r * gapY;
    slide.addShape(pres.shapes.RECTANGLE, { x, y, w: cardW, h: cardH, fill: { color: theme.light }, rectRadius: 0.08, shadow: makeShadow() });
    slide.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.1, h: cardH, fill: { color: theme.accent } });
    slide.addText(it[0], { x: x + 0.22, y: y + 0.1, w: 0.85, h: 0.8, fontSize: 30, fontFace: 'Arial', bold: true, color: theme.accent, valign: 'middle', margin: 0 });
    slide.addText(it[1], { x: x + 1.1, y: y + 0.16, w: cardW - 1.25, h: 0.42, fontSize: 15.5, fontFace: YH, bold: true, color: theme.primary, valign: 'middle', margin: 0 });
    slide.addText(it[2], { x: x + 1.1, y: y + 0.56, w: cardW - 1.25, h: 0.34, fontSize: 11.5, fontFace: YH, color: theme.secondary, valign: 'middle', margin: 0 });
  });

  // Page badge
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.05, w: 0.45, h: 0.45, fill: { color: theme.primary } });
  slide.addText('02', { x: 9.3, y: 5.05, w: 0.45, h: 0.45, fontSize: 11, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: 'Arial', bold: true, margin: 0 });
}
module.exports = { createSlide };
