from pptx import Presentation

EMU = 914400.0
p = Presentation('slides/output/VGGNet-paper-7min.pptx')
SW, SH = p.slide_width / EMU, p.slide_height / EMU
print(f'slide size: {SW:.3f} x {SH:.3f} inch')


def inch(e):
    return None if e is None else e / EMU


def walk(shapes, depth=0):
    out = []
    for sh in shapes:
        out.append(sh)
        if sh.shape_type == 6:  # group
            out.extend(walk(sh.shapes, depth + 1))
    return out


for idx, slide in enumerate(p.slides, 1):
    print(f'\n===== Slide {idx} =====')
    texts = []
    oob = []
    for sh in slide.shapes:
        l, t, w, h = inch(sh.left), inch(sh.top), inch(sh.width), inch(sh.height)
        if None not in (l, t, w, h):
            r, b = l + w, t + h
            if l < -0.03 or t < -0.03 or r > 10.03 or b > 5.64:
                label = ''
                if sh.has_text_frame and sh.text_frame.text.strip():
                    label = sh.text_frame.text.strip().replace('\n', '/')[:30]
                oob.append(f'    OOB: x={l:.2f} y={t:.2f} w={w:.2f} h={h:.2f} r={r:.2f} b={b:.2f}  {label}')
        # collect text
        if sh.has_text_frame and sh.text_frame.text.strip():
            texts.append(sh.text_frame.text.strip().replace('\n', '/'))
        if sh.has_table:
            tb = sh.table
            cells = []
            for row in tb.rows:
                cells.append(','.join(c.text.strip() for c in row.cells))
            texts.append('TABLE[ ' + ' ; '.join(cells) + ' ]')
        if sh.has_chart:
            ch = sh.chart
            try:
                cats = list(ch.plots[0].categories)
                vals = list(ch.plots[0].series[0].values)
                texts.append(f'CHART{cats}={vals}')
            except Exception as e:
                texts.append(f'CHART(err {e})')
    for line in oob:
        print(line)
    if not oob:
        print('  (no out-of-bounds shapes)')
    print('  TEXT:', ' | '.join(texts))
