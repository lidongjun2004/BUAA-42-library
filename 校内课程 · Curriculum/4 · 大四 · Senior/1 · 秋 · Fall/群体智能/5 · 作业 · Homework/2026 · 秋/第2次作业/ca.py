#!/usr/bin/env python3
"""Cellular automaton engine compatible with Golly's rule notation.

* 2D outer-totalistic rules written as "B3/S23" (Moore neighbourhood, 8 cells)
* 1D elementary (Wolfram) rules written as "W110"
* RLE read/write so every pattern here can be opened in Golly as-is
"""
import re
import numpy as np

# --------------------------------------------------------------------------
# 2D  B/S rules
# --------------------------------------------------------------------------
def parse_bs(rule):
    m = re.fullmatch(r"B(\d*)/S(\d*)", rule.strip(), re.I)
    if not m:
        raise ValueError("bad rule: %s" % rule)
    birth = np.zeros(9, bool)
    surv = np.zeros(9, bool)
    for c in m.group(1):
        birth[int(c)] = True
    for c in m.group(2):
        surv[int(c)] = True
    return birth, surv


def neighbours(grid, wrap=True):
    """8-neighbour count. wrap=True -> torus, else dead cells outside."""
    g = grid.astype(np.uint8)
    if wrap:
        n = np.zeros_like(g, dtype=np.uint8)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy or dx:
                    n += np.roll(np.roll(g, dy, 0), dx, 1)
        return n
    p = np.pad(g, 1)
    n = (p[:-2, :-2] + p[:-2, 1:-1] + p[:-2, 2:] +
         p[1:-1, :-2] + p[1:-1, 2:] +
         p[2:, :-2] + p[2:, 1:-1] + p[2:, 2:])
    return n


def step(grid, rule, wrap=True):
    birth, surv = rule if isinstance(rule, tuple) else parse_bs(rule)
    n = neighbours(grid, wrap)
    return np.where(grid, surv[n], birth[n])


def run(grid, rule, gens, wrap=True, hook=None):
    rule = parse_bs(rule) if isinstance(rule, str) else rule
    for t in range(gens):
        if hook is not None:
            hook(t, grid)
        grid = step(grid, rule, wrap)
    if hook is not None:
        hook(gens, grid)
    return grid


# ---- metrics ---------------------------------------------------------------
def density(g):
    return float(g.mean())


def activity(a, b):
    """fraction of cells that changed state between two generations"""
    return float((a != b).mean())


def block_entropy(g, k=3):
    """Shannon entropy (bits) of k x k block patterns, a proxy for disorder."""
    h, w = g.shape
    h -= h % k
    w -= w % k
    blocks = g[:h, :w].reshape(h // k, k, w // k, k).transpose(0, 2, 1, 3).reshape(-1, k * k)
    weights = 1 << np.arange(k * k)
    codes = (blocks.astype(np.int64) * weights).sum(1)
    _, cnt = np.unique(codes, return_counts=True)
    p = cnt / cnt.sum()
    return float(-(p * np.log2(p)).sum())


def bounding_box(g):
    ys, xs = np.nonzero(g)
    if len(ys) == 0:
        return None
    return ys.min(), xs.min(), ys.max() + 1, xs.max() + 1


# --------------------------------------------------------------------------
# 1D elementary rules
# --------------------------------------------------------------------------
def run1d(row, rule_no, gens, wrap=True):
    table = np.array([(rule_no >> i) & 1 for i in range(8)], dtype=np.uint8)
    rows = [row.astype(np.uint8)]
    for _ in range(gens):
        r = rows[-1]
        if wrap:
            l, rr = np.roll(r, 1), np.roll(r, -1)
        else:
            l = np.concatenate([[0], r[:-1]])
            rr = np.concatenate([r[1:], [0]])
        rows.append(table[(l << 2) | (r << 1) | rr])
    return np.array(rows)


# --------------------------------------------------------------------------
# RLE  (Golly native format)
# --------------------------------------------------------------------------
def read_rle(text):
    rule = "B3/S23"
    body = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("x"):
            m = re.search(r"rule\s*=\s*(\S+)", line)   # keep ":T128,128" bounded-grid suffix
            if m:
                rule = m.group(1)
            continue
        body.append(line)
    body = "".join(body).split("!")[0]
    cells = []
    x = y = 0
    for cnt, tag in re.findall(r"(\d*)([bo$])", body):
        n = int(cnt) if cnt else 1
        if tag == "b":
            x += n
        elif tag == "o":
            cells += [(y, x + i) for i in range(n)]
            x += n
        else:
            y += n
            x = 0
    if not cells:
        return np.zeros((1, 1), bool), rule
    h = max(c[0] for c in cells) + 1
    w = max(c[1] for c in cells) + 1
    g = np.zeros((h, w), bool)
    for yy, xx in cells:
        g[yy, xx] = True
    return g, rule


def write_rle(g, rule="B3/S23", comment=None):
    bb = bounding_box(g)
    if bb is None:
        return "x = 0, y = 0, rule = %s\n!\n" % rule
    y0, x0, y1, x1 = bb
    sub = g[y0:y1, x0:x1]
    out = []
    if comment:
        for c in comment.splitlines():
            out.append("#C " + c)
    out.append("x = %d, y = %d, rule = %s" % (x1 - x0, y1 - y0, rule))
    items = []
    blank_rows = 0
    for row in sub:
        if not row.any():
            blank_rows += 1
            continue
        if items:
            items.append((blank_rows + 1, "$"))
        blank_rows = 0
        # run-length encode row, trailing dead cells dropped
        last = np.nonzero(row)[0].max() + 1
        r = row[:last]
        i = 0
        while i < last:
            j = i
            while j < last and r[j] == r[i]:
                j += 1
            items.append((j - i, "o" if r[i] else "b"))
            i = j
    # wrap at run boundaries only: Golly rejects a line break inside "<count><tag>"
    toks = [("%d%s" % (n, t)) if n > 1 else t for n, t in items] + ["!"]
    line = ""
    for tok in toks:
        if len(line) + len(tok) > 70:
            out.append(line)
            line = ""
        line += tok
    out.append(line)
    return "\n".join(out) + "\n"


def place(canvas, pat, y, x):
    h, w = pat.shape
    canvas[y:y + h, x:x + w] |= pat.astype(bool)
    return canvas


def rot90(pat, k=1):
    return np.rot90(pat, k)


# a few named Life patterns (standard RLE from the LifeWiki)
PATTERNS = {
    "glider": "x = 3, y = 3, rule = B3/S23\nbo$2bo$3o!",
    "r_pentomino": "x = 3, y = 3, rule = B3/S23\nb2o$2o$bo!",
    "diehard": "x = 8, y = 3, rule = B3/S23\n6bo$2o$bo3b3o!",
    "acorn": "x = 7, y = 3, rule = B3/S23\nbo$3bo$2o2b3o!",
    "eater1": "x = 4, y = 4, rule = B3/S23\n2o$obo$2bo$2b2o!",
    "lwss": "x = 5, y = 4, rule = B3/S23\nbo2bo$o$o3bo$4o!",
    "gosper_gun": ("x = 36, y = 9, rule = B3/S23\n"
                   "24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o$2o8bo3bob2o"
                   "4bobo$10bo5bo7bo$11bo3bo$12b2o!"),
}


def pattern(name):
    return read_rle(PATTERNS[name])[0]
