from prettytable import PrettyTable
from rubik.cubes import Cube
from rubik.solvers import KociembaSolver, Solver, KociembaFastSolver


def benchmark(
    trials: int = 100,
    shuffles_num: int = 10,
    solver_cls: type[Solver] = KociembaSolver,
) -> list[int | float]:
    times: list[float] = []
    moves: list[int] = []

    for i in range(trials):
        cube = Cube("RRRRRRRRRBBBBBBBBBWWWWWWWWWGGGGGGGGGYYYYYYYYYOOOOOOOOO")
        cube.randomize(shuffles_num)

        solver = solver_cls(cube)
        solver.solve()

        times.append(solver.time_to_solve)
        moves.append(len(solver.moves))

    average_time = round(sum(times) / trials, 5)
    average_moves = sum(moves) / trials

    return [
        shuffles_num,
        average_time,
        round(min(times), 5),
        round(max(times), 5),
        average_moves,
        min(moves),
        max(moves),
    ]


def main():
    """
    Generates a series of statistics about the running time and move count for
    increasingly shuffled cubes. These statistics are calculated over a 100 trials.
    """
    table = PrettyTable()
    table.title = "My Implementation"
    table.field_names = [
        "Shuffles",
        "Time",
        "Min Time",
        "Max Time",
        "Moves",
        "Min Moves",
        "Max Moves",
    ]
    table.add_row(benchmark(trials=100, shuffles_num=10))
    table.add_row(benchmark(trials=100, shuffles_num=25))
    table.add_row(benchmark(trials=100, shuffles_num=40))

    table_c = PrettyTable()
    table_c.title = "C Implementation"
    table_c.field_names = [
        "Shuffles",
        "Time",
        "Min Time",
        "Max Time",
        "Moves",
        "Min Moves",
        "Max Moves",
    ]
    table_c.add_row(benchmark(shuffles_num=10, solver_cls=KociembaFastSolver))
    table_c.add_row(benchmark(shuffles_num=25, solver_cls=KociembaFastSolver))
    table_c.add_row(benchmark(shuffles_num=40, solver_cls=KociembaFastSolver))

    print(table)
    print(table_c)


if __name__ == "__main__":
    main()
