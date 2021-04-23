from numpy import average
from prettytable import PrettyTable
from cube import Cube
from kociembasolver import KociembaSolver


def benchmark(trials: int = 100, shuffles_num: int = 10) -> list[float]:
    times = []
    moves = []

    for i in range(trials):
        cube = Cube("RRRRRRRRRBBBBBBBBBWWWWWWWWWGGGGGGGGGYYYYYYYYYOOOOOOOOO")
        cube.randomize(shuffles_num)

        solver = KociembaSolver(cube)
        solver.solve()

        times.append(solver.time_to_solve)
        moves.append(len(solver.moves))

    average_time = round(sum(times) / trials, 5)
    average_moves = sum(moves) / trials

    return [shuffles_num, average_time, round(min(times), 5), round(max(times), 5),
            average_moves, min(moves), max(moves)]


def main():
    table = PrettyTable()
    table.field_names = ["Shuffles", "Time", "Min Time",
                         "Max Time", "Moves", "Min Moves", "Max Moves"]
    table.add_row(benchmark(shuffles_num=10))
    table.add_row(benchmark(shuffles_num=25))
    table.add_row(benchmark(shuffles_num=40))

    print(table)


if __name__ == "__main__":
    main()
