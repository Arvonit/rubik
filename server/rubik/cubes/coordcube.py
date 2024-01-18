from __future__ import annotations
from .cubiecube import CubieCube
from .tables import Tables


# TODO: Move functionality from CubieCube to CoordCube since that makes more sense
class CoordCube:
    def __init__(
        self,
        phase_1_corner: int = 0,
        phase_1_edge: int = 0,
        phase_1_ud_slice: int = 0,
        phase_2_corner: int = 0,
        phase_2_edge: int = 0,
        phase_2_ud_slice: int = 0,
    ):
        self.phase_1_corner = phase_1_corner
        self.phase_1_edge = phase_1_edge
        self.phase_1_ud_slice = phase_1_ud_slice
        self.phase_2_corner = phase_2_corner
        self.phase_2_edge = phase_2_edge
        self.phase_2_ud_slice = phase_2_ud_slice
        self.tables = Tables()

    @classmethod
    def from_cubie_cube(cls, cube: CubieCube) -> CoordCube:
        """
        Converts the current `CubieCube` to a `CoordCube`. We use a class method here
        instead of an instance method in `CubieCube` because of circular import errors.
        """
        return CoordCube(
            cube.phase_1_corner,
            cube.phase_1_edge,
            cube.phase_1_ud_slice,
            cube.phase_2_corner,
            cube.phase_2_edge,
            cube.phase_2_ud_slice,
        )

    def move(self, move_num: int):
        self.phase_1_corner = self.tables.twist_move[self.phase_1_corner][move_num]
        self.phase_1_edge = self.tables.flip_move[self.phase_1_edge][move_num]
        self.phase_1_ud_slice = self.tables.udslice_move[self.phase_1_ud_slice][move_num]  # fmt: skip
        self.phase_2_corner = self.tables.corner_move[self.phase_2_corner][move_num]
        self.phase_2_edge = self.tables.edge8_move[self.phase_2_edge][move_num]
        self.phase_2_ud_slice = self.tables.edge4_move[self.phase_2_ud_slice][move_num]
