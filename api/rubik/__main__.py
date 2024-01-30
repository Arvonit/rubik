from argparse import ArgumentParser
from rubik.cubes import Cube, print_cube
from rubik.solvers import KociembaSolver


def main():
    """
    The entry point for the CLI.
    """
    parser = ArgumentParser(description="Solve a 3x3 Rubik's cube")
    parser.add_argument(
        "cube_str",
        metavar="cube",
        action="store",
        nargs="?",
        type=str,
        help="A 54-character string with the colors of each face of the cube",
    )

    args = parser.parse_args()
    cube_str: str = args.cube_str
    cube: Cube

    if cube_str is None:
        print("Generating a random cube string...")
        cube = Cube()
        print(str(cube))
        print()
    elif len(cube_str) != 54:
        print("rubik: error: The cube string argument is not 54 characters long.")
        return
    else:
        try:
            cube = Cube(cube_str)
        except ValueError as e:
            print(f"rubik: error: {e}")
            return

    # Before solver
    print_cube(cube)
    print()

    try:
        solver = KociembaSolver(cube)
        solver.solve()
    except Exception as e:
        print(f"rubik: error: {e}")
        return

    # After solver
    print()
    print_cube(cube)


if __name__ == "__main__":
    main()
