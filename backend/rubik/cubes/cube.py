import numpy as np
from .facecube import FaceCube
from random import choice
from typing import Optional


class Cube:
    def __init__(self, cube_str: Optional[str] = None):
        randomize_cube = False

        if cube_str is None:
            cube_str = "RRRRRRRRRBBBBBBBBBWWWWWWWWWGGGGGGGGGYYYYYYYYYOOOOOOOOO"
            # assert len(cube_str) == 54
            randomize_cube = True
        else:
            # Convert all the characters of the string to uppercase
            cube_str = cube_str.upper()

            # Make sure cube_str is 54 characters long
            if len(cube_str) != 54:
                raise ValueError("The cube string argument must be 54 characters long.")

            # Verify cube_str is valid
            for char in cube_str:
                if char not in ("W", "B", "R", "G", "Y", "O"):
                    raise ValueError(
                        "The cube string argument contains invalid characters "
                        "(i.e. something other than 'W', 'B', 'R', 'G', 'Y', 'O')."
                    )

        self.pieces: np.ndarray = np.array(
            [
                # Up
                [
                    [cube_str[0], cube_str[1], cube_str[2]],
                    [cube_str[3], cube_str[4], cube_str[5]],
                    [cube_str[6], cube_str[7], cube_str[8]],
                ],
                # Left
                [
                    [cube_str[9], cube_str[10], cube_str[11]],
                    [cube_str[12], cube_str[13], cube_str[14]],
                    [cube_str[15], cube_str[16], cube_str[17]],
                ],
                # Front
                [
                    [cube_str[18], cube_str[19], cube_str[20]],
                    [cube_str[21], cube_str[22], cube_str[23]],
                    [cube_str[24], cube_str[25], cube_str[26]],
                ],
                # Right
                [
                    [cube_str[27], cube_str[28], cube_str[29]],
                    [cube_str[30], cube_str[31], cube_str[32]],
                    [cube_str[33], cube_str[34], cube_str[35]],
                ],
                # Back
                [
                    [cube_str[36], cube_str[37], cube_str[38]],
                    [cube_str[39], cube_str[40], cube_str[41]],
                    [cube_str[42], cube_str[43], cube_str[44]],
                ],
                # Down
                [
                    [cube_str[45], cube_str[46], cube_str[47]],
                    [cube_str[48], cube_str[49], cube_str[50]],
                    [cube_str[51], cube_str[52], cube_str[53]],
                ],
            ]
        )

        if randomize_cube:
            self.randomize()

    def randomize(self, shuffles_num: int = 18):
        # fmt: off
        transformations = [
            "F", "F'", "F2",
            "U", "U'", "U2",
            "L", "L'", "L2",
            "R", "R'", "R2",
            "B", "B'", "B2",
            "D", "D'", "D2"
        ]
        # fmt: on
        for i in range(shuffles_num):
            self.transform(choice(transformations))

    def is_solved(self) -> bool:
        is_solved = True

        for face in self.pieces:
            middle = face[1][1]
            for row in face:
                for item in row:
                    is_solved &= item == middle

        return is_solved

    def transform(self, transformation: Optional[str] = None):
        action = transformation[0]
        times = 1
        ccw = False

        try:
            if transformation[1] != "'":
                raise Exception
            ccw = True
        except:
            ccw = False

        try:
            times = int(transformation[1])
        except:
            times = 1

        # TODO: Replace with match statement once Python 3.10 is out
        if action == "F":
            self._front(times, ccw)
        elif action == "R":
            self._right(times, ccw)
        elif action == "U":
            self._up(times, ccw)
        elif action == "L":
            self._left(times, ccw)
        elif action == "B":
            self._back(times, ccw)
        elif action == "D":
            self._down(times, ccw)
        elif action == "Y":
            self._rotate_y(times, ccw)
        else:
            print("Invalid transformation", transformation)

    def front_face(self) -> np.ndarray:
        return self.pieces[2]

    def set_front_face(self, face: np.ndarray):
        self.pieces[2] = face

    def left_face(self) -> np.ndarray:
        return self.pieces[1]

    def set_left_face(self, face: np.ndarray):
        self.pieces[1] = face

    def right_face(self) -> np.ndarray:
        return self.pieces[3]

    def set_right_face(self, face: np.ndarray):
        self.pieces[3] = face

    def back_face(self) -> np.ndarray:
        return self.pieces[4]

    def set_back_face(self, face: np.ndarray):
        self.pieces[4] = face

    def up_face(self) -> np.ndarray:
        return self.pieces[0]

    def set_up_face(self, face: np.ndarray):
        self.pieces[0] = face

    def down_face(self) -> np.ndarray:
        return self.pieces[5]

    def set_down_face(self, face: np.ndarray):
        self.pieces[5] = face

    def _rotate_face(
        self, face: np.ndarray, times: int = 1, ccw: bool = False
    ) -> np.ndarray:
        times = -times if not ccw else times
        return np.rot90(face, times)

    def _up(self, times: int = 1, ccw: bool = False):
        for i in range(times):
            # We need a copy because otherwise the pointers point to the same row
            front_top_row = self.front_face()[0].copy()
            right_top_row = self.right_face()[0].copy()
            back_top_row = self.back_face()[0].copy()
            left_top_row = self.left_face()[0].copy()

            if not ccw:
                self.left_face()[0] = front_top_row
                self.back_face()[0] = left_top_row
                self.right_face()[0] = back_top_row
                self.front_face()[0] = right_top_row
            else:
                self.right_face()[0] = front_top_row
                self.back_face()[0] = right_top_row
                self.left_face()[0] = back_top_row
                self.front_face()[0] = left_top_row

        self.set_up_face(self._rotate_face(self.up_face(), times, ccw))

    def _down(self, times: int = 1, ccw: bool = False):
        for i in range(times):
            # We need a copy because otherwise the pointers point to the same row
            front_bottom_row = self.front_face()[2].copy()
            right_bottom_row = self.right_face()[2].copy()
            back_bottom_row = self.back_face()[2].copy()
            left_bottom_row = self.left_face()[2].copy()

            if not ccw:
                self.right_face()[2] = front_bottom_row
                self.back_face()[2] = right_bottom_row
                self.left_face()[2] = back_bottom_row
                self.front_face()[2] = left_bottom_row
            else:
                self.left_face()[2] = front_bottom_row
                self.back_face()[2] = left_bottom_row
                self.right_face()[2] = back_bottom_row
                self.front_face()[2] = right_bottom_row

        self.set_down_face(self._rotate_face(self.down_face(), times, ccw))

    def _left(self, times: int = 1, ccw: bool = False):
        for i in range(times):
            front_face = self.front_face().copy()
            up_face = self.up_face().copy()
            back_face = self.back_face().copy()
            down_face = self.down_face().copy()

            # Swap the columns
            if not ccw:
                self.down_face()[:, 0] = front_face[:, 0]
                self.back_face()[:, 2] = np.flip(down_face, 0)[:, 0]
                # The column needs to be flipped to work
                self.up_face()[:, 0] = np.flip(back_face, 0)[:, 2]
                self.front_face()[:, 0] = up_face[:, 0]
            else:
                self.up_face()[:, 0] = front_face[:, 0]
                self.back_face()[:, 2] = np.flip(up_face, 0)[:, 0]
                self.down_face()[:, 0] = np.flip(back_face, 0)[:, 2]
                self.front_face()[:, 0] = down_face[:, 0]

        self.set_left_face(self._rotate_face(self.left_face(), times, ccw))

    def _right(self, times: int = 1, ccw: bool = False):
        for i in range(times):
            front_face = self.front_face().copy()
            up_face = self.up_face().copy()
            back_face = self.back_face().copy()
            down_face = self.down_face().copy()

            # Swap the columns
            if not ccw:
                self.up_face()[:, 2] = front_face[:, 2]
                self.back_face()[:, 0] = np.flip(up_face, 0)[:, 2]
                self.down_face()[:, 2] = np.flip(back_face, 0)[:, 0]
                self.front_face()[:, 2] = down_face[:, 2]
            else:
                self.down_face()[:, 2] = front_face[:, 2]
                self.back_face()[:, 0] = np.flip(down_face, 0)[:, 2]
                self.up_face()[:, 2] = np.flip(back_face, 0)[:, 0]
                self.front_face()[:, 2] = up_face[:, 2]

        self.set_right_face(self._rotate_face(self.right_face(), times, ccw))

    def _front(self, times: int = 1, ccw: bool = False):
        self.set_front_face(self._rotate_face(self.front_face(), times, ccw))

        # Move edge columns up as well
        # Apply R to the left face
        for i in range(times):
            left_face = self.left_face().copy()
            up_face = self.up_face().copy()
            right_face = self.right_face().copy()
            down_face = self.down_face().copy()

            # Swap the columns
            if not ccw:
                self.up_face()[2] = np.flip(left_face, 0)[:, 2]
                self.right_face()[:, 0] = up_face[2]
                self.down_face()[0] = np.flip(right_face, 0)[:, 0]
                self.left_face()[:, 2] = down_face[0]
            else:
                self.left_face()[:, 2] = np.flip(up_face, 1)[2]
                self.down_face()[0] = left_face[:, 2]
                self.right_face()[:, 0] = np.flip(down_face, 1)[0]
                self.up_face()[2] = right_face[:, 0]

    def _back(self, times: int = 1, ccw: bool = False):
        self.set_back_face(self._rotate_face(self.back_face(), times, ccw))

        # Move edge columns up as well
        # Apply R to the right face
        for i in range(times):
            right_face = self.right_face().copy()
            up_face = self.up_face().copy()
            left_face = self.left_face().copy()
            down_face = self.down_face().copy()

            # Swap the columns
            if not ccw:
                self.up_face()[0] = right_face[:, 2]
                self.left_face()[:, 0] = np.flip(up_face, 1)[0]
                self.down_face()[2] = left_face[:, 0]
                self.right_face()[:, 2] = np.flip(down_face, 1)[2]
            else:
                self.right_face()[:, 2] = up_face[0]
                self.down_face()[2] = np.flip(right_face, 0)[:, 2]
                self.left_face()[:, 0] = down_face[2]
                self.up_face()[0] = np.flip(left_face, 0)[:, 0]

    def _rotate_y(self, times: int = 1, ccw: bool = False):
        for i in range(times):
            up = self.up_face().copy()
            left = self.left_face().copy()
            front = self.front_face().copy()
            right = self.right_face().copy()
            back = self.back_face().copy()
            down = self.down_face().copy()

            if not ccw:
                self.set_front_face(right)
                self.set_left_face(front)
                self.set_right_face(back)
                self.set_back_face(left)
                self.set_up_face(self._rotate_face(up))
                self.set_down_face(self._rotate_face(down, ccw=True))
            else:
                self.set_front_face(left)
                self.set_left_face(back)
                self.set_right_face(front)
                self.set_back_face(right)
                self.set_up_face(self._rotate_face(up, ccw=True))
                self.set_down_face(self._rotate_face(down))

    def face_str(self) -> str:
        up = self.up_face().flatten()
        right = self.right_face().flatten()
        front = self.front_face().flatten()
        down = self.down_face().flatten()
        left = self.left_face().flatten()
        back = self.back_face().flatten()
        cube_str = "".join(np.concatenate([up, right, front, down, left, back]))

        # Grab the middle color of each face to determine each face's color
        # Convert the colors to lowercase so that they do not conflict with the face
        # letters
        up_color = self.up_face()[1][1].lower()
        right_color = self.right_face()[1][1].lower()
        front_color = self.front_face()[1][1].lower()
        down_color = self.down_face()[1][1].lower()
        left_color = self.left_face()[1][1].lower()
        back_color = self.back_face()[1][1].lower()

        # Convert the colors to lowercase so that they do not conflict with the face
        # letters
        cube_str = cube_str.lower()
        # Convert colors to face letter
        return (
            cube_str.replace(up_color, "U")
            .replace(right_color, "R")
            .replace(front_color, "F")
            .replace(down_color, "D")
            .replace(left_color, "L")
            .replace(back_color, "B")
        )

    def to_face_cube(self) -> FaceCube:
        return FaceCube(self.face_str())

    def __str__(self) -> str:
        up = self.up_face().flatten()
        left = self.left_face().flatten()
        front = self.front_face().flatten()
        right = self.right_face().flatten()
        back = self.back_face().flatten()
        down = self.down_face().flatten()
        return "".join(np.concatenate([up, left, front, right, back, down]))
