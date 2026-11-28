// Slide 05 - Configurations A to E (BUAA style)
const { YH, EN, header, titleBlock, footer } = require('./_buaa.js');
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: 'FFFFFF' };
  header(slide, pres, theme);
  titleBlock(slide, pres, theme, '网络配置 -- 从 A 到 E');

  const blocks = [
    ['输入', '224x224', 45],
    ['Block1', 'conv3-64', 36],
    ['Block2', 'conv3-128', 27],
    ['Block3', 'conv3-256', 18],
    ['Block4', 'conv3-512', 9],
    ['Block5', 'conv3-512', 0]
  ];
  const py = 1.6, ph = 0.8, startX = 0.5, gap = 0.14;
  const bw = (9.0 - gap * blocks.length) / (blocks.length + 1);
  blocks.forEach((b, i) => {
    const x = startX + i * (bw + gap);
    slide.addShape(pres.shapes.RECTANGLE, { x, y: py, w: bw, h: ph, fill: { color: theme.secondary, transparency: b[2] } });
    slide.addText(b[0], { x, y: py + 0.12, w: bw, h: 0.28, fontSize: 10.5, fontFace: YH, bold: true, color: 'FFFFFF', align: 'center', margin: 0 });
    slide.addText(b[1], { x, y: py + 0.44, w: bw, h: 0.26, fontSize: 8.5, fontFace: EN, color: 'FFFFFF', align: 'center', margin: 0 });
    slide.addText('>', { x: x + bw - 0.02, y: py, w: gap + 0.06, h: ph, fontSize: 12, fontFace: EN, bold: true, color: theme.secondary, align: 'center', valign: 'middle', margin: 0 });
  });
  // FC block (accent)
  const fcx = startX + blocks.length * (bw + gap);
  slide.addShape(pres.shapes.RECTANGLE, { x: fcx, y: py, w: bw, h: ph, fill: { color: theme.primary } });
  slide.addText('FC', { x: fcx, y: py + 0.12, w: bw, h: 0.28, fontSize: 10.5, fontFace: YH, bold: true, color: 'FFFFFF', align: 'center', margin: 0 });
  slide.addText('4096->1000', { x: fcx, y: py + 0.44, w: bw, h: 0.26, fontSize: 8, fontFace: EN, color: 'FFFFFF', align: 'center', margin: 0 });

  slide.addText('每经过一次 2x2 maxpool, 空间减半 / 通道翻倍:  224 -> 112 -> 56 -> 28 -> 14 -> 7', { x: 0.5, y: py + ph + 0.1, w: 9, h: 0.3, fontSize: 10.5, fontFace: YH, color: '595959', align: 'center', margin: 0 });

  // config table
  const ty = 2.92;
  const hd = (t) => ({ text: t, options: { fill: { color: theme.primary }, color: 'FFFFFF', bold: true, align: 'center', fontFace: YH, fontSize: 10, valign: 'middle' } });
  const lc = (t) => ({ text: t, options: { align: 'left', color: '404040', fontFace: YH, fontSize: 9.5, valign: 'middle', fill: { color: 'FFFFFF' } } });
  const cc = (t, hl) => ({ text: t, options: { align: 'center', color: hl ? theme.accent : '404040', bold: !!hl, fontFace: EN, fontSize: 10, valign: 'middle', fill: { color: 'FFFFFF' } } });
  const tl = (t) => ({ text: t, options: { align: 'left', color: 'FFFFFF', bold: true, fontFace: YH, fontSize: 9.5, valign: 'middle', fill: { color: theme.secondary } } });
  const tc = (t, hl) => ({ text: t, options: { align: 'center', color: hl ? theme.accent : theme.primary, bold: true, fontFace: EN, fontSize: 10, valign: 'middle', fill: { color: 'DCE6F1' } } });
  const tbl = [
    [hd('Block / 配置'), hd('A'), hd('B'), hd('C'), hd('D'), hd('E')],
    [lc('Block1 (64)'), cc('1'), cc('2'), cc('2'), cc('2'), cc('2')],
    [lc('Block2 (128)'), cc('1'), cc('2'), cc('2'), cc('2'), cc('2')],
    [lc('Block3 (256)'), cc('2'), cc('2'), cc('3*'), cc('3'), cc('4')],
    [lc('Block4 (512)'), cc('2'), cc('2'), cc('3*'), cc('3'), cc('4')],
    [lc('Block5 (512)'), cc('2'), cc('2'), cc('3*'), cc('3'), cc('4')],
    [tl('权重层数'), tc('11'), tc('13'), tc('16', true), tc('16', true), tc('19', true)]
  ];
  slide.addTable(tbl, { x: 0.5, y: ty, w: 5.5, colW: [1.55, 0.79, 0.79, 0.79, 0.79, 0.79], rowH: 0.29, border: { type: 'solid', pt: 0.5, color: 'B8CCE4' }, valign: 'middle' });

  // right design points + callout
  const dx = 6.35, dyy = 2.92;
  slide.addText('关键设计', { x: dx, y: dyy, w: 3.2, h: 0.3, fontSize: 13, fontFace: YH, bold: true, color: theme.secondary, margin: 0 });
  slide.addText([
    { text: '所有卷积 stride=1, pad=1, 尺寸只由 maxpool 改变', options: { bullet: true, breakLine: true } },
    { text: '共 5 次 maxpool, 分辨率从 224 降到 7', options: { bullet: true, breakLine: true } },
    { text: 'A-LRN 验证 LRN 无用, 之后全部弃用', options: { bullet: true, breakLine: true } },
    { text: 'D = VGG-16, E = VGG-19; C 的 3* 含 1x1 卷积', options: { bullet: true } }
  ], { x: dx, y: dyy + 0.38, w: 3.25, h: 1.4, fontSize: 10.5, fontFace: YH, color: '404040', paraSpaceAfter: 6, margin: 0 });

  slide.addShape(pres.shapes.RECTANGLE, { x: dx, y: 4.34, w: 3.2, h: 0.56, fill: { color: theme.primary } });
  slide.addText([
    { text: '138M ', options: { bold: true, color: 'FFFFFF', fontSize: 16, fontFace: EN } },
    { text: '参数 (VGG-16), 约 90% 在 FC 层', options: { color: 'D6E0F0', fontSize: 10, fontFace: YH } }
  ], { x: dx + 0.2, y: 4.34, w: 2.9, h: 0.56, valign: 'middle', margin: 0 });

  footer(slide, pres, theme, 5);
}
module.exports = { createSlide };
