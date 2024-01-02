from __future__ import annotations
from functools import reduce
from math import comb
from .pieces import Corner, Edge


class CubieCube:
    def __init__(self, cp=None, co=None, ep=None, eo=None):
        """
        :param cp: A list of the corner permutations
        :param co: A list of the corner orientations
        :param ep: A list of the edge permutations
        :param eo: A list of the edge orientations
        """
        if cp is not None and co is not None and ep is not None and eo is not None:
            self.corner_permutations = cp
            self.corner_orientations = co
            self.edge_permutations = ep
            self.edge_orientations = eo
        else:
            self.corner_permutations = [corner for corner in Corner]
            self.corner_orientations = [0 for i in range(len(Corner))]
            self.edge_permutations = [edge for edge in Edge]
            self.edge_orientations = [0 for i in range(len(Edge))]

    def choose(self, n: int, k: int) -> int:
        if 0 <= k <= n:
            return comb(n, k)
        else:
            return 0

    def corner_multiply(self, other: CubieCube):
        cp = []
        co = []

        for corner in Corner:
            cp.append(self.corner_permutations[other.corner_permutations[corner]])
            co.append(
                (
                    self.corner_orientations[other.corner_permutations[corner]]
                    + other.corner_orientations[corner]
                )
                % 3
            )

        self.corner_orientations = co
        self.corner_permutations = cp

    def edge_multiply(self, other: CubieCube):
        ep = []
        eo = []

        for edge in Edge:
            ep.append(self.edge_permutations[other.edge_permutations[edge]])
            eo.append(
                (
                    other.edge_orientations[edge]
                    + self.edge_orientations[other.edge_permutations[edge]]
                )
                % 2
            )

        self.edge_orientations = eo
        self.edge_permutations = ep

    def multiply(self, other: CubieCube):
        self.corner_multiply(other)
        self.edge_multiply(other)

    def move(self, move_num: int):
        """
        Applies one of the 6 main moves to the cube.
        """
        self.multiply(MOVE_CUBE[move_num])

    # COORDINATES NEEDED FOR KOCIEMBA ALGORITHM

    @property
    def phase_1_corner(self):
        """
        Get the corner orientation coordinate of this cube. This is needed for phase 1 of the
        kociemba algorithm.
        """
        return reduce(lambda x, y: 3 * x + y, self.corner_orientations[:7])

    @phase_1_corner.setter
    def phase_1_corner(self, new: int):
        total = 0

        for i in range(7):
            x = new % 3
            self.corner_orientations[6 - i] = x
            total += x
            new //= 3

        self.corner_orientations[7] = (-total) % 3

    @property
    def phase_1_edge(self):
        """
        Get the edge orientation coordinate of this cube. This is needed for phase 1 of the
        kociemba algorithm.
        """
        return reduce(lambda x, y: 2 * x + y, self.edge_orientations[:11])

    @phase_1_edge.setter
    def phase_1_edge(self, new: int):
        total = 0

        for i in range(11):
            x = new % 2
            self.edge_orientations[10 - i] = x
            total += x
            new //= 2

        self.edge_orientations[11] = (-total) % 2

    @property
    def phase_1_ud_slice(self):
        """
        Get the UD slice coordinate of this cube. This is determined by the positions of the 4
        UD slice edges (FL, FR, BL, BR). This is needed for phase 1 of the kociemba algorithm.
        """
        ud_slice = 0
        seen = 0

        for i in range(12):
            if 8 <= self.edge_permutations[i] < 12:
                seen += 1
            elif seen >= 1:
                ud_slice += self.choose(i, seen - 1)

        return ud_slice

    @phase_1_ud_slice.setter
    def phase_1_ud_slice(self, new: int):
        seen = 3
        x = 0
        udslice_edges = [Edge.FR, Edge.FL, Edge.BL, Edge.BR]
        other_edges = [
            Edge.UR,
            Edge.UF,
            Edge.UL,
            Edge.UB,
            Edge.DR,
            Edge.DF,
            Edge.DL,
            Edge.DB,
        ]

        # Invalidate edges
        for i in range(12):
            self.edge_permutations[i] = Edge.DB

        # First position the slice edges
        for i in range(11, -1, -1):
            if new - self.choose(i, seen) < 0:
                self.edge_permutations[i] = udslice_edges[seen]
                seen -= 1
            else:
                new -= self.choose(i, seen)

        # Then the remaining edges
        for i in range(12):
            if self.edge_permutations[i] == Edge.DB:
                self.edge_permutations[i] = other_edges[x]
                x += 1

    @property
    def phase_2_corner(self):
        """
        Get the corner permutation coordinate of this cube. This is needed for phase 2 of the
        kociemba algorithm.
        """
        corner = 0

        for j in range(7, 0, -1):
            s = 0
            for i in range(j):
                if self.corner_permutations[i] > self.corner_permutations[j]:
                    s += 1
            corner = j * (corner + s)

        return corner

    @phase_2_corner.setter
    def phase_2_corner(self, new: int):
        corners = [i for i in range(8)]
        permutations = [0 for i in range(8)]
        coeffecients = [0 for i in range(7)]

        for i in range(1, 8):
            coeffecients[i - 1] = new % (i + 1)
            new //= i + 1

        for i in range(6, -1, -1):
            permutations[i + 1] = corners.pop(i + 1 - coeffecients[i])

        permutations[0] = corners[0]
        self.corner_permutations = permutations

    @property
    def phase_2_edge(self):
        """
        Get the phase 2 edge permutation coordinate of this cube. This is determined by the
        permutations of the 8 edges not inside the UD slice. This is needed for phase 2 of the
        kociemba algorithm.
        """
        edge = 0

        for j in range(7, 0, -1):
            s = 0
            for i in range(j):
                if self.edge_permutations[i] > self.edge_permutations[j]:
                    s += 1
            edge = j * (edge + s)

        return edge

    @phase_2_edge.setter
    def phase_2_edge(self, new: int):
        edges = [i for i in range(8)]
        permutations = [0 for i in range(8)]
        coeffecients = [0 for i in range(7)]

        for i in range(1, 8):
            coeffecients[i - 1] = new % (i + 1)
            new //= i + 1

        for i in range(6, -1, -1):
            permutations[i + 1] = edges.pop(i + 1 - coeffecients[i])

        permutations[0] = edges[0]
        self.edge_permutations[:8] = permutations  # type: ignore

    @property
    def phase_2_ud_slice(self):
        """
        Get the phase 2 UD slice coordinate of this cube. This is determined by the permutations
        of the 4 UD slice edges. This is needed for phase 2 of the kociemba algorithm.
        """
        ud_slice = self.edge_permutations[8:]
        ret = 0

        for j in range(3, 0, -1):
            s = 0
            for i in range(j):
                if ud_slice[i] > ud_slice[j]:
                    s += 1
            ret = j * (ret + s)

        return ret

    @phase_2_ud_slice.setter
    def phase_2_ud_slice(self, new: int):
        ud_slice_edges = [Edge.FR, Edge.FL, Edge.BL, Edge.BR]
        permutations = [0 for i in range(4)]
        coeffecients = [0 for i in range(3)]

        for i in range(1, 4):
            coeffecients[i - 1] = new % (i + 1)
            new //= i + 1

        for i in range(2, -1, -1):
            permutations[i + 1] = ud_slice_edges.pop(i + 1 - coeffecients[i])

        permutations[0] = ud_slice_edges[0]
        self.edge_permutations[8:] = permutations  # type: ignore

    # FUNCTIONS TO DETERMINE THE VALIDITY OF CUBE

    @property
    def corner_parity(self):
        s = 0
        for i in range(7, 0, -1):
            for j in range(i - 1, -1, -1):
                if self.corner_permutations[j] > self.corner_permutations[i]:
                    s += 1

        return s % 2

    @property
    def edge_parity(self):
        s = 0
        for i in range(11, 0, -1):
            for j in range(i - 1, -1, -1):
                if self.edge_permutations[j] > self.edge_permutations[i]:
                    s += 1

        return s % 2

    def validate(self):
        total = 0
        edge_count = [0 for edge in Edge]
        corner_count = [0 for corner in Corner]

        for i in range(12):
            edge_count[self.edge_permutations[i]] += 1
        for i in range(12):
            if edge_count[i] != 1:
                return -2

        for i in range(12):
            total += self.edge_orientations[i]
        if total % 2 != 0:
            return -3

        for i in range(8):
            corner_count[self.corner_permutations[i]] += 1
        for i in range(8):
            if corner_count[i] != 1:
                return -4

        total = 0
        for i in range(8):
            total += self.corner_orientations[i]

        if total % 3 != 0:
            return -5
        elif self.edge_parity != self.corner_parity:
            return -6

        return 0


