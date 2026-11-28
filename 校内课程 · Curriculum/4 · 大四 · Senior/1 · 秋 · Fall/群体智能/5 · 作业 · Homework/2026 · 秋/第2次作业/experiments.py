#!/usr/bin/env python3
"""All quantitative experiments for the Golly / Game-of-Life report.

Run:  python experiments.py [A|B|C|D|all]
Outputs: figs/*.png, patterns/*.rle (Golly-loadable), results.json
"""
import json
import os
import sys
import time

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.ndimage import label as cc_label

import ca

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figs")
PAT = os.path.join(HERE, "patterns")
RES_PATH = os.path.join(HERE, "results.json")
os.makedirs(FIG, exist_ok=True)
os.makedirs(PAT, exist_ok=True)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                     "axes.spines.top": False, "axes.spines.right": False})
CMAP = ListedColormap(["#ffffff", "#1f3a5f"])
CMAP_DARK = ListedColormap(["#0b1020", "#f4d35e"])


BGOLLY = "/Applications/Golly/bgolly"


def bgolly_population(rle_path, gens):
    """population at every generation 0..gens, computed by Golly's bgolly"""
    import subprocess
    out = subprocess.run([BGOLLY, "-m", str(gens), "-i", "1", rle_path],
                         capture_output=True, text=True, check=True).stdout
    pops = {}
    for line in out.splitlines():
        if ":" in line:
            a, b = line.split(":")
            try:
                pops[int(a.replace(",", ""))] = int(b.replace(",", ""))
            except ValueError:
                pass
    cur = int(ca.read_rle(open(rle_path).read())[0].sum())
    out = []
    for t in range(gens + 1):
        cur = pops.get(t, cur)      # bgolly prints every generation; forward-fill just in case
        out.append(cur)
    return out


def bgolly_run(rle_path, gens, rule=None):
    """grid after gens generations as computed by Golly (RLE round-trip)"""
    import subprocess
    import tempfile
    tmp = tempfile.NamedTemporaryFile(suffix=".rle", delete=False).name
    cmd = [BGOLLY, "-q", "-q", "-m", str(gens), "-o", tmp]
    if rule:
        cmd += ["-r", rule]
    subprocess.run(cmd + [rle_path], capture_output=True, text=True, check=True)
    g, _ = ca.read_rle(open(tmp).read())
    os.unlink(tmp)
    return g


def load_res():
    if os.path.exists(RES_PATH):
        return json.load(open(RES_PATH, encoding="utf-8"))
    return {}


