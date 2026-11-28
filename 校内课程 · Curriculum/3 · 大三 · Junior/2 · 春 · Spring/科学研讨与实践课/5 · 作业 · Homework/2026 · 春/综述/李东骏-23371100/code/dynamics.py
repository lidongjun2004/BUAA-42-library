from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class PayoffMatrix:
    reward_mutual_cooperation: float
    sucker_payoff: float
    temptation_to_defect: float
    punishment_mutual_defection: float


@dataclass(frozen=True)
class LinkDeathProbabilities:
    cooperator_cooperator: float
    cooperator_defector: float
    defector_defector: float


class Population:
    def __init__(
        self,
        num_nodes: int,
        average_degree: float,
        initial_cooperator_fraction: float,
        payoff_matrix: PayoffMatrix,
        selection_strength: float,
        link_death_probabilities: LinkDeathProbabilities,
        rng: np.random.Generator,
    ) -> None:
        self.num_nodes = num_nodes
        self.payoff_matrix = payoff_matrix
        self.selection_strength = selection_strength
        self.link_death_probabilities = link_death_probabilities
        self.rng = rng

        self.adjacency_sets: list[set[int]] = [set() for _ in range(num_nodes)]
        self.edge_list: list[tuple[int, int]] = []
        self.edge_index: dict[tuple[int, int], int] = {}

        edge_probability = average_degree / (num_nodes - 1)
        for first_node in range(num_nodes):
            for second_node in range(first_node + 1, num_nodes):
                if rng.random() < edge_probability:
                    self._add_edge(first_node, second_node)

        cooperator_count = int(round(num_nodes * initial_cooperator_fraction))
        strategy_assignment = np.zeros(num_nodes, dtype=bool)
        strategy_assignment[:cooperator_count] = True
        rng.shuffle(strategy_assignment)
        self.is_cooperator = strategy_assignment

    def _add_edge(self, first_node: int, second_node: int) -> None:
        ordered_edge = (first_node, second_node) if first_node < second_node else (second_node, first_node)
        if ordered_edge in self.edge_index:
            return
        self.edge_index[ordered_edge] = len(self.edge_list)
        self.edge_list.append(ordered_edge)
        self.adjacency_sets[ordered_edge[0]].add(ordered_edge[1])
        self.adjacency_sets[ordered_edge[1]].add(ordered_edge[0])

    def _remove_edge(self, first_node: int, second_node: int) -> None:
        ordered_edge = (first_node, second_node) if first_node < second_node else (second_node, first_node)
        if ordered_edge not in self.edge_index:
            return
        index_of_removed = self.edge_index.pop(ordered_edge)
        last_edge = self.edge_list.pop()
        if last_edge != ordered_edge:
            self.edge_list[index_of_removed] = last_edge
            self.edge_index[last_edge] = index_of_removed
        self.adjacency_sets[ordered_edge[0]].discard(ordered_edge[1])
        self.adjacency_sets[ordered_edge[1]].discard(ordered_edge[0])

    def normalized_payoff(self, focal_node: int) -> float:
        neighbor_count = len(self.adjacency_sets[focal_node])
        if neighbor_count == 0:
            return 0.0
        cooperator_neighbor_count = 0
        for neighbor in self.adjacency_sets[focal_node]:
            if self.is_cooperator[neighbor]:
                cooperator_neighbor_count += 1
        defector_neighbor_count = neighbor_count - cooperator_neighbor_count
        if self.is_cooperator[focal_node]:
            accumulated_payoff = (
                self.payoff_matrix.reward_mutual_cooperation * cooperator_neighbor_count
                + self.payoff_matrix.sucker_payoff * defector_neighbor_count
            )
        else:
            accumulated_payoff = (
                self.payoff_matrix.temptation_to_defect * cooperator_neighbor_count
                + self.payoff_matrix.punishment_mutual_defection * defector_neighbor_count
            )
        return accumulated_payoff / neighbor_count

    def strategy_update_step(self) -> None:
        focal_node = int(self.rng.integers(0, self.num_nodes))
        neighbor_set = self.adjacency_sets[focal_node]
        if not neighbor_set:
            return
        neighbor_array = np.fromiter(neighbor_set, dtype=np.int64, count=len(neighbor_set))
        partner_node = int(neighbor_array[self.rng.integers(0, neighbor_array.size)])
        focal_payoff = self.normalized_payoff(focal_node)
        partner_payoff = self.normalized_payoff(partner_node)
        exponent_argument = -self.selection_strength * (partner_payoff - focal_payoff)
        imitation_probability = 1.0 / (1.0 + np.exp(exponent_argument))
        if self.rng.random() < imitation_probability:
            self.is_cooperator[focal_node] = self.is_cooperator[partner_node]

    def link_update_step(self) -> None:
        if not self.edge_list:
            return
        edge_position = int(self.rng.integers(0, len(self.edge_list)))
        endpoint_a, endpoint_b = self.edge_list[edge_position]
        death_probability = self._edge_death_probability(endpoint_a, endpoint_b)
        if self.rng.random() >= death_probability:
            return
        self._remove_edge(endpoint_a, endpoint_b)
        redirecting_endpoint = endpoint_a if self.rng.random() < 0.5 else endpoint_b
        non_neighbor_array = self._non_neighbors_of(redirecting_endpoint)
        if non_neighbor_array.size == 0:
            return
        new_partner = int(non_neighbor_array[self.rng.integers(0, non_neighbor_array.size)])
        self._add_edge(redirecting_endpoint, new_partner)

    def _edge_death_probability(self, endpoint_a: int, endpoint_b: int) -> float:
        a_is_cooperator = bool(self.is_cooperator[endpoint_a])
        b_is_cooperator = bool(self.is_cooperator[endpoint_b])
        if a_is_cooperator and b_is_cooperator:
            return self.link_death_probabilities.cooperator_cooperator
        if (not a_is_cooperator) and (not b_is_cooperator):
            return self.link_death_probabilities.defector_defector
        return self.link_death_probabilities.cooperator_defector

    def _non_neighbors_of(self, focal_node: int) -> np.ndarray:
        forbidden = self.adjacency_sets[focal_node] | {focal_node}
        candidates = [candidate for candidate in range(self.num_nodes) if candidate not in forbidden]
        return np.asarray(candidates, dtype=np.int64)

    def step(self, link_update_probability: float) -> None:
        if link_update_probability > 0.0 and self.rng.random() < link_update_probability:
            self.link_update_step()
        else:
            self.strategy_update_step()

    def cooperator_fraction(self) -> float:
        return float(self.is_cooperator.mean())

    def edge_type_counts(self) -> tuple[int, int, int]:
        cooperator_cooperator_edges = 0
        cooperator_defector_edges = 0
        defector_defector_edges = 0
        for endpoint_a, endpoint_b in self.edge_list:
            a_is_cooperator = bool(self.is_cooperator[endpoint_a])
            b_is_cooperator = bool(self.is_cooperator[endpoint_b])
            if a_is_cooperator and b_is_cooperator:
                cooperator_cooperator_edges += 1
            elif (not a_is_cooperator) and (not b_is_cooperator):
                defector_defector_edges += 1
            else:
                cooperator_defector_edges += 1
        return cooperator_cooperator_edges, cooperator_defector_edges, defector_defector_edges

    def number_of_edges(self) -> int:
        return len(self.edge_list)


