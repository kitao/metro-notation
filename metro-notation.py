import math
import sys

from canvas import Canvas
from renderer import Renderer


def split_algorithm(algo_list):
    algos_lists = []
    index = 0

    for i, algo in enumerate(algo_list + [None]):
        if algo:
            continue

        alst = algo_list[index:i]
        index = i + 1

        if alst:
            algos_lists.append(alst)

    return algos_lists


def load_algorithm(filename):
    with open(filename, "r") as f:
        lines = map(lambda s: s.strip(), f.read().splitlines())

    algo_list = []
    name = None

    for line in lines:
        if not line or line[0] == "#":
            continue

        if line[0] == "-":
            algo_list.append(None)
            continue

        if line[0] == "[" and line[-1] == "]":
            name = line[1:-1]
            continue

        algo_list.append((name or "NONAME", line))
        name = None

    return split_algorithm(algo_list)


def render_algorithms(filename):
    algo_lists = load_algorithm(filename)

    for algo_list in algo_lists:
        renderer = Renderer.from_algorithm(algo_list)
        renderer.show()


def main():
    if len(sys.argv) != 2:
        print("metro-notation [filename]")
        return

    render_algorithms(sys.argv[1])


main()
