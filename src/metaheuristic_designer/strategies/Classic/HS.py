from __future__ import annotations
from typing import Union
from ...operators import OperatorVector, OperatorMeta
from ...selectionMethods import SurvivorSelection, ParentSelection
from ..VariablePopulation import VariablePopulation


class HS(VariablePopulation):
    """
    Harmony search
    """

    def __init__(
        self,
        initializer: Initializer,
        params: ParamScheduler | dict = {},
        name: str = "HS",
    ):
        survivor_sel = SurvivorSelection("(m+n)")

        HSM = initializer.pop_size
        cross = OperatorVector("Multicross", {"Nindiv": HSM})

        mutate1 = OperatorVector(
            "MutNoise",
            {
                "distrib": "Gauss",
                "F": params["BW"],
                "Cr": params["HMCR"] * params["PAR"],
            },
        )
        rand1 = OperatorVector("RandomMask", {"Cr": 1 - params["HMCR"]})

        mutate = OperatorMeta("Sequence", [mutate1, rand1])

        evolve_op = OperatorMeta("Sequence", [cross, mutate])

        super().__init__(
            initializer,
            evolve_op,
            survivor_sel=survivor_sel,
            n_offspring=1,
            params=params,
            name=name,
        )