def save_res(res):
    json.dump(res, open(RES_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def save_rle(name, grid, rule="B3/S23", comment=None):
    open(os.path.join(PAT, name + ".rle"), "w").write(ca.write_rle(grid, rule, comment))


def show(ax, g, cmap=CMAP, title=None):
    ax.imshow(g, cmap=cmap, interpolation="nearest", vmin=0, vmax=1)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_linewidth(0.4)
    if title:
        ax.set_title(title, fontsize=8, loc="left")


# ============================================================================
# A. same initial soup, nine rules
# ============================================================================
RULES = [
    ("Life", "B3/S23", 0.35),
    ("HighLife", "B36/S23", 0.35),
    ("Seeds", "B2/S", 0.08),
    ("Day & Night", "B3678/S34678", 0.35),
    ("Diamoeba", "B35678/S5678", 0.50),
    ("Anneal", "B4678/S35678", 0.50),
    ("34 Life", "B34/S34", 0.15),
    ("Replicator", "B1357/S1357", 0.35),
    ("Maze", "B3/S12345", 0.10),
]
SNAP_T = [0, 5, 20, 100, 400]


def exp_A(res):
    N, T = 128, 400
    rng = np.random.default_rng(2026)
    base = rng.random((N, N))          # same noise field for every rule
    out = {}
    fig, axes = plt.subplots(len(RULES), len(SNAP_T), figsize=(7.2, 1.45 * len(RULES)))
    for i, (name, rule, p0) in enumerate(RULES):
        g = base < p0
        save_rle("A_soup_%s" % name.replace(" ", "").replace("&", ""), g, rule,
                 "random soup, p0=%.2f, %dx%d torus in the report" % (p0, N, N))
        dens, act, ent = [], [], []
        prev = g
        snaps = {}
        for t in range(T + 1):
            if t in SNAP_T:
                snaps[t] = g.copy()
            dens.append(ca.density(g))
            ent.append(ca.block_entropy(g))
            if t > 0:
                act.append(ca.activity(prev, g))
            prev = g
            g = ca.step(g, rule, wrap=True)
        # damage spreading: flip the centre cell, same rule, 150 gens
        g0 = base < p0
        g1 = g0.copy()
        g1[N // 2, N // 2] ^= True
        ham = []
        for t in range(151):
            diff = g0 != g1
            ham.append(int(diff.sum()))
            g0 = ca.step(g0, rule, True)
            g1 = ca.step(g1, rule, True)
        out[name] = {"rule": rule, "p0": p0,
                     "density": dens, "activity": act, "entropy": ent,
                     "hamming": ham,
                     "final_density": float(np.mean(dens[-50:])),
                     "final_activity": float(np.mean(act[-50:])),
                     "final_entropy": float(np.mean(ent[-50:])),
                     "hamming_150": ham[-1]}
        for j, t in enumerate(SNAP_T):
            show(axes[i, j], snaps[t], title=("%s  %s" % (name, rule)) if j == 0 else None)
            if i == 0:
                axes[i, j].set_xlabel("t = %d" % t, fontsize=8)
                axes[i, j].xaxis.set_label_position("top")
        print("A", name, "dens %.3f act %.4f ham %d" % (out[name]["final_density"],
              out[name]["final_activity"], ham[-1]))
    fig.tight_layout(h_pad=0.6, w_pad=0.3)
    fig.savefig(os.path.join(FIG, "figA1_rules_snapshots.png"), dpi=200)
    plt.close(fig)

    # curves
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.3))
    for name, rule, p0 in RULES:
        o = out[name]
        axes[0].plot(o["density"], lw=0.9, label=name)
        axes[1].plot(np.arange(1, T + 1), o["activity"], lw=0.9)
        axes[2].plot(o["hamming"], lw=0.9)
    axes[0].set_xlabel("generation")
    axes[0].set_ylabel("density")
    axes[0].set_xscale("symlog", linthresh=10)
    axes[1].set_xlabel("generation")
    axes[1].set_ylabel("activity (changed fraction)")
    axes[1].set_xscale("symlog", linthresh=10)
    axes[1].set_yscale("symlog", linthresh=1e-3)
    axes[2].set_xlabel("generation after 1-cell flip")
    axes[2].set_ylabel("Hamming distance (cells)")
    axes[2].set_yscale("symlog", linthresh=1)
    axes[0].legend(frameon=False, fontsize=6, ncol=2)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "figA2_rules_curves.png"), dpi=200)
    plt.close(fig)
    res["A"] = out
    return res


# ============================================================================
# B. Life, initial density sweep + methuselahs
# ============================================================================
def settle_time(hist_hashes, T):
    """first t with state(t+2)==state(t) and state(t+1)==state(t-1)"""
    return T


