#!/usr/bin/env python3
"""Render the evolution video (1280x720, H.264) from the same patterns used in the report."""
import json
import os
import sys

import numpy as np
import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont

import ca

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "演化过程视频.mp4")
W, H, FPS = 1280, 720, 30
BG = (14, 18, 32)
FG = (244, 211, 94)
TXT = (235, 238, 245)
SUB = (160, 170, 190)


def font(size):
    for p in ["/System/Library/Fonts/PingFang.ttc", "/System/Library/Fonts/STHeiti Light.ttc",
              "/System/Library/Fonts/Hiragino Sans GB.ttc", "/System/Library/Fonts/Supplemental/Songti.ttc"]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

F_TITLE, F_H, F_B, F_S = font(44), font(30), font(24), font(19)


def grid_img(g, scale, fg=FG, bg=BG):
    a = np.zeros(g.shape + (3,), np.uint8)
    a[...] = bg
    a[g.astype(bool)] = fg
    im = Image.fromarray(a)
    return im.resize((g.shape[1] * scale, g.shape[0] * scale), Image.NEAREST)


class Writer:
    def __init__(self, path):
        self.w = imageio.get_writer(path, fps=FPS, codec="libx264", quality=8,
                                    pixelformat="yuv420p", macro_block_size=16)
        self.n = 0

    def add(self, im, repeat=1):
        for _ in range(repeat):
            self.w.append_data(np.asarray(im.convert("RGB")))
            self.n += 1

    def close(self):
        self.w.close()
        print("frames:", self.n, "=> %.1f s" % (self.n / FPS))


def canvas(title=None, sub=None):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    if title:
        d.text((40, 22), title, font=F_H, fill=TXT)
    if sub:
        d.text((40, 66), sub, font=F_S, fill=SUB)
    return im, d


def card(wr, title, lines, seconds=3.0):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((80, 200), title, font=F_TITLE, fill=FG)
    y = 290
    for ln in lines:
        d.text((80, y), ln, font=F_B, fill=TXT)
        y += 42
    wr.add(im, int(seconds * FPS))


def fade_hold(wr, im, seconds=1.0):
    wr.add(im, int(seconds * FPS))


# ---------------------------------------------------------------- scenes
def scene_soup(wr):
    N = 128
    rng = np.random.default_rng(2026)
    g = rng.random((N, N)) < 0.35
    scale = 4
    for t in range(0, 401):
        if t % 2 == 0:
            im, d = canvas("1. 经典生命游戏 B3/S23：随机初始分布的演化",
                           "128×128 环面，初始密度 0.35。混沌期 → 密度快速下降 → 静物与振荡器构成的“灰烬”")
            im.paste(grid_img(g, scale), (40, 110))
            d.text((620, 130), "第 %d 代" % t, font=F_H, fill=FG)
            d.text((620, 185), "密度 %.3f" % g.mean(), font=F_B, fill=TXT)
            d.text((620, 230), "活跃度 %.3f" % (0 if t == 0 else ca.activity(prev, g)), font=F_B, fill=TXT)
            d.text((620, 300), "观察：\n· 前几十代几乎所有细胞都在变化\n· 局部结构（方块、信标、闪烁子）固化后不再变\n· 偶有滑翔机在环面上游走", font=F_S, fill=SUB)
            wr.add(im, 1 if t > 60 else 2)
        prev = g
        g = ca.step(g, "B3/S23", True)
    fade_hold(wr, im, 1.5)


RULES = [("Life", "B3/S23", 0.35), ("HighLife", "B36/S23", 0.35), ("Seeds", "B2/S", 0.08),
         ("Day & Night", "B3678/S34678", 0.35), ("Diamoeba", "B35678/S5678", 0.50),
         ("Anneal", "B4678/S35678", 0.50), ("34 Life", "B34/S34", 0.15),
         ("Replicator", "B1357/S1357", 0.35), ("Maze", "B3/S12345", 0.10)]


def scene_rules(wr):
    N = 96
    rng = np.random.default_rng(2026)
    base = rng.random((N, N))
    grids = [base < p0 for _, _, p0 in RULES]
    rules = [ca.parse_bs(r) for _, r, _ in RULES]
    scale = 2
    for t in range(0, 301):
        if t % 2 == 0:
            im, d = canvas("2. 同一噪声场、九种演化规则：规则决定“相”",
                           "每格 96×96 环面；规则写法 B（出生邻居数）/S（存活邻居数），与 Golly 一致")
            for i in range(9):
                r, c = divmod(i, 3)
                x, y = 40 + c * 230, 105 + r * 205
                im.paste(grid_img(grids[i], scale), (x, y))
                d.text((x, y + 194 - 6), "%s  %s" % (RULES[i][0], RULES[i][1]), font=F_S, fill=TXT)
            d.text((740, 120), "第 %d 代" % t, font=F_H, fill=FG)
            d.text((740, 180), "Life / HighLife：很快凝固成静物与振荡器\n"
                               "Seeds：没有存活规则，永远爆炸式扩散\n"
                               "Day & Night：黑白对称，边界持续翻滚\n"
                               "Diamoeba / Anneal：像液滴/退火一样收缩成团\n"
                               "34 Life：振荡器密集、长期活跃\n"
                               "Replicator：任何图案都自我复制\n"
                               "Maze：长成迷宫状静态走廊", font=F_S, fill=SUB)
            wr.add(im, 2 if t < 40 else 1)
        grids = [ca.step(g, r, True) for g, r in zip(grids, rules)]
    fade_hold(wr, im, 1.5)


