#!/usr/bin/env python3
"""Markdown -> print-academic A4 HTML (figures, TOC, MathJax) for the pdf skill."""
import os
import re
import sys

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

CSS = """
@page { size: A4 portrait; }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html, body { margin: 0; padding: 0; background: #fff; color: #16202e;
  font-family: "PingFang SC", "Songti SC", "Noto Sans CJK SC", "Microsoft YaHei", Arial, sans-serif;
  font-size: 10.4pt; line-height: 1.75; }
h1 { font-size: 20pt; text-align: center; margin: 0 0 2mm; letter-spacing: .5px; }
.subtitle { text-align: center; color: #5a6b80; font-size: 10.5pt; margin-bottom: 9mm; }
h2 { font-size: 14.5pt; margin: 9mm 0 3.5mm; padding-bottom: 1.6mm;
     border-bottom: 1.2pt solid #2f6f8f; color: #1d4257; }
h3 { font-size: 11.8pt; margin: 6mm 0 2.5mm; color: #24566e; }
h4 { font-size: 10.6pt; margin: 4.5mm 0 2mm; color: #3c5a6b; }
p { margin: 0 0 2.6mm; text-align: justify; }
ul, ol { margin: 0 0 3mm; padding-left: 7mm; }
li { margin-bottom: 1.1mm; }
code { font-family: "SF Mono", Menlo, Consolas, monospace; font-size: 9pt;
  background: #f2f5f8; padding: 0.4mm 1.1mm; border-radius: 2px; color: #24455c; }
pre { background: #f6f8fa; border: .5pt solid #d9e0e6; border-left: 2.4pt solid #2f6f8f;
  padding: 2.6mm 3.2mm; margin: 0 0 3.4mm; overflow-x: hidden; }
pre code { background: none; padding: 0; font-size: 8.4pt; line-height: 1.5; color: #22303c; }
table { width: 100%; border-collapse: collapse; font-size: 8.8pt; margin: 0 0 3.6mm;
  table-layout: auto; }
th { background: #eaf1f6; border: .5pt solid #b9c9d4; padding: 1.5mm 2mm; text-align: left;
  color: #1d4257; }
td { border: .45pt solid #d3dce3; padding: 1.4mm 2mm; vertical-align: top; }
tr:nth-child(even) td { background: #fafcfd; }
figure { margin: 4.5mm 0 5.5mm; text-align: center; page-break-inside: avoid; }
figure img { max-width: 100%; max-height: 178mm; border: .5pt solid #d8e0ea; }
figcaption { margin-top: 1.8mm; font-size: 8.5pt; color: #5a6b80; text-align: center; }
blockquote { margin: 0 0 3mm; padding: 1.6mm 3.4mm; border-left: 2.4pt solid #9db8c8;
  background: #f5f8fa; color: #33475a; font-size: 9.8pt; }
.toc { page-break-after: always; }
.toc h2 { border: none; margin-top: 0; margin-bottom: 3mm; }
.toc ol { list-style: none; padding-left: 0; }
.toc ol li { margin-bottom: 0.4mm; font-size: 9pt; line-height: 1.32; }
.toc ol ol { padding-left: 6mm; font-size: 8.5pt; color: #45596b; }
.toc a { color: #1d4257; text-decoration: none; }
.toc a:hover { text-decoration: underline; }
.abstract { border: .6pt solid #cddbe4; background: #f7fafc; padding: 3.4mm 4.2mm;
  margin-bottom: 6mm; }
.abstract h2 { margin: 0 0 2.4mm; font-size: 12pt; border: none; }
.abstract p { margin-bottom: 1.8mm; }
.meta { text-align: center; color: #64778a; font-size: 9.4pt; margin-bottom: 7mm; }
.kw { color: #0f5c73; font-weight: 600; }
.note { font-size: 9.2pt; color: #5a6b80; }
hr { border: none; border-top: .5pt solid #d8e0ea; margin: 6mm 0; }
"""


def slug(text, seen):
    base = re.sub(r"[^\w一-鿿]+", "-", text.strip()).strip("-") or "sec"
    key, i = base, 1
    while key in seen:
        i += 1
        key = f"{base}-{i}"
    seen.add(key)
    return key


