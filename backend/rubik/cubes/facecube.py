from .cubiecube import CubieCube
from .pieces import Face, Corner, Edge, Facelet


class FaceCube:
    # Maps corner positions to facelet positions
    CORNER_FACELETS = [
        [Facelet.U9, Facelet.R1, Facelet.F3],
        [Facelet.U7, Facelet.F1, Facelet.L3],
        [Facelet.U1, Facelet.L1, Facelet.B3],
        [Facelet.U3, Facelet.B1, Facelet.R3],
        [Facelet.D3, Facelet.F9, Facelet.R7],
        [Facelet.D1, Facelet.L9, Facelet.F7],
        [Facelet.D7, Facelet.B9, Facelet.L7],
        [Facelet.D9, Facelet.R9, Facelet.B7],
    ]
    # Maps edge positions to facelet positions
    EDGE_FACELETS = [
        [Facelet.U6, Facelet.R2],
        [Facelet.U8, Facelet.F2],
        [Facelet.U4, Facelet.L2],
        [Facelet.U2, Facelet.B2],
        [Facelet.D6, Facelet.R8],
        [Facelet.D2, Facelet.F8],
        [Facelet.D4, Facelet.L8],
        [Facelet.D8, Facelet.B8],
        [Facelet.F6, Facelet.R4],
        [Facelet.F4, Facelet.L6],
        [Facelet.B6, Facelet.L4],
        [Facelet.B4, Facelet.R6],
    ]
    # Maps corner positions to colors
    CORNER_COLORS = [
        [Face.U, Face.R, Face.F],
        [Face.U, Face.F, Face.L],
        [Face.U, Face.L, Face.B],
        [Face.U, Face.B, Face.R],
        [Face.D, Face.F, Face.R],
        [Face.D, Face.L, Face.F],
        [Face.D, Face.B, Face.L],
        [Face.D, Face.R, Face.B],
    ]
    # Maps edge positions to colors
    EDGE_COLORS = [
        [Face.U, Face.R],
        [Face.U, Face.F],
        [Face.U, Face.L],
        [Face.U, Face.B],
        [Face.D, Face.R],
        [Face.D, Face.F],
        [Face.D, Face.L],
        [Face.D, Face.B],
        [Face.F, Face.R],
        [Face.F, Face.L],
        [Face.B, Face.L],
        [Face.B, Face.R],
    ]

    def __init__(self, cube_str: str):
        self.pieces = [Face[cube_str[i]] for i in range(54)]

    def to_cubie_cube(self) -> CubieCube:
        cubie_cube = CubieCube()
        orientation = 0

        for i in Corner:
            for orientation in range(3):
                # All corner names begin with either a U or D
                if self.pieces[FaceCube.CORNER_FACELETS[i][orientation]] in [
                    Face.U,
                    Face.D,
                ]:
                    break

            color_1 = self.pieces[FaceCube.CORNER_FACELETS[i][(orientation + 1) % 3]]
            color_2 = self.pieces[FaceCube.CORNER_FACELETS[i][(orientation + 2) % 3]]

            for j in Corner:
                if (
                    color_1 == FaceCube.CORNER_COLORS[j][1]
                    and color_2 == FaceCube.CORNER_COLORS[j][2]
                ):
                    cubie_cube.corner_permutations[i] = j
                    cubie_cube.corner_orientations[i] = orientation
                    break

        for i in Edge:
            for j in Edge:
                if (
                    self.pieces[FaceCube.EDGE_FACELETS[i][0]]
                    == FaceCube.EDGE_COLORS[j][0]
                    and self.pieces[FaceCube.EDGE_FACELETS[i][1]]
                    == FaceCube.EDGE_COLORS[j][1]
                ):
                    cubie_cube.edge_permutations[i] = j
                    cubie_cube.edge_orientations[i] = 0
                    break
                if (
                    self.pieces[FaceCube.EDGE_FACELETS[i][0]]
                    == FaceCube.EDGE_COLORS[j][1]
                    and self.pieces[FaceCube.EDGE_FACELETS[i][1]]
                    == FaceCube.EDGE_COLORS[j][0]
                ):
                    cubie_cube.edge_permutations[i] = j
                    cubie_cube.edge_orientations[i] = 1
                    break

        return cubie_cube
