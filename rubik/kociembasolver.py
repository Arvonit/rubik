import kociemba
import numpy as np
from coordcube import CoordCube
from cube import Cube
from solver import Solver
from time import time
from tables import Tables
from pieces import Face


class KociembaSolver(Solver):
    def __init__(self, cube: Cube):
        super().__init__(cube)
        self.max_moves_length = 29  # Upper bound of the kociemba algorithm
        self.moves = []
        self.start = 0
        self.end = 0
        self.time_to_solve = 0
        self.tables = Tables()

        self.face_cube = self.cube.to_face_cube()
        self.cubie_cube = self.face_cube.to_cubie_cube()
        self.coord_cube = CoordCube.from_cubie_cube(self.cubie_cube)

        # Verify cube
        self._validate_cube()

        # Store the nth move with the index of the face being transformed in `axis` and the number
        # "quarter" turns in `power`.
        self.axis = [0 for i in range(self.max_moves_length)]
        self.power = [0 for i in range(self.max_moves_length)]

        # Coordinates needed for phase 1
        self.phase_1_corner = [0 for i in range(self.max_moves_length)]
        self.phase_1_corner[0] = self.coord_cube.phase_1_corner
        self.phase_1_edge = [0 for i in range(self.max_moves_length)]
        self.phase_1_edge[0] = self.coord_cube.phase_1_edge
        self.phase_1_ud_slice = [0 for i in range(self.max_moves_length)]
        self.phase_1_ud_slice[0] = self.coord_cube.phase_1_ud_slice

        # Coordinates needed for phase 2
        self.phase_2_corner = [0 for i in range(self.max_moves_length)]
        self.phase_2_corner[0] = self.coord_cube.phase_2_corner
        self.phase_2_edge = [0 for i in range(self.max_moves_length)]
        self.phase_2_edge[0] = self.coord_cube.phase_2_edge
        self.phase_2_ud_slice = [0 for i in range(self.max_moves_length)]
        self.phase_2_ud_slice[0] = self.coord_cube.phase_2_ud_slice

        # This stores the minimum number of moves required to complete phase 1 or 2 after n moves
        # and are derived from the pruning tables.
        self.phase_1_min_distance = [0 for i in range(self.max_moves_length)]
        self.phase_1_min_distance[0] = self._phase_1_heuristic(0)
        self.phase_2_min_distance = [0 for i in range(self.max_moves_length)]

        # Used for finding out which moves were calculated in phase 1 and phase 2
        self.phase_1_moves_index = 0

    def solve(self):
        if self.cube.is_solved():
            print("The cube is already solved.")
            return

        self.start = time()

        # My implementation of Kocimeba
        self._phase_1()

        # Kociemba implemented in C
        # self.moves = kociemba.solve(self.cube.face_str()).split(" ")

        # Apply transformations gathered from the solver
        for transformation in self.moves:
            self.cube.transform(transformation)

        if not self.cube.is_solved():
            raise RuntimeError("The cube could not be solved!")

        self.end = time()
        self.time_to_solve = round(self.end - self.start, 5)

        print(f"The solution requires {len(self.moves)} moves and took " +
              f"{self.time_to_solve} seconds.")
        print(" ".join(self.moves))

        # phase_1_moves = " ".join(self.moves[:self.phase_1_moves_index])
        # phase_2_moves = " ".join(self.moves[self.phase_1_moves_index:])
        # print(f"\nPhase 1 Moves: {phase_1_moves}")
        # print(f"Phase 2 Moves: {phase_2_moves}")

    def _phase_1(self):
        for depth in range(self.max_moves_length):
            length = self._phase_1_search(0, depth)
            if length >= 0:
                self.moves = self._generate_moves(length)
                return

        raise RuntimeError("Unable to find solution.")

    def _phase_1_heuristic(self, i: int) -> int:
        """
        This heuristic returns a lower bound on the number of moves to reach phase 2.
        """
        return max(
            self.tables.udslice_twist_prune[self.phase_1_ud_slice[i], self.phase_1_corner[i]],
            self.tables.udslice_flip_prune[self.phase_1_ud_slice[i], self.phase_1_edge[i]]
        )

    def _phase_1_search(self, n: int, depth: int) -> int:
        # print(n, depth, self.phase_1_min_distance[n])
        if self.phase_1_min_distance[n] == 0:
            # Begin phase 2
            self.phase_1_moves_index = n
            return self._phase_2(n)
        elif self.phase_1_min_distance[n] <= depth:
            for i in range(6):
                # We don't want to turn the same and opposite face on consecutive moves
                if n > 0 and self.axis[n - 1] in (i, i + 3):
                    continue

                for j in range(1, 4):
                    self.axis[n] = i
                    self.power[n] = j
                    move_num = 3 * i + j - 1

                    # Update phase 1 coordinates using tables and heuristic
                    self.phase_1_corner[n + 1] = \
                        self.tables.twist_move[self.phase_1_corner[n]][move_num]
                    self.phase_1_edge[n + 1] = \
                        self.tables.flip_move[self.phase_1_edge[n]][move_num]
                    self.phase_1_ud_slice[n + 1] = \
                        self.tables.udslice_move[self.phase_1_ud_slice[n]][move_num]
                    self.phase_1_min_distance[n + 1] = self._phase_1_heuristic(n + 1)

                    # Start search from next node
                    next = self._phase_1_search(n + 1, depth - 1)
                    if next >= 0:
                        return next

        return -1

    def _phase_2(self, n: int) -> int:
        cubie_cube = self.face_cube.to_cubie_cube()

        for i in range(n):
            for j in range(self.power[i]):
                cubie_cube.move(self.axis[i])

        self.phase_2_corner[n] = cubie_cube.phase_2_corner
        self.phase_2_edge[n] = cubie_cube.phase_2_edge
        self.phase_2_ud_slice[n] = cubie_cube.phase_2_ud_slice
        self.phase_2_min_distance[n] = self._phase_2_heuristic(n)

        for depth in range(self.max_moves_length - n):
            length = self._phase_2_search(n, depth)
            if length >= 0:
                return length

        return -1

    def _phase_2_heuristic(self, i: int) -> int:
        """
        This heuristic returns a lower bound on the number of moves to solve the cube.
        """
        return max(
            self.tables.edge4_corner_prune[self.phase_2_ud_slice[i], self.phase_2_corner[i]],
            self.tables.edge4_edge8_prune[self.phase_2_ud_slice[i], self.phase_2_edge[i]]
        )

    def _phase_2_search(self, n: int, depth: int) -> int:
        if self.phase_2_min_distance[n] == 0:
            return n
        elif self.phase_2_min_distance[n] <= depth:
            for i in range(6):
                # We don't want to turn the same and opposite face on consecutive moves
                if n > 0 and self.axis[n - 1] in (i, i + 3):
                    continue

                for j in range(1, 4):
                    # We limit moves to U*, D*, R2, L2, F2, B2
                    if i in (1, 2, 4, 5) and j != 2:
                        continue

                    self.axis[n] = i
                    self.power[n] = j

                    move_num = 3 * i + j - 1

                    # Update phase 2 coordinates using tables and heuristic
                    self.phase_2_corner[n + 1] = \
                        self.tables.corner_move[self.phase_2_corner[n]][move_num]
                    self.phase_2_edge[n + 1] = \
                        self.tables.edge8_move[self.phase_2_edge[n]][move_num]
                    self.phase_2_ud_slice[n + 1] = \
                        self.tables.edge4_move[self.phase_2_ud_slice[n]][move_num]
                    self.phase_2_min_distance[n + 1] = self._phase_2_heuristic(n + 1)

                    # Start search from next node
                    next = self._phase_2_search(n + 1, depth - 1)
                    if next >= 0:
                        return next

        return -1

    def _generate_moves(self, high: int, low: int = 0):
        def recover_move(axis_power):
            axis, power = axis_power
            if power == 1:
                return Face(axis).name
            if power == 2:
                return Face(axis).name + "2"
            if power == 3:
                return Face(axis).name + "'"
            raise RuntimeError("Invalid move in solution.")

        return list(map(recover_move, zip(self.axis[low:high], self.power[low:high])))

    def _validate_cube(self):
        def get_status():
            count = [0 for i in range(6)]

            for char in self.cube.face_str():
                count[Face[char]] += 1

            for i in range(6):
                if count[i] != 9:
                    return -1

            return self.cubie_cube.validate()

        status = get_status()
        error_message = ""

        if status == 0:
            return
        elif status == -1:
            error_message = "Not all colors appear exactly 9 times."
        elif status == -2:
            error_message = "Not all edges exist exactly once."
        elif status == -3:
            error_message = "One edge must be flipped."
        elif status == -4:
            error_message = "Not all corners exist exactly once."
        elif status == -5:
            error_message = "One corner must be twisted."
        elif status == -6:
            error_message = "Two corners or edges must be swapped."

        raise ValueError(error_message)
