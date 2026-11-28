from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from dynamics import (
    LinkDeathProbabilities,
    run_to_average_cooperation,
    run_with_edge_type_history,
)
from plot_utils import (
    COOPERATOR_BLUE,
    COOPERATOR_COOPERATOR_COLOR,
    COOPERATOR_DEFECTOR_COLOR,
    DEFECTOR_DEFECTOR_COLOR,
    DEFECTOR_RED,
    save_figure,
)


@dataclass(frozen=True)
class DefaultParameters:
    num_nodes: int = 100
    average_degree: float = 6.0
    initial_cooperator_fraction: float = 0.5
    selection_strength: float = 1.0
    total_steps: int = 5000
    averaging_window_size: int = 1000
    number_of_seeds: int = 50
    base_seed: int = 42
    link_death_probabilities: LinkDeathProbabilities = LinkDeathProbabilities(
        cooperator_cooperator=0.1,
        cooperator_defector=0.8,
        defector_defector=0.3,
    )


DEFAULTS = DefaultParameters()


def _assert_cooperation_array_in_range(cooperation_array: np.ndarray) -> None:
    assert cooperation_array.min() >= 0.0, "cooperation rate must be >= 0"
    assert cooperation_array.max() <= 1.0, "cooperation rate must be <= 1"


def _assert_standard_deviation_non_negative(standard_deviation_array: np.ndarray) -> None:
    assert standard_deviation_array.min() >= 0.0, "standard deviation must be non-negative"


def _assert_edge_counts_valid(
    cooperator_cooperator_history: np.ndarray,
    cooperator_defector_history: np.ndarray,
    defector_defector_history: np.ndarray,
    num_nodes: int,
) -> None:
    maximum_edges = num_nodes * (num_nodes - 1) // 2
    total_history = (
        cooperator_cooperator_history
        + cooperator_defector_history
        + defector_defector_history
    )
    assert total_history.min() >= 0, "edge count must be non-negative"
    assert total_history.max() <= maximum_edges, "edge count exceeds N(N-1)/2"


def _seed_for(seed_index: int) -> int:
    return DEFAULTS.base_seed + seed_index


def collect_cooperation_over_seeds(
    temptation: float,
    time_scale_ratio: float,
    number_of_seeds: int,
) -> np.ndarray:
    cooperation_values = np.zeros(number_of_seeds, dtype=np.float64)
    for seed_index in range(number_of_seeds):
        cooperation_values[seed_index] = run_to_average_cooperation(
            num_nodes=DEFAULTS.num_nodes,
            average_degree=DEFAULTS.average_degree,
            initial_cooperator_fraction=DEFAULTS.initial_cooperator_fraction,
            temptation=temptation,
            selection_strength=DEFAULTS.selection_strength,
            link_death_probabilities=DEFAULTS.link_death_probabilities,
            time_scale_ratio=time_scale_ratio,
            total_steps=DEFAULTS.total_steps,
            averaging_window_size=DEFAULTS.averaging_window_size,
            seed=_seed_for(seed_index),
        )
    return cooperation_values


