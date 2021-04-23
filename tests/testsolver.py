from unittest import TestCase
from kociembasolver import KociembaSolver
from cube import Cube


class TestKociembaSolver(TestCase):
    def test_solve(self):
        cube = Cube("OBBOBRBYOGYYBOOBOGOBWBWYWWGBGRRRWOORYWYRYRYGWRGWGGWRYG")
        solver = KociembaSolver(cube)
        solver.solve()
        self.assertEqual(cube.is_solved(), True)
