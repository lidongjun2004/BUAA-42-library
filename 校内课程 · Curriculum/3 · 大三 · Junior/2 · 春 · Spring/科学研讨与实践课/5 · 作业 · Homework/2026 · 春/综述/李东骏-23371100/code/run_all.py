from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from experiments import (
    DEFAULTS,
    experiment_cooperation_heatmap,
    experiment_cooperation_vs_temptation_static_vs_dynamic,
    experiment_cooperation_vs_time_scale_ratio,
    experiment_edge_type_evolution,
    run_experiment_with_timing,
)
from plot_utils import apply_academic_style


HEATMAP_SEEDS_DEFAULT = 50


def main() -> int:
    code_directory = Path(__file__).resolve().parent
    project_root = code_directory.parent
    figure_directory = project_root / "figure"
    figure_directory.mkdir(parents=True, exist_ok=True)
    results_directory = project_root / "code"
    results_directory.mkdir(parents=True, exist_ok=True)

    apply_academic_style()

    overall_start = time.time()
    collected_results: dict = {
        "defaults": {
            "num_nodes": DEFAULTS.num_nodes,
            "average_degree": DEFAULTS.average_degree,
            "initial_cooperator_fraction": DEFAULTS.initial_cooperator_fraction,
            "selection_strength": DEFAULTS.selection_strength,
            "total_steps": DEFAULTS.total_steps,
            "averaging_window_size": DEFAULTS.averaging_window_size,
            "number_of_seeds": DEFAULTS.number_of_seeds,
            "base_seed": DEFAULTS.base_seed,
            "link_death_cooperator_cooperator": DEFAULTS.link_death_probabilities.cooperator_cooperator,
            "link_death_cooperator_defector": DEFAULTS.link_death_probabilities.cooperator_defector,
            "link_death_defector_defector": DEFAULTS.link_death_probabilities.defector_defector,
        }
    }

    print("[1/4] Cooperation vs W ...")
    result_one, _ = run_experiment_with_timing(
        "fig1",
        lambda: experiment_cooperation_vs_time_scale_ratio(
            figure_directory / "cooperation_vs_W.png"
        ),
    )
    collected_results["fig1_cooperation_vs_time_scale_ratio"] = result_one

    print("[2/4] Cooperation vs b: static vs dynamic ...")
    result_two, _ = run_experiment_with_timing(
        "fig2",
        lambda: experiment_cooperation_vs_temptation_static_vs_dynamic(
            figure_directory / "cooperation_vs_b_static_vs_dynamic.png"
        ),
    )
    collected_results["fig2_cooperation_vs_temptation_static_vs_dynamic"] = result_two

    print("[3/4] Edge-type evolution ...")
    result_three, _ = run_experiment_with_timing(
        "fig3",
        lambda: experiment_edge_type_evolution(
            figure_directory / "edge_type_evolution.png"
        ),
    )
    collected_results["fig3_edge_type_evolution"] = result_three

    print("[4/4] Cooperation heatmap ...")
    result_four, _ = run_experiment_with_timing(
        "fig4",
        lambda: experiment_cooperation_heatmap(
            figure_directory / "cooperation_heatmap.png",
            number_of_seeds=HEATMAP_SEEDS_DEFAULT,
        ),
    )
    collected_results["fig4_cooperation_heatmap"] = result_four

    overall_elapsed = time.time() - overall_start
    collected_results["total_elapsed_seconds"] = overall_elapsed

    results_path = code_directory / "results.json"
    with results_path.open("w", encoding="utf-8") as results_file:
        json.dump(collected_results, results_file, indent=2, ensure_ascii=False)

    print(f"Total wall time: {overall_elapsed:.1f}s")
    print(f"Figures written to: {figure_directory}")
    print(f"Numerical results saved to: {results_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