def experiment_cooperation_vs_time_scale_ratio(figure_output_path: Path) -> dict:
    time_scale_ratios = np.array([0.0, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0])
    fixed_temptation = 1.3

    cooperation_mean_per_ratio = np.zeros(time_scale_ratios.size, dtype=np.float64)
    cooperation_standard_deviation_per_ratio = np.zeros(time_scale_ratios.size, dtype=np.float64)

    for ratio_index, time_scale_ratio in enumerate(time_scale_ratios):
        cooperation_values = collect_cooperation_over_seeds(
            temptation=fixed_temptation,
            time_scale_ratio=float(time_scale_ratio),
            number_of_seeds=DEFAULTS.number_of_seeds,
        )
        _assert_cooperation_array_in_range(cooperation_values)
        cooperation_mean_per_ratio[ratio_index] = cooperation_values.mean()
        cooperation_standard_deviation_per_ratio[ratio_index] = cooperation_values.std(ddof=1)

    _assert_cooperation_array_in_range(cooperation_mean_per_ratio)
    _assert_standard_deviation_non_negative(cooperation_standard_deviation_per_ratio)

    epsilon_for_log_axis = 0.05
    plotting_x_values = np.where(time_scale_ratios > 0.0, time_scale_ratios, epsilon_for_log_axis)

    figure, axes = plt.subplots()
    axes.errorbar(
        plotting_x_values,
        cooperation_mean_per_ratio,
        yerr=cooperation_standard_deviation_per_ratio,
        marker="o",
        capsize=3,
        color=COOPERATOR_BLUE,
        ecolor="#555555",
        elinewidth=0.9,
    )
    axes.set_xscale("log")
    axes.set_xlabel("Time-scale ratio W (link update / strategy update)")
    axes.set_ylabel("Cooperation rate (mean over last 1000 steps)")
    axes.set_title(f"Cooperation vs W   (b = {fixed_temptation},  {DEFAULTS.number_of_seeds} seeds)")
    axes.set_ylim(-0.02, 1.02)
    axes.set_xticks(plotting_x_values)
    axes.set_xticklabels([f"{value:g}" if value > 0 else "0" for value in time_scale_ratios])
    axes.axhline(DEFAULTS.initial_cooperator_fraction, color="grey", linestyle=":", linewidth=1.0, alpha=0.7,
                 label="Initial cooperator fraction")
    axes.legend(loc="lower right")
    save_figure(figure, str(figure_output_path))

    return {
        "time_scale_ratios": time_scale_ratios.tolist(),
        "cooperation_mean": cooperation_mean_per_ratio.tolist(),
        "cooperation_std": cooperation_standard_deviation_per_ratio.tolist(),
        "fixed_temptation": fixed_temptation,
    }


def experiment_cooperation_vs_temptation_static_vs_dynamic(figure_output_path: Path) -> dict:
    temptation_values = np.array([1.0, 1.05, 1.1, 1.2, 1.3, 1.5, 1.7, 2.0])
    static_time_scale_ratio = 0.0
    dynamic_time_scale_ratio = 10.0

    static_mean = np.zeros(temptation_values.size, dtype=np.float64)
    static_standard_deviation = np.zeros(temptation_values.size, dtype=np.float64)
    dynamic_mean = np.zeros(temptation_values.size, dtype=np.float64)
    dynamic_standard_deviation = np.zeros(temptation_values.size, dtype=np.float64)

    for temptation_index, temptation in enumerate(temptation_values):
        static_values = collect_cooperation_over_seeds(
            temptation=float(temptation),
            time_scale_ratio=static_time_scale_ratio,
            number_of_seeds=DEFAULTS.number_of_seeds,
        )
        dynamic_values = collect_cooperation_over_seeds(
            temptation=float(temptation),
            time_scale_ratio=dynamic_time_scale_ratio,
            number_of_seeds=DEFAULTS.number_of_seeds,
        )
        _assert_cooperation_array_in_range(static_values)
        _assert_cooperation_array_in_range(dynamic_values)
        static_mean[temptation_index] = static_values.mean()
        static_standard_deviation[temptation_index] = static_values.std(ddof=1)
        dynamic_mean[temptation_index] = dynamic_values.mean()
        dynamic_standard_deviation[temptation_index] = dynamic_values.std(ddof=1)

    _assert_cooperation_array_in_range(static_mean)
    _assert_cooperation_array_in_range(dynamic_mean)
    _assert_standard_deviation_non_negative(static_standard_deviation)
    _assert_standard_deviation_non_negative(dynamic_standard_deviation)

    figure, axes = plt.subplots()
    axes.errorbar(
        temptation_values, static_mean, yerr=static_standard_deviation,
        marker="s", capsize=3, color=DEFECTOR_RED, ecolor="#555555", elinewidth=0.9,
        label=f"Static network (W = {static_time_scale_ratio:g})",
    )
    axes.errorbar(
        temptation_values, dynamic_mean, yerr=dynamic_standard_deviation,
        marker="o", capsize=3, color=COOPERATOR_BLUE, ecolor="#555555", elinewidth=0.9,
        label=f"Dynamic network (W = {dynamic_time_scale_ratio:g})",
    )
    axes.set_xlabel("PD temptation strength b")
    axes.set_ylabel("Cooperation rate (mean over last 1000 steps)")
    axes.set_title(f"Static vs dynamic network   ({DEFAULTS.number_of_seeds} seeds)")
    axes.set_ylim(-0.02, 1.02)
    axes.legend(loc="upper right")
    save_figure(figure, str(figure_output_path))

    return {
        "temptation_values": temptation_values.tolist(),
        "static_time_scale_ratio": static_time_scale_ratio,
        "dynamic_time_scale_ratio": dynamic_time_scale_ratio,
        "static_mean": static_mean.tolist(),
        "static_std": static_standard_deviation.tolist(),
        "dynamic_mean": dynamic_mean.tolist(),
        "dynamic_std": dynamic_standard_deviation.tolist(),
    }


