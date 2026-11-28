"""Regenerate every figure from results.json without re-running the simulations."""
import json
import os

import sim

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))

a = {int(k): v for k, v in R["a"].items()}
sim.fig_zones()
sim.fig_snapshots()
sim.fig_accuracy(a)
sim.fig_consensus(R["b"])
sim.fig_passage(R["m"])
sim.fig_variants(R["m"])
print("figures regenerated:", sorted(os.listdir(sim.FIGDIR)))
