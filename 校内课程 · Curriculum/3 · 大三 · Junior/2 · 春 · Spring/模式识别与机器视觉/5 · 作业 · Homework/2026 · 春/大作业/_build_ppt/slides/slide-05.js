// Slide 05 - Network configurations A to E (pipeline + table + design points)
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };
  const YH = 'Microsoft YaHei';
  const makeShadow = () => ({ type: 'outer', color: '003049', blur: 4, offset: 1.5, angle: 135, opacity: 0.1 });

  slide.addText('网络配置 -- 从 A 到 E', { x: 0.6, y: 0.35, w: 9, h: 0.55, fontSize: 28, fontFace: YH, bold: true, color: theme.primary, margin: 0 });

  // Pipeline blocks
  const blocks = [
    ['输入', '224x224', theme.secondary, 75],
    ['Block1', 'conv3-64', theme.secondary, 60],
    ['Block2', 'conv3-128', theme.secondary, 45],
    ['Block3', 'conv3-256', theme.secondary, 30],
    ['Block4', 'conv3-512', theme.secondary, 15],
    ['Block5', 'conv3-512', theme.secondary, 0],
    ['FC', '4096->1000', theme.accent, 0]
  ];
  const py = 1.2, ph = 0.92, startX = 0.6, totalW = 9.0, gap = 0.16;
  const bw = (totalW - gap * (blocks.length - 1)) / blocks.length;
  blocks.forEach((b, i) => {
    const x = startX + i * (bw + gap);
    const isFC = (i === blocks.length - 1);
    slide.addShape(pres.shapes.RECTANGLE, { x, y: py, w: bw, h: ph, fill: { color: b[2], transparency: b[3] }, rectRadius: 0.05, shadow: makeShadow() });
    slide.addText(b[0], { x, y: py + 0.14, w: bw, h: 0.3, fontSize: 11.5, fontFace: YH, bold: true, color: isFC ? 'FFFFFF' : theme.primary, align: 'center', margin: 0 });
    slide.addText(b[1], { x, y: py + 0.48, w: bw, h: 0.3, fontSize: 9, fontFace: 'Arial', color: isFC ? 'FFFFFF' : theme.primary, align: 'center', margin: 0 });
    if (i < blocks.length - 1) {
      slide.addText('>', { x: x + bw - 0.04, y: py, w: gap + 0.08, h: ph, fontSize: 13, fontFace: 'Arial', bold: true, color: theme.secondary, align: 'center', valign: 'middle', margin: 0 });
    }
  });
  slide.addText('每经过一次 2x2 maxpool, 空间减半 / 通道翻倍:  224 -> 112 -> 56 -> 28 -> 14 -> 7', { x: 0.6, y: py + ph + 0.1, w: 9, h: 0.3, fontSize: 11, fontFace: YH, color: theme.secondary, align: 'center', margin: 0 });

  // Config table (left-bottom)
  const ty = 3.0;
  const hd = (t) => ({ text: t, options: { fill: { color: theme.primary }, color: 'FFFFFF', bold: true, align: 'center', fontFace: YH, fontSize: 10.5, valign: 'middle' } });
  const lc = (t) => ({ text: t, options: { align: 'left', color: theme.primary, fontFace: YH, fontSize: 9.5, valign: 'middle', fill: { color: 'FFFFFF' } } });
  const cc = (t, hl) => ({ text: t, options: { align: 'center', color: hl ? theme.accent : theme.primary, bold: !!hl, fontFace: 'Arial', fontSize: 10.5, valign: 'middle', fill: { color: 'FFFFFF' } } });
  const tl = (t) => ({ text: t, options: { align: 'left', color: 'FFFFFF', bold: true, fontFace: YH, fontSize: 9.5, valign: 'middle', fill: { color: theme.secondary } } });
  const tc = (t, hl) => ({ text: t, options: { align: 'center', color: hl ? theme.accent : theme.primary, bold: true, fontFace: 'Arial', fontSize: 10.5, valign: 'middle', fill: { color: 'FFFFFF' } } });
  const tbl = [
    [hd('Block / 配置'), hd('A'), hd('B'), hd('C'), hd('D'), hd('E')],
    [lc('Block1 (64)'), cc('1'), cc('2'), cc('2'), cc('2'), cc('2')],
    [lc('Block2 (128)'), cc('1'), cc('2'), cc('2'), cc('2'), cc('2')],
    [lc('Block3 (256)'), cc('2'), cc('2'), cc('3*'), cc('3'), cc('4')],
    [lc('Block4 (512)'), cc('2'), cc('2'), cc('3*'), cc('3'), cc('4')],
    [lc('Block5 (512)'), cc('2'), cc('2'), cc('3*'), cc('3'), cc('4')],
    [tl('权重层数'), tc('11'), tc('13'), tc('16', true), tc('16', true), tc('19', true)]
  ];
  slide.addTable(tbl, { x: 0.6, y: ty, w: 5.6, colW: [1.6, 0.8, 0.8, 0.8, 0.8, 0.8], rowH: 0.3, border: { type: 'solid', pt: 0.5, color: 'D9C9A8' }, valign: 'middle' });

  // Right-bottom: design points + param callout
  const dx = 6.45, dyy = 3.0;
  slide.addText('关键设计', { x: dx, y: dyy, w: 3.2, h: 0.3, fontSize: 13, fontFace: YH, bold: true, color: theme.accent, margin: 0 });
  slide.addText([
    { text: '所有卷积 stride=1, pad=1, 尺寸只由 maxpool 改变', options: { bullet: true, breakLine: true } },
    { text: '共 5 次 maxpool, 分辨率从 224 降到 7', options: { bullet: true, breakLine: true } },
    { text: 'A-LRN 验证 LRN 无用, 之后全部弃用', options: { bullet: true, breakLine: true } },
    { text: 'D = VGG-16, E = VGG-19; C 的 3* 含 1x1 卷积', options: { bullet: true } }
  ], { x: dx, y: dyy + 0.4, w: 3.2, h: 1.45, fontSize: 10.5, fontFace: YH, color: theme.primary, paraSpaceAfter: 7, margin: 0 });

  slide.addShape(pres.shapes.RECTANGLE, { x: dx, y: 4.46, w: 3.15, h: 0.58, fill: { color: theme.primary }, rectRadius: 0.08, shadow: makeShadow() });
  slide.addText([
    { text: '138M ', options: { bold: true, color: 'FFFFFF', fontSize: 17, fontFace: 'Arial' } },
    { text: '参数 (VGG-16), 约 90% 集中在 FC 层', options: { color: 'FFFFFF', fontSize: 10, fontFace: YH } }
  ], { x: dx + 0.2, y: 4.46, w: 2.85, h: 0.58, valign: 'middle', margin: 0 });

  // Page badge
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fill: { color: theme.primary } });
  slide.addText('05', { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fontSize: 11, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: 'Arial', bold: true, margin: 0 });
}
module.exports = { createSlide };
