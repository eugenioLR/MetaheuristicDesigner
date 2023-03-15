from __future__ import annotations
from typing import List
from copy import copy


class Indiv:
    """
    Individual that holds a tentative solution with 
    its fitness.
    """

    def __init__(self, objfunc: ObjectiveFunc, vector: np.ndarray, speed: np.ndarray = None, operator: Operator=None):
        """
        Constructor of the Individual class.
        """

        self.objfunc = objfunc
        self._genotype = vector
        self.speed = speed
        if speed is None:
            self.speed = np.zeros_like(vector)
        self.operator = operator
        self._fitness = 0
        self.fitness_calculated = False
        self.best = vector
        self.is_dead = False
    

    def __copy__(self) -> Indiv:
        """
        Returns a copy of the Individual.
        """

        copied_ind = Indiv(self.objfunc, copy(self._genotype), copy(self.speed), self.operator)
        copied_ind._fitness = self._fitness
        copied_ind.fitness_calculated = self.fitness_calculated
        copied_ind.best = copy(self.best)
        return copied_ind
    

    @property
    def genotype(self) -> np.ndarray:
        """
        Gets the value of the vector.
        """

        return self._genotype


    @genotype.setter
    def genotype(self, vector: np.ndarray):
        """
        Sets the value of the vector.
        """

        self.fitness_calculated = False
        self._genotype = vector
    

    def store_best(self, past_indiv: Indiv):
        """
        Stores the vector that yeided the best fitness between the one the indiviudal has and another input vector
        """

        if self.fitness < past_indiv.fitness:
            self.best = past_indiv.genotype


    def reproduce(self, population: List[Indiv]) -> Indiv:
        """
        Apply the operator to obtain a new individual.
        """

        new_indiv = self.operator(self, population, self.objfunc)
        new_indiv.genotype = self.objfunc.repair_solution(new_indiv.genotype)
        return Indiv(self.objfunc, new_vector, self.speed, self.operator)


    def apply_speed(self) -> Indiv:
        """
        Apply the speed to obtain an individual with a new position.
        """

        return Indiv(self.objfunc, self._genotype + self.speed, self.speed, self.operator)


    @property
    def fitness(self) -> float:
        """
        Obtain the fitness of the individual, optimized to be calculated 
        only once per individual.
        """

        if not self.fitness_calculated:
            self.fitness = self.objfunc(self)
        return self._fitness
    
    @fitness.setter
    def fitness(self, fit: float):
        """
        Obtain the fitness of the individual, optimized to be calculated 
        only once per individual.
        """
        
        self._fitness = fit
        self.fitness_calculated = True