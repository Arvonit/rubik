import sys
from cube import Cube
from kociembasolver import KociembaSolver
from printer import print_cube


def main():
    cube: Cube

    try:
        cube = Cube(sys.argv[1])
    except IndexError:
        # Example cube strings
        # OBBOBRBYO GYYBOOBOG OBWBWYWWG BGRRRWOOR YWYRYRYGW RGWGGWRYG
        # OBBOBRBYOGYYBOOBOGOBWBWYWWGBGRRRWOORYWYRYRYGWRGWGGWRYG
        # WOWGYBWYOGYGYBYOGGROWBRGYWRBORWGGYBRBWORORBWBORGOWRYBY
        cube = Cube("OBBOBRBYOGYYBOOBOGOBWBWYWWGBGRRRWOORYWYRYRYGWRGWGGWRYG")

    print_cube(cube)

    solver = KociembaSolver(cube)
    solver.solve()

    print_cube(cube)


if __name__ == "__main__":
    main()
