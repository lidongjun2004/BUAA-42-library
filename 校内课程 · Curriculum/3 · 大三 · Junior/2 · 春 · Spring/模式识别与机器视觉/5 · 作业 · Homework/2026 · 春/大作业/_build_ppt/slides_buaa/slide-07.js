// Slide 07 - Results (BUAA style)
const { YH, EN, header, titleBlock, footer } = require('./_buaa.js');
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: 'FFFFFF' };
  header(slide, pres, theme);
  titleBlock(slide, pres, theme, '实验结果 -- 深度的胜利');

  slide.addChart(pres.charts.BAR, [{ name: 'top-1 error (%)', labels: ['A (11)', 'B (13)', 'C (16)', 'D (16)', 'E (19)'], values: [29.6, 28.7, 28.1, 27.0, 27.3] }], {
    x: 0.45, y: 1.62, w: 5.55, h: 2.82, barDir: 'col',
    chartColors: [theme.primary],
    chartArea: { fill: { color: 'FFFFFF' } },
    catAxisLabelColor: '404040', catAxisLabelFontFace: EN, catAxisLabelFontSize: 10,
    valAxisLabelColor: '808080', valAxisLabelFontSize: 9, valAxisMinVal: 24, valAxisMaxVal: 30,
    valGridLine: { color: 'E6E6E6', size: 0.5 }, catGridLine: { style: 'none' },
    showValue: true, dataLabelPosition: 'outEnd', dataLabelColor: theme.primary, dataLabelFontFace: EN, dataLabelFontSize: 10, dataLabelFormatCode: '0.0',
    showLegend: false, showTitle: false
  });
  slide.addText('单尺度可比设置 (训练 S=256, 测试 Q=256); 柱子越矮越好', { x: 0.45, y: 4.5, w: 5.55, h: 0.3, fontSize: 9.5, fontFace: YH, color: '808080', align: 'center', margin: 0 });

  slide.addText('从结果表读出的四件事', { x: 6.2, y: 1.62, w: 3.4, h: 0.35, fontSize: 14, fontFace: YH, bold: true, color: theme.secondary, margin: 0 });
  slide.addText([
    { text: '越深越准: top-1 从 29.6% 一路降到 25.5% (E 最佳)', options: { bullet: true, breakLine: true } },
    { text: '3x3 优于 1x1: 同为 16 层, D 全面优于 C', options: { bullet: true, breakLine: true } },
    { text: 'LRN 无用: A-LRN 反而略差于 A', options: { bullet: true, breakLine: true } },
    { text: '多尺度训练显著有效; 19 层后收益递减', options: { bullet: true } }
  ], { x: 6.2, y: 2.05, w: 3.4, h: 2.2, fontSize: 11.5, fontFace: YH, color: '404040', paraSpaceAfter: 10, margin: 0 });

  slide.addShape(pres.shapes.RECTANGLE, { x: 6.2, y: 4.32, w: 3.4, h: 0.58, fill: { color: theme.primary } });
  slide.addText([
    { text: '最佳单模型  ', options: { bold: true, color: 'FFE08A', fontFace: YH } },
    { text: 'top-1 24.8% / top-5 7.5%', options: { bold: true, color: 'FFFFFF', fontFace: EN } }
  ], { x: 6.4, y: 4.32, w: 3.05, h: 0.58, fontSize: 12, valign: 'middle', margin: 0 });

  footer(slide, pres, theme, 7);
}
module.exports = { createSlide };