def exp_B(res):
    N, T, reps = 128, 1500, 6
    ps = [0.02, 0.05, 0.08, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]
    rows = []
    curves = {}
    for p in ps:
        finals, settles = [], []
        for r in range(reps):
            rng = np.random.default_rng(100 * r + int(p * 1000))
            g = rng.random((N, N)) < p
            dens = []
            h2 = [None, None]
            settled = None
            for t in range(T + 1):
                dens.append(ca.density(g))
                key = g.tobytes()
                if settled is None and h2[0] is not None and key == h2[0]:
                    settled = t - 2
                h2 = [h2[1], key]
                if settled is not None and t > settled + 5:
                    break
                g = ca.step(g, "B3/S23", True)
            finals.append(dens[-1])
            settles.append(settled if settled is not None else T)
            if r == 0:
                curves[p] = dens
        rows.append({"p0": p, "final_density": float(np.mean(finals)),
                     "final_std": float(np.std(finals)),
                     "settle_mean": float(np.mean(settles)),
                     "settle_max": int(max(settles)),
                     "n_unsettled": int(sum(s >= T for s in settles))})
        print("B p0=%.2f final %.4f settle %.0f" % (p, rows[-1]["final_density"], rows[-1]["settle_mean"]))

    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.3))
    for p in [0.05, 0.15, 0.35, 0.6, 0.9]:
        axes[0].plot(curves[p], lw=0.9, label="p0=%.2f" % p)
    axes[0].set_xscale("symlog", linthresh=10)
    axes[0].set_xlabel("generation")
    axes[0].set_ylabel("density")
    axes[0].legend(frameon=False, fontsize=6)
    axes[1].errorbar([r["p0"] for r in rows], [r["final_density"] for r in rows],
                     yerr=[r["final_std"] for r in rows], fmt="o-", ms=3, lw=0.9, color="#1f3a5f")
    axes[1].set_xlabel("initial density p0")
    axes[1].set_ylabel("final density")
    axes[2].plot([r["p0"] for r in rows], [r["settle_mean"] for r in rows], "s-", ms=3, lw=0.9, color="#b23a48")
    axes[2].set_xlabel("initial density p0")
    axes[2].set_ylabel("settle time (gens, cap %d)" % T)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "figB1_density_sweep.png"), dpi=200)
    plt.close(fig)

    # --- methuselahs on an unbounded plane, population curve from Golly (bgolly) ----
    meth = {}
    specs = [("r_pentomino", 1300), ("diehard", 150), ("acorn", 5400)]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.3))
    for k, (name, T2) in enumerate(specs):
        pat = ca.pattern(name)
        save_rle("B_" + name, pat, "B3/S23")
        t0 = time.time()
        pop = bgolly_population(os.path.join(PAT, "B_" + name + ".rle"), T2)
        pop_arr = np.array(pop)
        # stabilisation = last generation whose population is not yet 2-periodic
        # (last generation t with pop[t] != pop[t+2], plus 2)
        diff = np.nonzero(pop_arr[:-2] != pop_arr[2:])[0]
        stab = int(diff[-1]) + 2 if len(diff) else 0
        # cross-check the first 300 generations with our numpy engine
        g = np.zeros((400, 400), bool)
        ca.place(g, pat, 200, 200)
        mine = []
        for t in range(301):
            mine.append(int(g.sum()))
            g = ca.step(g, "B3/S23", False)
        n = min(len(mine), len(pop))
        agree = mine[:n] == pop[:n]
        meth[name] = {"pop": pop, "final_pop": pop[-1], "max_pop": int(pop_arr.max()),
                      "stab_est": stab, "seconds": round(time.time() - t0, 1),
                      "died_at": (int(np.argmax(pop_arr == 0)) if (pop_arr == 0).any() else None),
                      "numpy_agrees_first_300": bool(agree)}
        print("B", name, meth[name]["final_pop"], meth[name]["max_pop"], "stab", stab,
              "agree", agree, "%.1fs" % (time.time() - t0))
        axes[k].plot(pop, lw=0.8, color="#1f3a5f")
        axes[k].set_title(name.replace("_", "-"), fontsize=8, loc="left")
        axes[k].set_xlabel("generation")
        axes[k].set_ylabel("population")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "figB2_methuselah.png"), dpi=200)
    plt.close(fig)
    res["B"] = {"sweep": rows, "methuselah": meth, "N": N, "T": T, "reps": reps}
    return res


# ============================================================================
# C. logic in Life: gun + eater, glider NOT gate
# ============================================================================
def orientations(p):
    outs = []
    for k in range(4):
        r = np.rot90(p, k)
        outs.append(("rot%d" % k, r))
        outs.append(("rot%d_flip" % k, r[:, ::-1]))
    return outs


def periodic(g, rule, T, period, wrap=False):
    a = ca.run(g.copy(), rule, T, wrap)
    b = ca.run(a.copy(), rule, period, wrap)
    return np.array_equal(a, b), a


