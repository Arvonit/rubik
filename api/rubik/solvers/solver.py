from rubik.cubes import Cube
from abc import ABC, abstractmethod


class Solver(ABC):
    """An abstract base class representing a Rubik's cube solver."""

    def __init__(self, cube: Cube):
        self.cube = cube
        self.time_to_solve: float = 0
        self.moves: list = []

    @abstractmethod
    def solve(self):
        ...
