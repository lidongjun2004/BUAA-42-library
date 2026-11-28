// Shared BUAA-style components for all content slides.
const YH = 'Microsoft YaHei';
const EN = 'Arial';

// Right-top school name lockup + thin divider line under the header.
function header(slide, pres, theme) {
  slide.addText([
    { text: '北京航空航天大学  ', options: { fontFace: YH, bold: true, color: theme.primary, fontSize: 11 } },
    { text: 'BEIHANG UNIVERSITY', options: { fontFace: EN, color: theme.secondary, fontSize: 8 } }
  ], { x: 5.0, y: 0.26, w: 4.6, h: 0.3, align: 'right', valign: 'middle', margin: 0 });
  slide.addShape(pres.shapes.LINE, { x: 0.5, y: 0.7, w: 9.0, h: 0, line: { color: theme.secondary, width: 1 } });
}

// Left-top parallelogram accent block + section title.
function titleBlock(slide, pres, theme, title) {
  slide.addShape('parallelogram', { x: 0.5, y: 0.95, w: 0.46, h: 0.44, fill: { color: theme.primary } });
  slide.addText(title, { x: 1.08, y: 0.9, w: 8.2, h: 0.52, fontSize: 23, fontFace: YH, bold: true, color: theme.primary, valign: 'middle', margin: 0 });
}

// Bottom-left motto + bottom-right page number.
function footer(slide, pres, theme, pageNum) {
  slide.addText('德才兼备  知行合一', { x: 0.5, y: 5.18, w: 3.2, h: 0.32, fontSize: 11, fontFace: YH, color: 'A6A6A6', valign: 'middle', margin: 0 });
  slide.addText(String(pageNum).padStart(2, '0'), { x: 8.95, y: 5.18, w: 0.6, h: 0.32, fontSize: 11, fontFace: EN, bold: true, color: theme.primary, align: 'right', valign: 'middle', margin: 0 });
}

module.exports = { YH, EN, header, titleBlock, footer };