def exp_C(res):
    out = {}
    gun = ca.pattern("gosper_gun")
    eater = ca.pattern("eater1")
    S = 200
    # where does the stream go? run the lone gun and locate gliders
    g = np.zeros((S, S), bool)
    ca.place(g, gun, 10, 10)
    g200 = ca.run(g.copy(), "B3/S23", 200, False)
    lab, n = cc_label(g200, structure=np.ones((3, 3)))
    gliders = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(ys) == 5 and ys.max() > 10 + 9 + 2:
            gliders.append((int(ys.mean()), int(xs.mean())))
    gliders.sort()
    out["gun_period"] = 30
    out["stream_dir"] = "south-east" if gliders and gliders[-1][1] > gliders[0][1] else "?"
    out["gliders_t200"] = gliders
    print("C gliders at t=200:", gliders)
    # eater search: around the glider path, 30-70 cells from the gun
    found = None
    tried = 0
    t0 = time.time()
    for oname, e in orientations(eater):
        for cy in range(40, 80):
            for cx in range(cy - 10, cy + 30):   # near the diagonal of the stream
                tried += 1
                h = np.zeros((S, S), bool)
                ca.place(h, gun, 10, 10)
                if h[cy:cy + e.shape[0], cx:cx + e.shape[1]].any():
                    continue
                ca.place(h, e, cy, cx)
                ok, a = periodic(h, "B3/S23", 240, 30)
                if ok and a[cy:cy + e.shape[0], cx:cx + e.shape[1]].sum() == e.sum() \
                        and not a[90:, :].any() and not a[:, 90:].any():
                    found = (oname, cy, cx)
                    break
            if found:
                break
        if found:
            break
    print("C eater search tried %d, found %s in %.0fs" % (tried, found, time.time() - t0))
    out["eater"] = {"orientation": found[0], "y": found[1], "x": found[2], "tried": tried}
    e = dict(orientations(eater))[found[0]]
    h = np.zeros((S, S), bool)
    ca.place(h, gun, 10, 10)
    ca.place(h, e, found[1], found[2])
    save_rle("C1_gun_plus_eater", h, "B3/S23", "Gosper glider gun; eater 1 absorbs the stream")
    hs = {t: None for t in (0, 60, 120, 240)}
    gg = h.copy()
    for t in range(241):
        if t in hs:
            hs[t] = gg[:72, :72].copy()
        gg = ca.step(gg, "B3/S23", False)
    fig, axes = plt.subplots(1, 4, figsize=(7.2, 2.0))
    for ax, t in zip(axes, sorted(hs)):
        show(ax, hs[t], title="t = %d" % t)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "figC1_gun_eater.png"), dpi=200)
    plt.close(fig)

    # ---- NOT gate: a second gun (rotated, stream going north-east) crosses the first
    # geometry: gun A at (8,8) fires SE; gun B (rotated 90 deg) placed lower-left fires NE.
    # The two streams cross around x ~ 60. If every input glider annihilates a signal glider,
    # nothing ever reaches the "downstream" region x >= XL.  Dead boundary; T long enough for a
    # surviving glider to get there (c/4).
    S, YB, XL, T_NOT = 240, 110, 150, 700
    gunB = np.rot90(gun, 1)       # SE-moving gliders become NE-moving
    best = None
    tried = 0
    t0 = time.time()
    candidates = []
    for dy in range(0, 32):
        for dx in range(0, 32):
            tried += 1
            h = np.zeros((S, S), bool)
            ca.place(h, gun, 8, 8)
            ca.place(h, gunB, YB + dy, 8 + dx)
            a = ca.run(h, "B3/S23", T_NOT, False)
            if a[:, XL:].any():
                continue
            b = ca.run(a.copy(), "B3/S23", 30, False)
            if np.array_equal(a, b):
                candidates.append((dy, dx))
                if best is None:
                    best = (dy, dx)
            if len(candidates) >= 3:
                break
        if len(candidates) >= 3:
            break
    print("C NOT search tried %d, candidates %s in %.0fs" % (tried, candidates, time.time() - t0))
    out["not_gate"] = {"offset": best, "tried": tried, "candidates": candidates,
                       "geometry": {"S": S, "YB": YB, "XL": XL, "T": T_NOT}}
    dy, dx = best
    # truth table: input stream present / absent -> count gliders crossing x>=140 in t in [200,420]
    def count_output(with_input):
        h = np.zeros((S, S), bool)
        ca.place(h, gun, 8, 8)
        if with_input:
            ca.place(h, gunB, YB + dy, 8 + dx)
        seen = 0
        prev_hit = False
        g = h.copy()
        snap = None
        for t in range(T_NOT + 1):
            hit = g[:, XL].any()
            if hit and not prev_hit:
                seen += 1
            prev_hit = hit
            if t == 600:
                snap = g.copy()
            g = ca.step(g, "B3/S23", False)
        return seen, snap, h
    n1, s1, h1 = count_output(True)
    n0, s0, h0 = count_output(False)
    out["not_gate"]["output_with_input"] = n1
    out["not_gate"]["output_without_input"] = n0
    print("C NOT gate: input=1 -> %d output gliders; input=0 -> %d" % (n1, n0))
    save_rle("C2_not_gate", h1, "B3/S23",
             "NOT gate: gun A (top-left, SE stream) is the signal; gun B (bottom-left, NE stream) is the input.\n"
             "Input gliders annihilate signal gliders at the crossing, so output (right side) = NOT input.")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6))
    show(axes[0], s0, title="input = 0 (no gun B): %d gliders cross the output line" % n0)
    show(axes[1], s1, title="input = 1 (gun B on): %d gliders cross the output line" % n1)
    for ax in axes:
        ax.axvline(XL, color="#b23a48", lw=0.8, ls="--")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "figC2_not_gate.png"), dpi=200)
    plt.close(fig)

    # ---- single glider pair collision outcomes (phase / offset) -------------
    gl = ca.pattern("glider")          # moves SE
    gl2 = np.rot90(gl, 1)              # moves NE
    outcomes = {}
    for dy in range(-12, 13):
        for dx in range(-12, 13):
            h = np.zeros((80, 80), bool)
            ca.place(h, gl, 20, 20)
            yy, xx = 50 + dy, 20 + dx
            if h[yy:yy + 3, xx:xx + 3].any():
                continue
            ca.place(h, gl2, yy, xx)
            a = ca.run(h, "B3/S23", 120, False)
            pop = int(a.sum())
            key = "vanish" if pop == 0 else ("pass (10 cells)" if pop == 10 else "debris/still life")
            outcomes[key] = outcomes.get(key, 0) + 1
    out["pair_collisions"] = outcomes
    print("C pair collisions:", outcomes)
    res["C"] = out
    return res