def scene_density(wr):
    N = 128
    ps = [0.10, 0.35, 0.70]
    rng = np.random.default_rng(11)
    base = rng.random((N, N))
    grids = [base < p for p in ps]
    scale = 3
    for t in range(0, 301):
        if t % 2 == 0:
            im, d = canvas("3. 同一规则 B3/S23、三种初始密度：殊途同归",
                           "初始密度 0.10 / 0.35 / 0.70；过稀和过密都会先经历一次“塌缩”，最终密度都落到 0.03 附近")
            for i, g in enumerate(grids):
                x = 40 + i * 410
                im.paste(grid_img(g, scale), (x, 110))
                d.text((x, 500), "p0 = %.2f   当前密度 %.3f" % (ps[i], g.mean()), font=F_B, fill=TXT)
            d.text((40, 560), "第 %d 代" % t, font=F_H, fill=FG)
            d.text((300, 568), "p0=0.70 的格子在第 1 代几乎全部因“过度拥挤”死亡，再从残留碎片重新生长；p0=0.10 则因“孤立”先大量死亡。",
                   font=F_S, fill=SUB)
            wr.add(im, 2 if t < 30 else 1)
        grids = [ca.step(g, "B3/S23", True) for g in grids]
    fade_hold(wr, im, 1.5)


