from unittest import TestCase
from rubik.cubes import Cube


class TestCube(TestCase):
    def test_init(self):
        cube = Cube("OBBOBRBYOGYYBOOBOGOBWBWYWWGBGRRROOORYWYRYRYGWRGWGGWRYG")
        self.assertEqual(0, 0)

    def test_transformation(self):
        cube = Cube("OBBOBRBYOGYYBOOBOGOBWBWYWWGBGRRROOORYWYRYRYGWRGWGGWRYG")
        self.assertEqual(0, 0)
