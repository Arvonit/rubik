from rubik.cube import Cube
from abc import ABC, abstractmethod


class Solver(ABC):
    """An abstract base class representing a Rubik's cube solver."""

    def __init__(self, cube: Cube):
        self.cube = cube

    @abstractmethod
    def solve(self):
        ...