def scene_rpent(wr):
    S = 260
    g = np.zeros((S, S), bool)
    ca.place(g, ca.pattern("r_pentomino"), S // 2, S // 2)
    scale = 2
    hist = []
    for t in range(0, 1200):
        if t % 4 == 0:
            im, d = canvas("4. 初始条件的另一端：只有 5 个细胞的 R 五格骨牌",
                           "260×260 死边界平面。5 个细胞要经过 1103 代才能稳定，最终留下 116 个细胞（含飞走的 6 架滑翔机）")
            im.paste(grid_img(g, scale), (40, 110))
            d.text((600, 130), "第 %d 代" % t, font=F_H, fill=FG)
            d.text((600, 185), "细胞数 %d" % g.sum(), font=F_B, fill=TXT)
            hist.append(int(g.sum()))
            # tiny population plot
            d.rectangle((600, 300, 1230, 520), outline=SUB)
            if len(hist) > 1:
                mx = max(hist) or 1
                pts = [(600 + 630 * i / 300, 520 - 220 * h / mx) for i, h in enumerate(hist)]
                d.line(pts, fill=FG, width=2)
            d.text((600, 525), "细胞数随时间变化（峰值 %d）" % max(hist), font=F_S, fill=SUB)
            d.text((600, 580), "类比：一粒种子长成一片生态系统，\n中途不断“喷出”滑翔机（信息外泄），最后固化。", font=F_S, fill=SUB)
            wr.add(im, 1)
        g = ca.step(g, "B3/S23", False)
    fade_hold(wr, im, 1.5)


def scene_gun_eater(wr, res):
    e = res["C"]["eater"]
    gun = ca.pattern("gosper_gun")
    eater = ca.pattern("eater1")
    ors = {}
    for k in range(4):
        r = np.rot90(eater, k)
        ors["rot%d" % k] = r
        ors["rot%d_flip" % k] = r[:, ::-1]
    S = 100
    g = np.zeros((S, S), bool)
    ca.place(g, gun, 10, 10)
    ca.place(g, ors[e["orientation"]], e["y"], e["x"])
    scale = 6
    for t in range(0, 241):
        im, d = canvas("5. 数理逻辑的积木：高斯帕滑翔机枪 + 吞噬器",
                       "枪每 30 代发射一架滑翔机（信号源）；吞噬器把到达的滑翔机干净吸收（信号终端）")
        im.paste(grid_img(g[:100, :100], scale), (40, 110))
        d.text((680, 130), "第 %d 代" % t, font=F_H, fill=FG)
        d.text((680, 185), "细胞数 %d" % g.sum(), font=F_B, fill=TXT)
        d.text((680, 260), "滑翔机 = 1 bit 信号，沿对角线以 c/4 传播\n枪周期 30 代 → 一条固定频率的信号流\n吞噬器 (eater 1) 的位置和朝向由程序穷举搜索得到：\n  朝向 %s，位置 (%d, %d)\n\n这两个零件是在生命游戏里搭逻辑门的最小积木。"
               % (e["orientation"], e["y"], e["x"]), font=F_S, fill=SUB)
        wr.add(im, 1)
        g = ca.step(g, "B3/S23", False)
    fade_hold(wr, im, 1.5)


def scene_not_gate(wr, res):
    dy, dx = res["C"]["not_gate"]["offset"]
    gun = ca.pattern("gosper_gun")
    gunB = np.rot90(gun, 1)
    S = 230
    scale = 2
    for with_input in (False, True):
        g = np.zeros((S, S), bool)
        ca.place(g, gun, 8, 8)
        if with_input:
            ca.place(g, gunB, 150 + dy, 8 + dx)
        T = 520            # gliders reach x = 120 at about t = 378 (speed c/4)
        for t in range(0, T + 1):
            if t % 2 == 0:
                im, d = canvas("6. 用生命游戏实现一个非门（NOT）",
                               "左上的枪 = 固定信号；左下的枪 = 输入；右侧虚线 = 输出。输入信号与固定信号在交叉点相撞湮灭")
                im.paste(grid_img(g, scale), (40, 110))
                d.line((40 + 120 * scale, 110, 40 + 120 * scale, 110 + S * scale), fill=(178, 58, 72), width=2)
                d.text((560, 130), "第 %d 代" % t, font=F_H, fill=FG)
                d.text((560, 190), ("输入 = 1（下方枪在发射）" if with_input else "输入 = 0（没有下方的枪）"), font=F_B, fill=TXT)
                out_hit = g[:, 120:].any()
                d.text((560, 235), "输出端是否有滑翔机：%s" % ("有" if out_hit else "无"), font=F_B,
                       fill=FG if out_hit else SUB)
                d.text((560, 320), "真值表（实验计数，700 代内到达输出区的滑翔机数）：\n   输入 0 → 输出 %d 架滑翔机（= 1）\n   输入 1 → 输出 %d 架滑翔机（= 0）\n\n两架滑翔机以 90° 对撞时，只有特定相位/偏移会完全湮灭，\n其他相位会留下碎片或互相穿过；\n偏移 (dy, dx) = (%d, %d) 由程序穷举得到。"
                       % (res["C"]["not_gate"]["output_without_input"], res["C"]["not_gate"]["output_with_input"], dy, dx),
                       font=F_S, fill=SUB)
                wr.add(im, 1)
            g = ca.step(g, "B3/S23", False)
        fade_hold(wr, im, 1.5)


def scene_1d(wr):
    Wc = 320
    scale = 4
    rows_vis = 140
    rng = np.random.default_rng(5)
    for rule, title, sub, start in [
        (110, "7. 一维规则 110：与生命游戏“计算等价”的最小系统",
         "每个细胞只看左右邻居，8 条查表规则。Cook (2004) 证明它图灵完备——与生命游戏在计算能力上等价", (rng.random(Wc) < 0.5)),
        (184, "8. 一维规则 184 = 单车道交通流模型",
         "1 = 有车，0 = 空位。车前方空则前进一格。密度 0.7 时出现向后传播的“堵车波”", (rng.random(Wc) < 0.70)),
    ]:
        table = np.array([(rule >> i) & 1 for i in range(8)], np.uint8)
        row = start.astype(np.uint8)
        buf = np.zeros((rows_vis, Wc), np.uint8)
        for t in range(260):
            buf = np.roll(buf, -1, 0)
            buf[-1] = row
            im, d = canvas(title, sub)
            im.paste(grid_img(buf, scale), (0, 110))
            d.text((40, 680), "时间 t = %d（时间向下，新一行在最下方）" % t, font=F_S, fill=TXT)
            if rule == 184:
                moves = int((row & ~np.roll(row, -1)).sum())
                d.text((700, 680), "本步前进的车数 %d / 车辆总数 %d" % (moves, row.sum()), font=F_S, fill=TXT)
            wr.add(im, 1)
            l, r = np.roll(row, 1), np.roll(row, -1)
            row = table[(l << 2) | (row << 1) | r]
        fade_hold(wr, im, 1.5)


def main():
    res = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))
    wr = Writer(OUT)
    card(wr, "第二次群智作业：生命游戏的规则与初始条件探究",
         ["23371100  李东骏", "", "内容：",
          "1–3  经典规则的演化、九种规则对比、三种初始密度",
          "4    R 五格骨牌：5 个细胞的 1103 代",
          "5–6  滑翔机枪 + 吞噬器，以及一个可工作的非门",
          "7–8  一维规则 110 / 184：计算等价与交通流"], 4.0)
    scene_soup(wr)
    scene_rules(wr)
    scene_density(wr)
    scene_rpent(wr)
    scene_gun_eater(wr, res)
    scene_not_gate(wr, res)
    scene_1d(wr)
    card(wr, "小结", ["规则（B/S）决定系统处于哪个“相”：凝固、周期、混沌或复杂；",
                     "初始条件决定走到哪个具体终态，但统计量（终态密度）对初值不敏感；",
                     "B3/S23 这一条局部规则足以搭出逻辑门，和规则 110、图灵机计算等价。",
                     "", "所有图案文件（.rle）可直接用 Golly 打开复现。"], 4.0)
    wr.close()


if __name__ == "__main__":
    main()