def link_update_probability_from_time_scale_ratio(time_scale_ratio: float) -> float:
    if time_scale_ratio <= 0.0:
        return 0.0
    return time_scale_ratio / (1.0 + time_scale_ratio)


def run_to_average_cooperation(
    num_nodes: int,
    average_degree: float,
    initial_cooperator_fraction: float,
    temptation: float,
    selection_strength: float,
    link_death_probabilities: LinkDeathProbabilities,
    time_scale_ratio: float,
    total_steps: int,
    averaging_window_size: int,
    seed: int,
) -> float:
    rng = np.random.default_rng(seed)
    payoff_matrix = PayoffMatrix(
        reward_mutual_cooperation=1.0,
        sucker_payoff=0.0,
        temptation_to_defect=temptation,
        punishment_mutual_defection=0.0,
    )
    population = Population(
        num_nodes=num_nodes,
        average_degree=average_degree,
        initial_cooperator_fraction=initial_cooperator_fraction,
        payoff_matrix=payoff_matrix,
        selection_strength=selection_strength,
        link_death_probabilities=link_death_probabilities,
        rng=rng,
    )
    link_update_probability = link_update_probability_from_time_scale_ratio(time_scale_ratio)
    averaging_start_step = max(0, total_steps - averaging_window_size)
    cooperator_sum = 0.0
    sample_count = 0
    for step_index in range(total_steps):
        population.step(link_update_probability)
        if step_index >= averaging_start_step:
            cooperator_sum += population.cooperator_fraction()
            sample_count += 1
    return cooperator_sum / sample_count if sample_count > 0 else 0.0


def run_with_edge_type_history(
    num_nodes: int,
    average_degree: float,
    initial_cooperator_fraction: float,
    temptation: float,
    selection_strength: float,
    link_death_probabilities: LinkDeathProbabilities,
    time_scale_ratio: float,
    total_steps: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    payoff_matrix = PayoffMatrix(
        reward_mutual_cooperation=1.0,
        sucker_payoff=0.0,
        temptation_to_defect=temptation,
        punishment_mutual_defection=0.0,
    )
    population = Population(
        num_nodes=num_nodes,
        average_degree=average_degree,
        initial_cooperator_fraction=initial_cooperator_fraction,
        payoff_matrix=payoff_matrix,
        selection_strength=selection_strength,
        link_death_probabilities=link_death_probabilities,
        rng=rng,
    )
    link_update_probability = link_update_probability_from_time_scale_ratio(time_scale_ratio)
    cooperator_cooperator_history = np.zeros(total_steps, dtype=np.int64)
    cooperator_defector_history = np.zeros(total_steps, dtype=np.int64)
    defector_defector_history = np.zeros(total_steps, dtype=np.int64)
    cooperator_fraction_history = np.zeros(total_steps, dtype=np.float64)
    for step_index in range(total_steps):
        population.step(link_update_probability)
        cc, cd, dd = population.edge_type_counts()
        cooperator_cooperator_history[step_index] = cc
        cooperator_defector_history[step_index] = cd
        defector_defector_history[step_index] = dd
        cooperator_fraction_history[step_index] = population.cooperator_fraction()
    return (
        cooperator_cooperator_history,
        cooperator_defector_history,
        defector_defector_history,
        cooperator_fraction_history,
    )
