from cube import Cube
from solver import Solver


class LayerByLayerSolver(Solver):
    def __init__(self, cube: Cube):
        super().__init__(self, cube)
        self.moves = []

    def solve(self):
        self._solve_white_cross()

        if not self.cube.is_solved():
            print("Cube could not be solved!")

        print(self.moves)

    def _solve_white_cross(self):
        pass