# ============================================================================
# D. one-dimensional rules; Rule 184 == traffic model
# ============================================================================
def nasch_v1(cars, steps):
    """Agent-based traffic: N cells ring, each car moves one cell if the cell ahead is empty
    (Nagel-Schreckenberg with v_max = 1, p = 0). Returns occupancy history."""
    L = len(cars)
    pos = np.nonzero(cars)[0]
    hist = [cars.copy()]
    for _ in range(steps):
        occ = np.zeros(L, bool)
        occ[pos] = True
        ahead_free = ~occ[(pos + 1) % L]
        pos = np.where(ahead_free, (pos + 1) % L, pos)
        occ = np.zeros(L, bool)
        occ[pos] = True
        hist.append(occ)
    return np.array(hist, dtype=np.uint8)


def exp_D(res):
    out = {}
    W, T = 201, 100
    rules = [30, 90, 110, 184]
    fig, axes = plt.subplots(2, 4, figsize=(7.2, 3.9))
    rng = np.random.default_rng(7)
    single = np.zeros(W, np.uint8)
    single[W // 2] = 1
    rand = (rng.random(W) < 0.5).astype(np.uint8)
    for j, r in enumerate(rules):
        a = ca.run1d(single, r, T)
        b = ca.run1d(rand, r, T)
        show(axes[0, j], a, title="Rule %d, single seed" % r)
        show(axes[1, j], b, title="Rule %d, random" % r)
        open(os.path.join(PAT, "D_rule%d_random.rle" % r), "w").write(
            ca.write_rle(rand[None, :].astype(bool), "W%d" % r, "1D rule %d, random start (open in Golly)" % r))
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "figD1_1d_rules.png"), dpi=200)
    plt.close(fig)

    # Rule 184 vs agent-based traffic: bit-identical?
    L, steps = 400, 300
    rng = np.random.default_rng(3)
    rhos = np.linspace(0.05, 0.95, 19)
    flows_ca, flows_ab, identical = [], [], []
    for rho in rhos:
        cars = rng.random(L) < rho
        A = ca.run1d(cars.astype(np.uint8), 184, steps)
        B = nasch_v1(cars, steps)
        identical.append(bool(np.array_equal(A, B)))
        # flow = moves per cell per step over the last 100 steps
        moves = [(A[t] & ~A[t + 1]).sum() for t in range(steps - 100, steps)]
        flows_ca.append(float(np.mean(moves)) / L)
        moves = [(B[t] & ~B[t + 1]).sum() for t in range(steps - 100, steps)]
        flows_ab.append(float(np.mean(moves)) / L)
    out["traffic"] = {"rho": rhos.tolist(), "flow_rule184": flows_ca, "flow_agent": flows_ab,
                      "bit_identical": identical, "L": L, "steps": steps}
    print("D traffic identical:", all(identical), "max flow %.3f at rho %.2f" % (max(flows_ca), rhos[int(np.argmax(flows_ca))]))
    # fig: fundamental diagram + two spacetime diagrams (jam waves)
    fig = plt.figure(figsize=(7.2, 2.4))
    ax = fig.add_subplot(1, 3, 1)
    ax.plot(rhos, flows_ca, "o-", ms=3, lw=0.9, label="Rule 184 (CA)", color="#1f3a5f")
    ax.plot(rhos, flows_ab, "x", ms=5, label="car agents (NaSch v=1)", color="#b23a48")
    ax.plot(rhos, np.minimum(rhos, 1 - rhos), ls="--", lw=0.7, color="grey", label="min(rho, 1-rho)")
    ax.set_xlabel("car density rho")
    ax.set_ylabel("flow (cars / cell / step)")
    ax.legend(frameon=False, fontsize=6)
    for k, rho in enumerate([0.3, 0.7]):
        cars = rng.random(200) < rho
        A = ca.run1d(cars.astype(np.uint8), 184, 120)
        ax = fig.add_subplot(1, 3, 2 + k)
        show(ax, A, title="Rule 184, rho = %.1f (time goes down)" % rho)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "figD2_traffic.png"), dpi=200)
    plt.close(fig)
    res["D"] = out
    return res


