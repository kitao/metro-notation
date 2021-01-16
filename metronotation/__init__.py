import sys

from .renderer import Renderer

VERSION = "0.7.0"


def load_algorithm_file(filename):
    with open(filename, "r") as f:
        lines = map(lambda s: s.strip(), f.read().splitlines())

    #
    # parse algorithm file
    #
    algos = []
    name = cube = None

    for line in lines:
        if not line or line[0] == "#":
            continue

        if line[0] == "-":
            algos.append(None)
            continue

        if line[0] == "[" and line[-1] == "]":
            name = line[1:-1]
            continue

        if line[0] == "@":
            cube = line[1:]
            continue

        algos.append((name, cube, line))
        name = cube = None

    #
    # split algorithm list
    #
    algos_list = []
    algos_index = 0

    for i, algo in enumerate(algos + [None]):
        if algo:
            continue

        sub_algos = algos[algos_index:i]
        algos_index = i + 1

        if sub_algos:
            algos_list.append(sub_algos)

    return algos_list


def visualize_algorithm_file(filename):
    algos_list = load_algorithm_file(filename)
    renderer = Renderer.from_algorithm(algos_list)
    renderer.show()


def run():
    if len(sys.argv) != 2:
        print("metro-notation {}".format(VERSION))
        print("usage: metro-notation [filename]")
        return

    visualize_algorithm_file(sys.argv[1])