def experiment_edge_type_evolution(figure_output_path: Path) -> dict:
    fixed_time_scale_ratio = 5.0
    fixed_temptation = 1.3
    representative_seed = DEFAULTS.base_seed

    (
        cooperator_cooperator_history,
        cooperator_defector_history,
        defector_defector_history,
        cooperator_fraction_history,
    ) = run_with_edge_type_history(
        num_nodes=DEFAULTS.num_nodes,
        average_degree=DEFAULTS.average_degree,
        initial_cooperator_fraction=DEFAULTS.initial_cooperator_fraction,
        temptation=fixed_temptation,
        selection_strength=DEFAULTS.selection_strength,
        link_death_probabilities=DEFAULTS.link_death_probabilities,
        time_scale_ratio=fixed_time_scale_ratio,
        total_steps=DEFAULTS.total_steps,
        seed=representative_seed,
    )

    _assert_edge_counts_valid(
        cooperator_cooperator_history,
        cooperator_defector_history,
        defector_defector_history,
        DEFAULTS.num_nodes,
    )
    _assert_cooperation_array_in_range(cooperator_fraction_history)

    time_axis = np.arange(DEFAULTS.total_steps, dtype=np.int64)

    figure, primary_axis = plt.subplots()
    primary_axis.plot(time_axis, cooperator_cooperator_history,
                      color=COOPERATOR_COOPERATOR_COLOR, label="C-C edges")
    primary_axis.plot(time_axis, cooperator_defector_history,
                      color=COOPERATOR_DEFECTOR_COLOR, label="C-D edges")
    primary_axis.plot(time_axis, defector_defector_history,
                      color=DEFECTOR_DEFECTOR_COLOR, label="D-D edges")
    primary_axis.set_xlabel("Time step")
    primary_axis.set_ylabel("Edge count")
    primary_axis.set_title(
        f"Edge-type evolution  (W = {fixed_time_scale_ratio:g}, b = {fixed_temptation}, single run seed={representative_seed})"
    )
    primary_axis.set_ylim(bottom=0)
    primary_axis.legend(loc="center right")

    secondary_axis = primary_axis.twinx()
    secondary_axis.plot(time_axis, cooperator_fraction_history,
                        color="black", linestyle="--", linewidth=1.0, alpha=0.55,
                        label="Cooperator fraction")
    secondary_axis.set_ylabel("Cooperator fraction")
    secondary_axis.set_ylim(-0.02, 1.02)
    secondary_axis.grid(False)
    secondary_axis.legend(loc="upper right")

    save_figure(figure, str(figure_output_path))

    return {
        "time_scale_ratio": fixed_time_scale_ratio,
        "temptation": fixed_temptation,
        "seed": representative_seed,
        "initial_edge_counts": {
            "cc": int(cooperator_cooperator_history[0]),
            "cd": int(cooperator_defector_history[0]),
            "dd": int(defector_defector_history[0]),
        },
        "final_edge_counts": {
            "cc": int(cooperator_cooperator_history[-1]),
            "cd": int(cooperator_defector_history[-1]),
            "dd": int(defector_defector_history[-1]),
        },
        "final_cooperator_fraction": float(cooperator_fraction_history[-1]),
        "averaged_tail_edge_counts": {
            "cc": float(cooperator_cooperator_history[-DEFAULTS.averaging_window_size:].mean()),
            "cd": float(cooperator_defector_history[-DEFAULTS.averaging_window_size:].mean()),
            "dd": float(defector_defector_history[-DEFAULTS.averaging_window_size:].mean()),
        },
    }