# ============================================================================
# G. cross-validation: numpy engine vs Golly, cell by cell
# ============================================================================
def same_up_to_shift(a, b):
    ba, bb = ca.bounding_box(a), ca.bounding_box(b)
    if ba is None or bb is None:
        return ba == bb
    sa = a[ba[0]:ba[2], ba[1]:ba[3]]
    sb = b[bb[0]:bb[2], bb[1]:bb[3]]
    return sa.shape == sb.shape and bool(np.array_equal(sa, sb))


def exp_G(res):
    checks = []
    # (a) nine random soups on a 128x128 torus; Golly bounded grid syntax  rule:T128,128
    rng = np.random.default_rng(2026)
    base = rng.random((128, 128))
    for name, rule, p0 in RULES:
        g = base < p0
        path = os.path.join(PAT, "G_torus_%s.rle" % name.replace(" ", "").replace("&", ""))
        # Golly's bounded grid spans -64..63, so anchor the RLE at its top-left corner
        open(path, "w").write("#CXRLE Pos=-64,-64\n" + ca.write_rle(g, rule + ":T128,128"))
        T = 200
        mine = ca.run(g.copy(), rule, T, wrap=True)
        theirs = bgolly_run(path, T)
        # Golly keeps the full 128x128 bounded grid; our RLE writer crops to the bounding box,
        # so compare bounding-box crops
        ok = same_up_to_shift(mine, theirs)
        checks.append({"case": "torus soup %s (%s), %d gens" % (name, rule, T), "agree": ok,
                       "cells_numpy": int(mine.sum()), "cells_golly": int(theirs.sum())})
        print("G", checks[-1])
    # (b) plane patterns
    for fname, T in [("C1_gun_plus_eater", 300), ("C2_not_gate", 400), ("B_r_pentomino", 600)]:
        path = os.path.join(PAT, fname + ".rle")
        g0, rule = ca.read_rle(open(path).read())
        S = max(g0.shape) + 2 * (T // 4 + 10)
        g = np.zeros((S, S), bool)
        ca.place(g, g0, T // 4 + 10, T // 4 + 10)
        mine = ca.run(g, rule, T, wrap=False)
        theirs = bgolly_run(path, T)
        ok = same_up_to_shift(mine, theirs)
        checks.append({"case": "%s, %d gens" % (fname, T), "agree": ok,
                       "cells_numpy": int(mine.sum()), "cells_golly": int(theirs.sum())})
        print("G", checks[-1])
    res["G"] = checks
    return res


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    res = load_res()
    t0 = time.time()
    if which in ("A", "all"):
        res = exp_A(res); save_res(res)
    if which in ("B", "all"):
        res = exp_B(res); save_res(res)
    if which in ("C", "all"):
        res = exp_C(res); save_res(res)
    if which in ("D", "all"):
        res = exp_D(res); save_res(res)
    if which in ("G", "all"):
        res = exp_G(res); save_res(res)
    print("done in %.0fs" % (time.time() - t0))
