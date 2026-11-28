from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib import rcParams


COOPERATOR_BLUE = "#2E6F95"
DEFECTOR_RED = "#C0392B"
ACCENT_GREEN = "#27AE60"
ACCENT_GOLD = "#D4A017"
NEUTRAL_GREY = "#7F8C8D"

COOPERATOR_COOPERATOR_COLOR = COOPERATOR_BLUE
COOPERATOR_DEFECTOR_COLOR = ACCENT_GOLD
DEFECTOR_DEFECTOR_COLOR = DEFECTOR_RED


def apply_academic_style() -> None:
    plt.style.use("seaborn-v0_8-whitegrid")
    rcParams["figure.dpi"] = 110
    rcParams["savefig.dpi"] = 300
    rcParams["figure.figsize"] = (6.4, 4.4)
    rcParams["font.family"] = "DejaVu Sans"
    rcParams["font.size"] = 11
    rcParams["axes.titlesize"] = 12
    rcParams["axes.labelsize"] = 11
    rcParams["xtick.labelsize"] = 10
    rcParams["ytick.labelsize"] = 10
    rcParams["legend.fontsize"] = 10
    rcParams["axes.spines.top"] = False
    rcParams["axes.spines.right"] = False
    rcParams["axes.linewidth"] = 0.9
    rcParams["grid.alpha"] = 0.35
    rcParams["lines.linewidth"] = 1.8
    rcParams["lines.markersize"] = 6
    rcParams["legend.frameon"] = True
    rcParams["legend.framealpha"] = 0.85


def save_figure(figure: plt.Figure, output_path: str) -> None:
    figure.tight_layout()
    figure.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(figure)
