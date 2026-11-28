#!/usr/bin/env python3
"""Substitute {{PLACEHOLDER}} tokens in the assignment markdown with real numbers."""
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))


def pct(x, nd=1):
    return f"{100 * x:.{nd}f}%"


def nearest_p_for_accuracy(d, thr=0.9):
    """Smallest p whose accuracy reaches `thr` (interpolated, 1 decimal)."""
    ps, ac = d["p"], d["acc"]
    for i in range(1, len(ac)):
        if ac[i] >= thr > ac[i - 1]:
            f = (thr - ac[i - 1]) / max(ac[i] - ac[i - 1], 1e-9)
            return round(ps[i - 1] + f * (ps[i] - ps[i - 1]), 3)
    if ac and ac[-1] >= thr:
        return ps[-1]
    return None


A = {int(k): v for k, v in RES["a"].items()}
B = RES["b"]
M = RES["m"]
pscan = {round(r["p_informed"], 3): r for r in M["p_scan"]}
size = {int(r["n"]): r for r in M["size"]}
speed = {round(r["informed_speed"], 2): r for r in M["speed"]}

vals = {}

# ---- experiment A ---------------------------------------------------------
for n in sorted(A):
    d = A[n]
    for p in [0.0, 0.01, 0.02, 0.03, 0.05, 0.10, 0.20, 0.50]:
        idx = min(range(len(d["p"])), key=lambda i: abs(d["p"][i] - p))
        tag = f"{int(round(p * 100)):03d}"
        vals[f"ACC_{n}_{tag}"] = f"{d['acc'][idx]:.2f}"
    p90 = nearest_p_for_accuracy(d)
    vals[f"P90_{n}"] = f"{p90:.3f}" if p90 is not None else "未达到 0.9"
    if p90 is not None and n == 200:
        vals["NINF_200"] = f"{p90 * n:.1f}"

all_lead = [l for d in A.values() for l in d["lead"]]
vals["LEADFRAC"] = pct(float(np.mean(all_lead)), 0)

# ---- experiment B ---------------------------------------------------------
vals["B_P"] = f"{B['p']:.2f}"
col50 = [B["grid"][i][B["splits"].index(0.5)] for i in range(len(B["omegas"]))]
col60 = [B["grid"][i][min(range(len(B["splits"])), key=lambda j: abs(B["splits"][j] - 0.6))]
         for i in range(len(B["omegas"]))]
col70 = [B["grid"][i][min(range(len(B["splits"])), key=lambda j: abs(B["splits"][j] - 0.7))]
         for i in range(len(B["omegas"]))]
vals["B_050_MIN"], vals["B_050_MAX"] = f"{min(col50):.2f}", f"{max(col50):.2f}"
vals["B_060_MIN"], vals["B_060_MAX"] = f"{min(col60):.2f}", f"{max(col60):.2f}"
vals["B_100"] = pct(max(col70), 0)

# ---- experiment M ---------------------------------------------------------
def mk(d, key, fmt, nd=2):
    vals[key] = fmt(d) if fmt else "—"
    return vals[key]


for p, tag in [(0.0, "000"), (0.05, "005"), (0.10, "010"), (0.20, "020"),
               (0.30, "030"), (0.50, "050"), (1.0, "100")]:
    r = pscan.get(round(p, 3))
    if r is None:
        continue
    vals[f"M_{tag}"] = pct(r["success"])
    tf = r.get("t_first")
    vals[f"T_{tag}"] = f"{tf:.0f}" if tf else "未通过"
    vals[f"P{tag}"] = f"{p:.2f}"

s005 = pscan[round(0.05, 3)]["success"] - pscan[round(0.0, 3)]["success"]
sTop = pscan[round(1.0, 3)]["success"] - pscan[round(0.2, 3)]["success"]
vals["M_DELTA_005"] = pct(s005, 1)
vals["M_DELTA_TOP"] = pct(sTop, 1)
vals["M_DELTA_005_TEXT"] = (
    f"5% 的知情者把到达比例从 {pct(pscan[0.0]['success'])} 提升到 "
    f"{pct(pscan[round(0.05, 3)]['success'])}，而从 20% 提高到 100% 只多带来 "
    f"{pct(sTop, 1)}")

vals["REPS"] = str(pscan[round(0.0, 3)].get("reps", "—"))

sp = M.get("spread", [])
if sp:
    def sp_get(p, spread):
        for r in sp:
            if abs(r["p_informed"] - p) < 1e-9 and bool(r["spread"]) == spread:
                return r
        return None
    for p, tag in [(0.1, "010"), (0.3, "030"), (1.0, "100")]:
        a, b = sp_get(p, True), sp_get(p, False)
        if a and b:
            vals[f"SPREAD_{tag}"] = pct(a["success"])
            vals[f"CENTRE_{tag}"] = pct(b["success"])

for n in [20, 30, 45, 60]:
    r = size.get(n)
    if r:
        vals[f"SZ_{n}"] = pct(r["success"])
        vals[f"SZ_T{n}"] = f"{r['t_first']:.0f}" if r.get("t_first") else "—"
        vals[f"COLL_{n}"] = f"{r['collisions'] / 1000:.0f} 千"

if 20 in size and 60 in size:
    vals["COLL_RATIO"] = f"{size[60]['collisions'] / max(size[20]['collisions'], 1):.1f}"

for s, tag in [(1.0, "10"), (1.6, "16")]:
    r = speed.get(s)
    if r:
        vals[f"SP_T{tag}"] = f"{r['t_first']:.0f}" if r.get("t_first") else "—"
        vals[f"SP_S{tag}"] = pct(r["success"])

r10, r16 = speed.get(1.0), speed.get(1.6)
if r10 and r16 and r10.get("t_first") and r16.get("t_first"):
    vals["SP_IMP"] = f"{100 * (1 - r16['t_first'] / r10['t_first']):.0f}"

src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
missing = set()


def sub(m):
    k = m.group(1)
    if k in vals:
        return vals[k]
    missing.add(k)
    return m.group(0)


out = re.sub(r"\{\{([A-Z0-9_]+)\}\}", sub, text)
open(dst, "w", encoding="utf-8").write(out)
print(f"filled {len(vals)} values -> {dst}")
if missing:
    print("MISSING (left as placeholders):", sorted(missing))
else:
    print("no missing placeholders")
