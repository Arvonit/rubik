import time
import kociemba
from rubik.cubes import Cube
from .solver import Solver


class KociembaFastSolver(Solver):
    """
    A wrapper around an implementation of the Kociemba algorithm in C for benchmarking
    purposes.
    """

    def __init__(self, cube: Cube):
        super().__init__(cube)
        self.time_to_solve = 0
        self.moves = []

    def solve(self):
        if self.cube.is_solved():
            print("The cube is already solved.")
            return

        start = time.time()

        # Run C implementation of Kociemba's algorithm
        self.moves = kociemba.solve(self.cube.face_str()).split(" ")

        # Apply transformations gathered from the solver
        for transformation in self.moves:
            self.cube.transform(transformation)

        if not self.cube.is_solved():
            raise RuntimeError("The cube could not be solved!")

        end = time.time()
        self.time_to_solve = round(end - start, 5)
