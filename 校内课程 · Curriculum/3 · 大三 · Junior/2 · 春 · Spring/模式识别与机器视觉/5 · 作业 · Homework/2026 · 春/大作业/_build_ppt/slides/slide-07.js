// Slide 07 - Experimental results (bar chart + conclusions)
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };
  const YH = 'Microsoft YaHei';
  const makeShadow = () => ({ type: 'outer', color: '003049', blur: 5, offset: 2, angle: 135, opacity: 0.12 });

  slide.addText('实验结果 -- 深度的胜利', { x: 0.6, y: 0.4, w: 9, h: 0.6, fontSize: 28, fontFace: YH, bold: true, color: theme.primary, margin: 0 });

  // Bar chart: top-1 error across configs
  slide.addChart(pres.charts.BAR, [{
    name: 'top-1 error (%)',
    labels: ['A (11)', 'B (13)', 'C (16)', 'D (16)', 'E (19)'],
    values: [29.6, 28.7, 28.1, 27.0, 27.3]
  }], {
    x: 0.45, y: 1.4, w: 5.6, h: 2.95, barDir: 'col',
    chartColors: [theme.accent],
    chartArea: { fill: { color: 'FFFFFF' } },
    catAxisLabelColor: '003049', catAxisLabelFontFace: 'Arial', catAxisLabelFontSize: 10,
    valAxisLabelColor: '669bbc', valAxisLabelFontSize: 9, valAxisMinVal: 24, valAxisMaxVal: 30,
    valGridLine: { color: 'E6DAC0', size: 0.5 }, catGridLine: { style: 'none' },
    showValue: true, dataLabelPosition: 'outEnd', dataLabelColor: '003049', dataLabelFontFace: 'Arial', dataLabelFontSize: 10, dataLabelFormatCode: '0.0',
    showLegend: false, showTitle: false
  });
  slide.addText('单尺度可比设置 (训练 S=256, 测试 Q=256); 柱子越矮越好', { x: 0.45, y: 4.4, w: 5.6, h: 0.3, fontSize: 9.5, fontFace: YH, color: theme.secondary, align: 'center', margin: 0 });

  // Right: four conclusions
  slide.addText('从结果表读出的四件事', { x: 6.3, y: 1.4, w: 3.35, h: 0.35, fontSize: 14, fontFace: YH, bold: true, color: theme.accent, margin: 0 });
  slide.addText([
    { text: '越深越准: top-1 从 29.6% 一路降到 25.5% (E, 最佳设置)', options: { bullet: true, breakLine: true } },
    { text: '3x3 优于 1x1: 同为 16 层, D 全面优于 C', options: { bullet: true, breakLine: true } },
    { text: 'LRN 无用: A-LRN 反而略差于 A', options: { bullet: true, breakLine: true } },
    { text: '多尺度训练显著有效; 到 19 层后收益开始递减', options: { bullet: true } }
  ], { x: 6.3, y: 1.85, w: 3.35, h: 2.45, fontSize: 12, fontFace: YH, color: theme.primary, paraSpaceAfter: 11, margin: 0 });

  // Bottom-right best-model callout
  slide.addShape(pres.shapes.RECTANGLE, { x: 6.3, y: 4.45, w: 3.35, h: 0.6, fill: { color: theme.primary }, rectRadius: 0.08, shadow: makeShadow() });
  slide.addText([
    { text: '最佳单模型  ', options: { bold: true, color: 'F4A261', fontFace: YH } },
    { text: 'top-1 24.8% / top-5 7.5%', options: { bold: true, color: 'FFFFFF', fontFace: 'Arial' } }
  ], { x: 6.5, y: 4.45, w: 3.05, h: 0.6, fontSize: 12.5, valign: 'middle', margin: 0 });

  // Page badge
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fill: { color: theme.primary } });
  slide.addText('07', { x: 9.3, y: 5.08, w: 0.45, h: 0.45, fontSize: 11, color: 'FFFFFF', align: 'center', valign: 'middle', fontFace: 'Arial', bold: true, margin: 0 });
}
module.exports = { createSlide };