def main(src, dst):
    raw = open(src, encoding="utf-8").read()

    # --- protect LaTeX from markdown parsing (a bare `_` pair would turn
    #     into italics, and `\\_` / `<` / `&` would be mangled) -----------
    blocks, inlines = [], []

    def grab_block(m):
        blocks.append(m.group(1))
        return "@@MB%d@@" % (len(blocks) - 1)

    def grab_inline(m):
        inlines.append(m.group(1))
        return "@@MI%d@@" % (len(inlines) - 1)

    raw = re.sub(r"\$\$(.+?)\$\$", grab_block, raw, flags=re.S)
    raw = re.sub(r"(?<!\$)\$([^\$\n]+?)\$(?!\$)", grab_inline, raw)

    md = MarkdownIt("commonmark", {"html": True, "breaks": False}).enable("table")
    body = md.render(raw)

    body = re.sub(r"@@MB(\d+)@@",
                  lambda m: "$$" + blocks[int(m.group(1))] + "$$", body)
    body = re.sub(r"@@MI(\d+)@@",
                  lambda m: "$" + inlines[int(m.group(1))] + "$", body)

    soup = BeautifulSoup(body, "html.parser")

    seen = set()
    for h in soup.find_all(["h1", "h2", "h3", "h4"]):
        h["id"] = slug(h.get_text(), seen)

    # wrap every standalone image into <figure><figcaption>
    for img in list(soup.find_all("img")):
        cap = (img.get("alt") or "").strip()
        fig = soup.new_tag("figure")
        img.replace_with(fig)
        fig.append(img)
        if cap:
            fc = soup.new_tag("figcaption")
            fc.string = cap
            fig.append(fc)

    # strip orphan markdown markers
    from bs4 import NavigableString
    for node in soup.find_all(string=True):
        if isinstance(node, NavigableString) and "**" in str(node):
            node.replace_with(str(node).replace("**", ""))

    # build a clickable table of contents from h2/h3
    parts, inner = [], []
    toc = soup.new_tag("div", **{"class": "toc"})
    h = soup.new_tag("h2")
    h.string = "目录"
    toc.append(h)
    ol = soup.new_tag("ol")
    cur = None
    for el in soup.find_all(["h2", "h3"]):
        if el.name == "h2" and el.get_text().strip() == "目录":
            continue
        txt = el.get_text().strip()
        li = soup.new_tag("li")
        a = soup.new_tag("a", href="#" + el["id"])
        a.string = txt
        li.append(a)
        if el.name == "h3":
            inner.append(li)
        else:
            if inner and cur is not None:
                sub = soup.new_tag("ol")
                for x in inner:
                    sub.append(x.extract())
                cur.append(sub)
            inner = []
            ol.append(li)
            cur = li
    if inner and cur is not None:
        sub = soup.new_tag("ol")
        for x in inner:
            sub.append(x.extract())
        cur.append(sub)
    toc.append(ol)

    wrapper = soup.new_tag("div")
    for el in list(soup.contents):
        wrapper.append(el.extract())
    body_el = wrapper

    # insert the toc right before the first h2
    first_h2 = body_el.find("h2")
    toc_html = str(toc)
    if first_h2 is not None:
        first_h2.insert_before(toc)
    else:
        body_el.append(toc)

    rendered = body_el.decode()
    head_extra = """
<script>
window.MathJax = { tex: { inlineMath: [['$','$']], displayMath: [['$$','$$']] },
  svg: { fontCache: 'global' }, chtml: { scale: 0.94 } };
</script>
<script id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
"""
    html = (
        "<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\"/>\n"
        f"<title>{os.path.basename(src)}</title>\n"
        f"<style>{CSS}</style>\n{head_extra}\n</head>\n<body>\n{rendered}\n</body>\n</html>\n"
    )
    open(dst, "w", encoding="utf-8").write(html)
    print(f"wrote {dst}  ({len(html)} bytes, {seen.__len__()} anchors)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
