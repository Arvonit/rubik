from unittest import TestCase
from kociembasolver import KociembaSolver
from cube import Cube


class TestOptimalSolver(TestCase):
    def test_solve():
        cube = Cube("OBBOBRBYOGYYBOOBOGOBWBWYWWGBGRRRWOORYWYRYRYGWRGWGGWRYG")
        solver = KociembaSolver(cube)

        solver.solve(cube)  # TODO: Add assert here
        # assert str(cube) == "BBBBBBBBB"
        assert cube.is_solved()