# Below is the code for `MOVE_CUBE`, which is needed for generating the move tables.
# Copyright (c) 2020 Tom Begley.
_cpU = (
    Corner.UBR,
    Corner.URF,
    Corner.UFL,
    Corner.ULB,
    Corner.DFR,
    Corner.DLF,
    Corner.DBL,
    Corner.DRB,
)
_coU = (0, 0, 0, 0, 0, 0, 0, 0)
_epU = (
    Edge.UB,
    Edge.UR,
    Edge.UF,
    Edge.UL,
    Edge.DR,
    Edge.DF,
    Edge.DL,
    Edge.DB,
    Edge.FR,
    Edge.FL,
    Edge.BL,
    Edge.BR,
)
_eoU = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

_cpR = (
    Corner.DFR,
    Corner.UFL,
    Corner.ULB,
    Corner.URF,
    Corner.DRB,
    Corner.DLF,
    Corner.DBL,
    Corner.UBR,
)
_coR = (2, 0, 0, 1, 1, 0, 0, 2)
_epR = (
    Edge.FR,
    Edge.UF,
    Edge.UL,
    Edge.UB,
    Edge.BR,
    Edge.DF,
    Edge.DL,
    Edge.DB,
    Edge.DR,
    Edge.FL,
    Edge.BL,
    Edge.UR,
)
_eoR = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

