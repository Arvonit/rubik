from time import time
import numpy as np
import kociemba
from solver import Solver
from printer import print_cube


class KociembaSolver(Solver):
    def solve(self):
        start = time()
        moves = kociemba.solve(self._kociemba_str())

        for transformation in moves.split(" "):
            self.cube.transform(transformation)
            # print(transformation)
            # print_cube(self.cube)
            # print()

        end = time()

        if not self.cube.is_solved():
            raise Exception("Cube could not be solved!")

        print(f"Solution took {end - start} seconds.")
        print(moves)

    def _kociemba_str(self) -> str:
        up = self.cube.up_face().flatten()
        right = self.cube.right_face().flatten()
        front = self.cube.front_face().flatten()
        down = self.cube.down_face().flatten()
        left = self.cube.left_face().flatten()
        back = self.cube.back_face().flatten()
        cube_str = "".join(np.concatenate([up, right, front, down, left, back]))

        # Grab the middle color of each face to determine each face's color
        # Convert the colors to lowercase so that they do not conflict with Kociemba's characters
        up_color = self.cube.up_face()[1][1].lower()
        right_color = self.cube.right_face()[1][1].lower()
        front_color = self.cube.front_face()[1][1].lower()
        down_color = self.cube.down_face()[1][1].lower()
        left_color = self.cube.left_face()[1][1].lower()
        back_color = self.cube.back_face()[1][1].lower()

        # Convert the colors to lowercase so that they do not conflict with Kociemba's characters
        return cube_str.lower().replace(up_color, "U") \
            .replace(right_color, "R") \
            .replace(front_color, "F") \
            .replace(down_color, "D") \
            .replace(left_color, "L") \
            .replace(back_color, "B")
