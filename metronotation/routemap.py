LAYER_TP = 0
LAYER_MD = 1
LAYER_BT = 2
LAYER_TM = 3
LAYER_BM = 4
LAYER_AL = 5

DIR_UP = (0, -1)
DIR_DN = (0, 1)
DIR_LT = (-1, 0)
DIR_RT = (1, 0)
DIR_LU = (-1, -1)
DIR_RD = (1, 1)

LETTER_TABLE = [
    ("R", (LAYER_TP, DIR_UP, 1)),
    ("M", (LAYER_MD, DIR_DN, 1)),
    ("L", (LAYER_BT, DIR_DN, 1)),
    ("U", (LAYER_TP, DIR_RT, 1)),
    ("D", (LAYER_BT, DIR_LT, 1)),
    ("F", (LAYER_TP, DIR_RD, 1)),
    ("B", (LAYER_BT, DIR_LU, 1)),
    #
    ("R2", (LAYER_TP, DIR_UP, 2)),
    ("M2", (LAYER_MD, DIR_DN, 2)),
    ("L2", (LAYER_BT, DIR_DN, 2)),
    ("U2", (LAYER_TP, DIR_RT, 2)),
    ("D2", (LAYER_BT, DIR_LT, 2)),
    ("F2", (LAYER_TP, DIR_RD, 2)),
    ("B2", (LAYER_BT, DIR_LU, 2)),
    #
    ("R'", (LAYER_TP, DIR_DN, 1)),
    ("M'", (LAYER_MD, DIR_UP, 1)),
    ("L'", (LAYER_BT, DIR_UP, 1)),
    ("U'", (LAYER_TP, DIR_LT, 1)),
    ("D'", (LAYER_BT, DIR_RT, 1)),
    ("F'", (LAYER_TP, DIR_LU, 1)),
    ("B'", (LAYER_BT, DIR_RD, 1)),
    #
    ("R2'", (LAYER_TP, DIR_DN, 2)),
    ("M2'", (LAYER_MD, DIR_UP, 2)),
    ("L2'", (LAYER_BT, DIR_UP, 2)),
    ("U2'", (LAYER_TP, DIR_LT, 2)),
    ("D2'", (LAYER_BT, DIR_RT, 2)),
    ("F2'", (LAYER_TP, DIR_LU, 2)),
    ("B2'", (LAYER_BT, DIR_RD, 2)),
    #
    ("Rw", (LAYER_TM, DIR_UP, 1)),
    ("Lw", (LAYER_BM, DIR_DN, 1)),
    ("Uw", (LAYER_TM, DIR_RT, 1)),
    ("Dw", (LAYER_BM, DIR_LT, 1)),
    ("Fw", (LAYER_TM, DIR_RD, 1)),
    ("Bw", (LAYER_BM, DIR_LU, 1)),
    #
    ("Rw2", (LAYER_TM, DIR_UP, 2)),
    ("Lw2", (LAYER_BM, DIR_DN, 2)),
    ("Uw2", (LAYER_TM, DIR_RT, 2)),
    ("Dw2", (LAYER_BM, DIR_LT, 2)),
    ("Fw2", (LAYER_TM, DIR_RD, 2)),
    ("Bw2", (LAYER_BM, DIR_LU, 2)),
    #
    ("Rw'", (LAYER_TM, DIR_DN, 1)),
    ("Lw'", (LAYER_BM, DIR_UP, 1)),
    ("Uw'", (LAYER_TM, DIR_LT, 1)),
    ("Dw'", (LAYER_BM, DIR_RT, 1)),
    ("Fw'", (LAYER_TM, DIR_LU, 1)),
    ("Bw'", (LAYER_BM, DIR_RD, 1)),
    #
    ("Rw2'", (LAYER_TM, DIR_DN, 2)),
    ("Lw2'", (LAYER_BM, DIR_UP, 2)),
    ("Uw2'", (LAYER_TM, DIR_LT, 2)),
    ("Dw2'", (LAYER_BM, DIR_RT, 2)),
    ("Fw2'", (LAYER_TM, DIR_LU, 2)),
    ("Bw2'", (LAYER_BM, DIR_RD, 2)),
    #
    ("x'", (LAYER_AL, DIR_DN, 1)),
    ("y", (LAYER_AL, DIR_RT, 1)),
    ("y'", (LAYER_AL, DIR_LT, 1)),
]
LETTER_TABLE.sort(key=lambda x: len(x[0]), reverse=True)

CUBE_RF = 0
CUBE_OF = 1
CUBE_BF = 2
CUBE_GF = 3
CUBE_WF = 4
CUBE_YF = 5
CUBE_RB = 6
CUBE_OB = 7
CUBE_BB = 8
CUBE_GB = 9
CUBE_WB = 10
CUBE_YB = 11

CUBE_TABLE = {
    "R": CUBE_RF,
    "O": CUBE_OF,
    "B": CUBE_BF,
    "G": CUBE_GF,
    "W": CUBE_WF,
    "Y": CUBE_YF,
    "r": CUBE_RB,
    "o": CUBE_OB,
    "b": CUBE_BB,
    "g": CUBE_GB,
    "w": CUBE_WB,
    "y": CUBE_YB,
}


class Node:
    def __init__(self, letters, layer, direction, count):
        self.letters = letters
        self.layer = layer
        self.direction = direction
        self.count = count

        self.is_start_hit = False
        self.is_end_hit = False

    def from_letters(letters):
        for lt, nd in LETTER_TABLE:
            if letters.startswith(lt):
                return Node(lt, *nd), letters[len(lt) :]

        raise ValueError(letters)


class Route:
    def __init__(self, nodes):
        x = y = 0
        min_x = min_y = 0
        max_x = max_y = 0
        route_count = {(0, 0): 1}

        for node in nodes:
            for i in range(node.count):
                x += node.direction[0]
                y += node.direction[1]

                min_x = min(x, min_x)
                min_y = min(y, min_y)
                max_x = max(x, max_x)
                max_y = max(y, max_y)

                if (x, y) in route_count:
                    route_count[(x, y)] += 1
                else:
                    route_count[(x, y)] = 1

        self.nodes = nodes
        self.width = max_x - min_x
        self.height = max_y - min_y
        self.start_x = -min_x
        self.start_y = -min_y

        nodes[0].is_start_hit = route_count[(0, 0)] > 1
        nodes[-1].is_end_hit = route_count[(x, y)] > 1

    def from_letters(letters):
        nodes = []

        while letters:
            node, letters = Node.from_letters(letters)
            nodes.append(node)

        return Route(nodes)


class RouteMap:
    def __init__(self, name, cube, routes):
        self.name = name
        self.cube = cube
        self.routes = routes
        self.width = sum([route.width for route in routes])
        self.height = max([route.height for route in routes])

        for route in routes:
            route.start_y += (self.height - route.height) / 2

    def from_letters(name, cube, letters):
        cube = [CUBE_TABLE[c] for c in cube] if cube else None
        routes = [Route.from_letters(nt) for nt in letters.split()]

        return RouteMap(name, cube, routes)
