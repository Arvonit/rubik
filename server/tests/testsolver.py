from unittest import TestCase
from rubik.solvers import KociembaSolver
from rubik.cubes import Cube


class TestKociembaSolver(TestCase):
    def test_solve(self):
        cube = Cube("OBBOBRBYOGYYBOOBOGOBWBWYWWGBGRRRWOORYWYRYRYGWRGWGGWRYG")
        solver = KociembaSolver(cube)
        solver.solve()
        self.assertEqual(cube.is_solved(), True)
        print("Tests passed!")
