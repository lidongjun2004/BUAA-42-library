// Slide 01 - Cover (Asymmetric Left-Right)
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };
  const YH = 'Microsoft YaHei';

  // Left accent band
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.22, h: 5.625, fill: { color: theme.accent } });

  // Kicker
  slide.addText('ICLR 2015      arXiv: 1409.1556', {
    x: 0.7, y: 0.6, w: 5.3, h: 0.35, fontSize: 13, fontFace: 'Arial',
    color: theme.accent, bold: true, charSpacing: 1, margin: 0
  });

  // Main title
  slide.addText('VGGNet', {
    x: 0.62, y: 1.0, w: 5.5, h: 1.2, fontSize: 78, fontFace: 'Arial',
    color: theme.primary, bold: true, margin: 0
  });

  // Chinese subtitle
  slide.addText('用极小卷积核把网络做深', {
    x: 0.7, y: 2.28, w: 5.4, h: 0.55, fontSize: 24, fontFace: YH,
    color: theme.primary, bold: true, margin: 0
  });
  slide.addText('-- 深度卷积网络的设计哲学与实验验证', {
    x: 0.7, y: 2.85, w: 5.4, h: 0.4, fontSize: 15, fontFace: YH,
    color: theme.secondary, margin: 0
  });

  // English paper name + authors
  slide.addText('Very Deep Convolutional Networks for Large-Scale Image Recognition', {
    x: 0.7, y: 3.42, w: 5.3, h: 0.4, fontSize: 11.5, fontFace: 'Arial', italic: true,
    color: theme.secondary, margin: 0
  });
  slide.addText('Karen Simonyan  &  Andrew Zisserman', {
    x: 0.7, y: 3.92, w: 5.35, h: 0.3, fontSize: 11.5, fontFace: 'Arial',
    color: theme.secondary, margin: 0
  });
  slide.addText('Visual Geometry Group, University of Oxford', {
    x: 0.7, y: 4.2, w: 5.35, h: 0.3, fontSize: 11, fontFace: 'Arial',
    color: theme.secondary, margin: 0
  });

  // Footer
  slide.addShape(pres.shapes.LINE, { x: 0.7, y: 4.72, w: 5.0, h: 0, line: { color: theme.secondary, width: 0.75 } });
  slide.addText([
    { text: '模式识别与机器视觉   课程论文讲解', options: { fontFace: YH, bold: true, color: theme.primary } },
    { text: '        约 7 分钟', options: { fontFace: YH, color: theme.secondary } }
  ], { x: 0.7, y: 4.82, w: 5.4, h: 0.4, fontSize: 12, margin: 0 });

  // Right panel - stacked layers motif (inverted pyramid: output on top)
  const px = 6.25, py = 0.55, pw = 3.4, ph = 4.5;
  slide.addShape(pres.shapes.RECTANGLE, { x: px, y: py, w: pw, h: ph, fill: { color: theme.primary }, rectRadius: 0.12 });
  slide.addText('THE DEEPER, THE BETTER', {
    x: px + 0.2, y: py + 0.25, w: pw - 0.4, h: 0.35, fontSize: 12, fontFace: 'Arial',
    color: 'FFFFFF', bold: true, align: 'center', charSpacing: 1, margin: 0
  });

  const n = 12, topY = 1.4, bandH = 0.17, gap = 0.1, wTop = 1.0, wBot = 2.7;
  for (let i = 0; i < n; i++) {
    const w = wTop + (wBot - wTop) * (i / (n - 1));
    const x = px + (pw - w) / 2;
    const y = topY + i * (bandH + gap);
    const isOut = (i === 0);
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w, h: bandH,
      fill: { color: isOut ? theme.accent : theme.secondary, transparency: isOut ? 0 : (8 + i * 4) },
      rectRadius: 0.02
    });
  }
  slide.addText('11  ->  19  weight layers', {
    x: px + 0.2, y: py + ph - 0.48, w: pw - 0.4, h: 0.35, fontSize: 12.5, fontFace: 'Arial',
    color: 'FFFFFF', bold: true, align: 'center', margin: 0
  });
}
module.exports = { createSlide };
