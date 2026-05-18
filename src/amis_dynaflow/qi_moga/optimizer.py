from __future__ import annotations
import numpy as np
import pandas as pd


def _dominates(a, b):
    return np.all(a <= b) and np.any(a < b)


def pareto_filter(objectives: np.ndarray) -> np.ndarray:
    n = len(objectives)
    keep = np.ones(n, dtype=bool)
    for i in range(n):
        if keep[i]:
            for j in range(n):
                if i != j and _dominates(objectives[j], objectives[i]):
                    keep[i] = False
                    break
    return keep


class QIMOGAOptimizer:
    """Probabilistic amplitude-based QI-MOGA reference implementation.

    This implementation intentionally avoids misleading claims about quantum speedup.
    It maintains probability distributions over candidate scheduling states on classical hardware.
    """

    def __init__(self, population_size=80, generations=120, candidate_states=24, chromosome_length=24, mutation_rate=0.05, seed=42):
        self.population_size = population_size
        self.generations = generations
        self.candidate_states = candidate_states
        self.chromosome_length = chromosome_length
        self.mutation_rate = mutation_rate
        self.rng = np.random.default_rng(seed)
        self.amplitudes = np.ones((chromosome_length, candidate_states), dtype=float) / np.sqrt(candidate_states)
        self.history = []

    def sample_population(self):
        probs = self.amplitudes ** 2
        pop = []
        for _ in range(self.population_size):
            chrom = [self.rng.choice(self.candidate_states, p=probs[g] / probs[g].sum()) + 1 for g in range(self.chromosome_length)]
            pop.append(chrom)
        return np.asarray(pop)

    def evaluate(self, population, services: pd.DataFrame) -> np.ndarray:
        base = services.groupby('station_id')['service_duration_min'].mean().reindex(range(1, self.candidate_states + 1)).fillna(services['service_duration_min'].mean()).to_numpy()
        obj = []
        for chrom in population:
            selected = base[np.asarray(chrom) - 1]
            pwt = selected.mean()
            ttis = selected.sum() / max(1, len(selected)) + np.std(selected)
            rub = np.var(np.bincount(chrom, minlength=self.candidate_states + 1)[1:])
            swe = np.var(selected / (selected.mean() + 1e-9))
            obj.append([pwt, ttis, rub, swe])
        return np.asarray(obj)

    def update_amplitudes(self, elites):
        counts = np.ones_like(self.amplitudes) * 1e-3
        for chrom in elites:
            for g, state in enumerate(chrom[:self.chromosome_length]):
                counts[g, int(state) - 1] += 1
        probs = counts / counts.sum(axis=1, keepdims=True)
        current_probs = self.amplitudes ** 2
        mixed = 0.85 * current_probs + 0.15 * probs
        noise = self.rng.normal(0, self.mutation_rate, mixed.shape)
        mixed = np.clip(mixed + noise, 1e-9, None)
        mixed = mixed / mixed.sum(axis=1, keepdims=True)
        self.amplitudes = np.sqrt(mixed)
        entropy = float((-mixed * np.log(mixed + 1e-12)).sum(axis=1).mean())
        self.history.append({'mean_entropy': entropy})

    def run(self, services: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        archive_rows = []
        for gen in range(self.generations):
            pop = self.sample_population()
            objectives = self.evaluate(pop, services)
            mask = pareto_filter(objectives)
            elites = pop[mask]
            if len(elites) == 0:
                elites = pop[np.argsort(objectives[:, 0])[: max(2, self.population_size // 10)]]
            self.update_amplitudes(elites)
            for chrom, obj in zip(pop[mask], objectives[mask]):
                archive_rows.append({'generation': gen, 'chromosome': '>'.join(map(str, chrom)), 'patient_waiting_time': obj[0], 'total_time_in_system': obj[1], 'resource_utilization_balance': obj[2], 'staff_workload_equity': obj[3]})
        archive = pd.DataFrame(archive_rows).drop_duplicates('chromosome')
        metric_df = pd.DataFrame(self.history)
        return archive, metric_df