_cpF = (
    Corner.UFL,
    Corner.DLF,
    Corner.ULB,
    Corner.UBR,
    Corner.URF,
    Corner.DFR,
    Corner.DBL,
    Corner.DRB,
)
_coF = (1, 2, 0, 0, 2, 1, 0, 0)
_epF = (
    Edge.UR,
    Edge.FL,
    Edge.UL,
    Edge.UB,
    Edge.DR,
    Edge.FR,
    Edge.DL,
    Edge.DB,
    Edge.UF,
    Edge.DF,
    Edge.BL,
    Edge.BR,
)
_eoF = (0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0)

_cpD = (
    Corner.URF,
    Corner.UFL,
    Corner.ULB,
    Corner.UBR,
    Corner.DLF,
    Corner.DBL,
    Corner.DRB,
    Corner.DFR,
)
_coD = (0, 0, 0, 0, 0, 0, 0, 0)
_epD = (
    Edge.UR,
    Edge.UF,
    Edge.UL,
    Edge.UB,
    Edge.DF,
    Edge.DL,
    Edge.DB,
    Edge.DR,
    Edge.FR,
    Edge.FL,
    Edge.BL,
    Edge.BR,
)
_eoD = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

_cpL = (
    Corner.URF,
    Corner.ULB,
    Corner.DBL,
    Corner.UBR,
    Corner.DFR,
    Corner.UFL,
    Corner.DLF,
    Corner.DRB,
)
_coL = (0, 1, 2, 0, 0, 2, 1, 0)
_epL = (
    Edge.UR,
    Edge.UF,
    Edge.BL,
    Edge.UB,
    Edge.DR,
    Edge.DF,
    Edge.FL,
    Edge.DB,
    Edge.FR,
    Edge.UL,
    Edge.DL,
    Edge.BR,
)
_eoL = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

_cpB = (
    Corner.URF,
    Corner.UFL,
    Corner.UBR,
    Corner.DRB,
    Corner.DFR,
    Corner.DLF,
    Corner.ULB,
    Corner.DBL,
)
_coB = (0, 0, 1, 2, 0, 0, 2, 1)
_epB = (
    Edge.UR,
    Edge.UF,
    Edge.UL,
    Edge.BR,
    Edge.DR,
    Edge.DF,
    Edge.DL,
    Edge.BL,
    Edge.FR,
    Edge.FL,
    Edge.UB,
    Edge.DB,
)
_eoB = (0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1)

MOVE_CUBE = [CubieCube() for i in range(6)]

MOVE_CUBE[0].corner_permutations = _cpU
MOVE_CUBE[0].corner_orientations = _coU
MOVE_CUBE[0].edge_permutations = _epU
MOVE_CUBE[0].edge_orientations = _eoU

MOVE_CUBE[1].corner_permutations = _cpR
MOVE_CUBE[1].corner_orientations = _coR
MOVE_CUBE[1].edge_permutations = _epR
MOVE_CUBE[1].edge_orientations = _eoR

MOVE_CUBE[2].corner_permutations = _cpF
MOVE_CUBE[2].corner_orientations = _coF
MOVE_CUBE[2].edge_permutations = _epF
MOVE_CUBE[2].edge_orientations = _eoF

MOVE_CUBE[3].corner_permutations = _cpD
MOVE_CUBE[3].corner_orientations = _coD
MOVE_CUBE[3].edge_permutations = _epD
MOVE_CUBE[3].edge_orientations = _eoD

MOVE_CUBE[4].corner_permutations = _cpL
MOVE_CUBE[4].corner_orientations = _coL
MOVE_CUBE[4].edge_permutations = _epL
MOVE_CUBE[4].edge_orientations = _eoL

MOVE_CUBE[5].corner_permutations = _cpB
MOVE_CUBE[5].corner_orientations = _coB
MOVE_CUBE[5].edge_permutations = _epB
MOVE_CUBE[5].edge_orientations = _eoB
