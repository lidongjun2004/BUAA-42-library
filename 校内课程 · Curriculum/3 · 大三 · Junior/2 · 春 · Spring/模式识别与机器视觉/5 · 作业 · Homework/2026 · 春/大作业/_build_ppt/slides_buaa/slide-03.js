// Slide 03 - Background & Core Question (BUAA style)
const { YH, EN, header, titleBlock, footer } = require('./_buaa.js');
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: 'FFFFFF' };
  header(slide, pres, theme);
  titleBlock(slide, pres, theme, '研究背景与核心问题');

  slide.addText('2014 年的现状', { x: 0.5, y: 1.62, w: 5, h: 0.38, fontSize: 16, fontFace: YH, bold: true, color: theme.secondary, margin: 0 });
  slide.addText([
    { text: '卷积网络已在大规模图像识别上远超传统手工特征', options: { bullet: true, breakLine: true } },
    { text: '但主流架构大多只有约 8 个权重层 (AlexNet / ZFNet / OverFeat)', options: { bullet: true, breakLine: true } },
    { text: '第一层偏爱大卷积核 (11x11 或 7x7) 来获取足够感受野', options: { bullet: true, breakLine: true } },
    { text: '而网络的深度方向, 几乎从未被系统性地探索过', options: { bullet: true } }
  ], { x: 0.5, y: 2.06, w: 5.05, h: 2.0, fontSize: 13, fontFace: YH, color: '404040', paraSpaceAfter: 11, margin: 0 });

  const cx = 5.85, cy = 1.62, cw = 3.65, ch = 2.5;
  slide.addShape(pres.shapes.RECTANGLE, { x: cx, y: cy, w: cw, h: ch, fill: { color: theme.primary } });
  slide.addShape('parallelogram', { x: cx + 0.3, y: cy + 0.3, w: 0.28, h: 0.26, fill: { color: theme.secondary } });
  slide.addText('CORE QUESTION', { x: cx + 0.68, y: cy + 0.27, w: cw - 1.0, h: 0.3, fontSize: 11, fontFace: EN, bold: true, color: 'D6E0F0', charSpacing: 1, valign: 'middle', margin: 0 });
  slide.addText('网络究竟需要多深, 才能充分发挥它的表示能力?', { x: cx + 0.3, y: cy + 0.7, w: cw - 0.6, h: 0.88, fontSize: 18, fontFace: YH, bold: true, color: 'FFFFFF', margin: 0 });
  slide.addText([
    { text: '本文做法  ', options: { bold: true, color: 'FFFFFF' } },
    { text: '控制其它所有变量, 只把深度从 11 层加到 19 层, 卷积核统一用最小的 3x3', options: { color: 'D6E0F0' } }
  ], { x: cx + 0.3, y: cy + 1.66, w: cw - 0.6, h: 0.72, fontSize: 12, fontFace: YH, margin: 0 });

  const by = 4.34;
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: by, w: 9.0, h: 0.6, fill: { color: theme.light } });
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: by, w: 0.1, h: 0.6, fill: { color: theme.accent } });
  slide.addText([
    { text: '一句话  ', options: { bold: true, color: theme.accent, fontFace: YH } },
    { text: '把 "深度" 本身当成唯一变量, 干净地量化它对识别精度的贡献', options: { color: theme.primary, fontFace: YH } }
  ], { x: 0.78, y: by, w: 8.5, h: 0.6, fontSize: 13, valign: 'middle', margin: 0 });

  footer(slide, pres, theme, 3);
}
module.exports = { createSlide };