def experiment_cooperation_heatmap(figure_output_path: Path, number_of_seeds: int) -> dict:
    time_scale_ratios = np.array([0.1, 0.5, 1.0, 2.0, 5.0, 10.0])
    temptation_values = np.array([1.0, 1.05, 1.1, 1.2, 1.3, 1.5, 1.7, 2.0])

    cooperation_grid = np.zeros((temptation_values.size, time_scale_ratios.size), dtype=np.float64)
    for temptation_index, temptation in enumerate(temptation_values):
        for ratio_index, time_scale_ratio in enumerate(time_scale_ratios):
            cooperation_values = collect_cooperation_over_seeds(
                temptation=float(temptation),
                time_scale_ratio=float(time_scale_ratio),
                number_of_seeds=number_of_seeds,
            )
            _assert_cooperation_array_in_range(cooperation_values)
            cooperation_grid[temptation_index, ratio_index] = cooperation_values.mean()

    _assert_cooperation_array_in_range(cooperation_grid)

    figure, axes = plt.subplots(figsize=(6.4, 4.8))
    heatmap_image = axes.imshow(
        cooperation_grid,
        aspect="auto",
        origin="lower",
        cmap="RdYlBu",
        vmin=0.0,
        vmax=1.0,
    )
    axes.set_xticks(np.arange(time_scale_ratios.size))
    axes.set_xticklabels([f"{value:g}" for value in time_scale_ratios])
    axes.set_yticks(np.arange(temptation_values.size))
    axes.set_yticklabels([f"{value:g}" for value in temptation_values])
    axes.set_xlabel("Time-scale ratio W")
    axes.set_ylabel("PD temptation strength b")
    axes.set_title(f"Cooperation rate heatmap   ({number_of_seeds} seeds per cell)")

    for temptation_index in range(temptation_values.size):
        for ratio_index in range(time_scale_ratios.size):
            value = cooperation_grid[temptation_index, ratio_index]
            text_color = "white" if (value < 0.25 or value > 0.75) else "black"
            axes.text(ratio_index, temptation_index, f"{value:.2f}",
                      ha="center", va="center", color=text_color, fontsize=9)

    colorbar = figure.colorbar(heatmap_image, ax=axes)
    colorbar.set_label("Cooperation rate")
    save_figure(figure, str(figure_output_path))

    return {
        "time_scale_ratios": time_scale_ratios.tolist(),
        "temptation_values": temptation_values.tolist(),
        "cooperation_grid": cooperation_grid.tolist(),
        "number_of_seeds": number_of_seeds,
    }


def run_experiment_with_timing(experiment_name: str, experiment_callable) -> tuple[dict, float]:
    start_time = time.time()
    result = experiment_callable()
    elapsed_seconds = time.time() - start_time
    print(f"  [{experiment_name}] done in {elapsed_seconds:.1f}s")
    return result, elapsed_seconds
