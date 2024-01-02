from inspect import cleandoc
import numpy as np
from .cube import Cube
from stringcolor import cs


def _flattened_pieces(cube: Cube) -> list[cs]:
    up = cube.pieces[0].flatten()
    top_rows = np.concatenate(
        [cube.pieces[1][0], cube.pieces[2][0], cube.pieces[3][0], cube.pieces[4][0]]
    )
    middle_rows = np.concatenate(
        [cube.pieces[1][1], cube.pieces[2][1], cube.pieces[3][1], cube.pieces[4][1]]
    )
    bottom_rows = np.concatenate(
        [cube.pieces[1][2], cube.pieces[2][2], cube.pieces[3][2], cube.pieces[4][2]]
    )
    down = cube.pieces[5].flatten()

    total = np.concatenate([up, top_rows, middle_rows, bottom_rows, down])

    colored_total = []
    for piece in total:
        color = ""
        if piece.lower() == "y":
            color = "yellow"
        elif piece.lower() == "o":
            color = "orange"
        elif piece.lower() == "b":
            color = "blue"
        elif piece.lower() == "w":
            color = "white"
        elif piece.lower() == "g":
            color = "green"
        elif piece.lower() == "r":
            color = "red"
        colored_total.append(cs(piece, color))

    return colored_total


def print_cube(cube: Cube):
    template = """
        {}{}{}
        {}{}{}
        {}{}{}
    {}{}{} {}{}{} {}{}{} {}{}{}
    {}{}{} {}{}{} {}{}{} {}{}{}
    {}{}{} {}{}{} {}{}{} {}{}{}
        {}{}{}
        {}{}{}
        {}{}{}
    """.format(
        *_flattened_pieces(cube)
    )

    print(cleandoc(template))
    # for item in _flattened_pieces(cube):
    #     print(item)
