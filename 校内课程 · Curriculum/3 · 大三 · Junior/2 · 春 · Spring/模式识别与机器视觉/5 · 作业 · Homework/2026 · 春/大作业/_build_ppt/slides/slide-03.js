// Slide 03 - Background & Core Question (Two-column + takeaway)
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };
  const YH = 'Microsoft YaHei';
  const makeShadow = () => ({ type: 'outer', color: '003049', blur: 5, offset: 2, angle: 135, opacity: 0.12 });

  slide.addText('研究背景与核心问题', { x: 0.6, y: 0.4, w: 8.5, h: 0.6, fontSize: 28, fontFace: YH, bold: true, color: theme.primary, margin: 0 });

  // Left: 2014 status
  slide.addText('2014 年的现状', { x: 0.6, y: 1.25, w: 5, h: 0.4, fontSize: 17, fontFace: YH, bold: true, color: theme.accent, margin: 0 });
  slide.addText([
    { text: '卷积网络已在大规模图像识别上远超传统手工特征', options: { bullet: true, breakLine: true } },
    { text: '但主流架构大多只有约 8 个权重层 (AlexNet / ZFNet / OverFeat)', options: { bullet: true, breakLine: true } },
    { text: '第一层偏爱大卷积核 (11x11 或 7x7) 来获取足够感受野', options: { bullet: true, breakLine: true } },
    { text: '而网络的深度方向, 几乎从未被系统性地探索过', options: { bullet: true } }
  ], { x: 0.6, y: 1.75, w: 5.05, h: 2.4, fontSize: 13.5, fontFace: YH, color: theme.primary, paraSpaceAfter: 12, margin: 0 });

  // Right: core question card
  const cx = 5.95, cy = 1.25, cw = 3.65, ch = 2.9;
  slide.addShape(pres.shapes.RECTANGLE, { x: cx, y: cy, w: cw, h: ch, fill: { color: theme.primary }, rectRadius: 0.1, shadow: makeShadow() });
  slide.addText('CORE QUESTION', { x: cx + 0.3, y: cy + 0.28, w: cw - 0.6, h: 0.3, fontSize: 12, fontFace: 'Arial', bold: true, color: theme.secondary, charSpacing: 2, margin: 0 });
  slide.addText('网络究竟需要多深, 才能充分发挥它的表示能力?', { x: cx + 0.3, y: cy + 0.62, w: cw - 0.6, h: 1.15, fontSize: 19, fontFace: YH, bold: true, color: 'FFFFFF', margin: 0 });
  slide.addText([
    { text: '本文做法   ', options: { bold: true, color: 'F4A261' } },
    { text: '控制其他所有变量, 只让深度从 11 层增加到 19 层, 并把卷积核统一缩到最小的 3x3', options: { color: 'FFFFFF' } }
  ], { x: cx + 0.3, y: cy + 1.92, w: cw - 0.6, h: 0.88, fontSize: 12, fontFace: YH, margin: 0 });

  // Bottom takeaway
  const by = 4.42;
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: by, w: 9.0, h: 0.6, fill: { color: theme.light }, rectRadius: 0.06, shadow: makeShadow() });
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: by, w: 0.1, h: 0.6, fill: { color: theme.accent } });
  slide.addText([
    { text: '一句话   ', options: { bold: true, color: theme.accent, fontFace: YH } },
    { text: '把 "深度" 本身当成唯一变量, 干净地量化它对识别精度的贡献', options: { color: theme.primary, fontFace: YH } }
  ], { x: 0.85, y: by, w: 8.5, h: 0.6, fontSize: 13.5, valign: 'middle', margin: 0 });

  // Page badge
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fill: { color: theme.primary } });
  slide.addText('03', { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fontSize: 11, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: 'Arial', bold: true, margin: 0 });
}
module.exports = { createSlide };
