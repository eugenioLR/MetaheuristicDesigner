from __future__ import annotations
import time
import pandas as pd
from matplotlib import pyplot as plt
from ..Algorithm import Algorithm
from collections import Counter


class AlgorithmSelection:
    """
    General framework for metaheuristic algorithms

    Parameters
    ----------

    objfunc: ObjectiveFunc
        Objective function to be optimized.
    search_strategy: Algorithm
        Search strategy that will iteratively optimize the function.
    params: ParamScheduler or dict, optional
        Dictionary of parameters to define the stopping condition and output of the algorithm.
    """

    def __init__(
        self,
        algorithm_list: Iterable[Algorithm],
        params: Union[ParamScheduler, dict] = None,
    ):
        if params is None:
            params = {}

        self.repetitions = params.get("repetitions", 10)

        self.algorithm_list = algorithm_list

        # Avoid repeating names
        name_counter = Counter()
        for alg in algorithm_list:
            prev_name = alg.name
            if alg.name in name_counter:
                alg.name = alg.name + str(name_counter[alg.name] + 1)
            name_counter.update([prev_name])

        self.solutions = []
        self.verbose = params.get("verbose", True)

    def optimize(self):
        if self.verbose:
            print(
                f"Running {len(self.algorithm_list)} algorithms {self.repetitions} times each."
            )

        best_solution = None
        best_fitness = 0
        report_raw = pd.DataFrame(columns=["name", "realtime", "cputime", "fitness"])
        for idx, algorithm in enumerate(self.algorithm_list):
            for rep in range(self.repetitions):
                solution, fitness = algorithm.optimize()

                report_raw.loc[len(report_raw.index)] = {
                    "name": algorithm.name,
                    "realtime": algorithm.real_time_spent,
                    "cputime": algorithm.cpu_time_spent,
                    "fitness": fitness,
                }

                if self.verbose:
                    print(f"{algorithm.name} repetition {rep+1}/{self.repetitions}.")

                if best_solution is None or best_fitness > fitness:
                    best_solution = solution
                    best_fitness = fitness

                algorithm.restart()

            if self.verbose:
                print(f"{algorithm.name} finished. {idx+1}/{len(self.algorithm_list)}")
                print()

        report_gropued = report_raw.groupby("name", sort=False)
        report = pd.DataFrame()

        for group_name, group in report_gropued:
            print(group_name, group)
            report = pd.concat(
                [
                    report,
                    pd.DataFrame(
                        {
                            "name": [group_name],
                            "realtime_min": [group["realtime"].min()],
                            "realtime_avg": [group["realtime"].mean()],
                            "realtime_max": [group["realtime"].max()],
                            "realtime_std": [group["realtime"].std()],
                            "cputime_min": [group["cputime"].min()],
                            "cputime_avg": [group["cputime"].mean()],
                            "cputime_max": [group["cputime"].max()],
                            "cputime_std": [group["cputime"].std()],
                            "fitness_min": [group["fitness"].min()],
                            "fitness_avg": [group["fitness"].mean()],
                            "fitness_max": [group["fitness"].max()],
                            "fitness_std": [group["fitness"].std()],
                        }
                    ),
                ]
            )

        return best_solution, report.reset_index(drop=True)
