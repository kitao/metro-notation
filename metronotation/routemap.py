DIR_UP = (0, -1)
DIR_DN = (0, 1)
DIR_LT = (-1, 0)
DIR_RT = (1, 0)
DIR_LU = (-1, -1)
DIR_RD = (1, 1)

TGT_TP = 0
TGT_MD = 1
TGT_BT = 2
TGT_TM = 3
TGT_BM = 4
TGT_AL = 5

NOTATION_TABLE = [
    ("R", (TGT_TP, DIR_UP, 1)),
    ("M", (TGT_MD, DIR_DN, 1)),
    ("L", (TGT_BT, DIR_DN, 1)),
    ("U", (TGT_TP, DIR_RT, 1)),
    ("D", (TGT_BT, DIR_LT, 1)),
    ("F", (TGT_TP, DIR_RD, 1)),
    ("B", (TGT_BT, DIR_LU, 1)),
    #
    ("R2", (TGT_TP, DIR_UP, 2)),
    ("M2", (TGT_MD, DIR_DN, 2)),
    ("L2", (TGT_BT, DIR_DN, 2)),
    ("U2", (TGT_TP, DIR_RT, 2)),
    ("D2", (TGT_BT, DIR_LT, 2)),
    ("F2", (TGT_TP, DIR_RD, 2)),
    ("B2", (TGT_BT, DIR_LU, 2)),
    #
    ("R'", (TGT_TP, DIR_DN, 1)),
    ("M'", (TGT_MD, DIR_UP, 1)),
    ("L'", (TGT_BT, DIR_UP, 1)),
    ("U'", (TGT_TP, DIR_LT, 1)),
    ("D'", (TGT_BT, DIR_RT, 1)),
    ("F'", (TGT_TP, DIR_LU, 1)),
    ("B'", (TGT_BT, DIR_RD, 1)),
    #
    ("R2'", (TGT_TP, DIR_DN, 2)),
    ("M2'", (TGT_MD, DIR_UP, 2)),
    ("L2'", (TGT_BT, DIR_UP, 2)),
    ("U2'", (TGT_TP, DIR_LT, 2)),
    ("D2'", (TGT_BT, DIR_RT, 2)),
    ("F2'", (TGT_TP, DIR_LU, 2)),
    ("B2'", (TGT_BT, DIR_RD, 2)),
    #
    ("Rw", (TGT_TM, DIR_UP, 1)),
    ("Lw", (TGT_BM, DIR_DN, 1)),
    ("Uw", (TGT_TM, DIR_RT, 1)),
    ("Dw", (TGT_BM, DIR_LT, 1)),
    ("Fw", (TGT_TM, DIR_RD, 1)),
    ("Bw", (TGT_BM, DIR_LU, 1)),
    #
    ("Rw2", (TGT_TM, DIR_UP, 2)),
    ("Lw2", (TGT_BM, DIR_DN, 2)),
    ("Uw2", (TGT_TM, DIR_RT, 2)),
    ("Dw2", (TGT_BM, DIR_LT, 2)),
    ("Fw2", (TGT_TM, DIR_RD, 2)),
    ("Bw2", (TGT_BM, DIR_LU, 2)),
    #
    ("Rw'", (TGT_TM, DIR_DN, 1)),
    ("Lw'", (TGT_BM, DIR_UP, 1)),
    ("Uw'", (TGT_TM, DIR_LT, 1)),
    ("Dw'", (TGT_BM, DIR_RT, 1)),
    ("Fw'", (TGT_TM, DIR_LU, 1)),
    ("Bw'", (TGT_BM, DIR_RD, 1)),
    #
    ("Rw2'", (TGT_TM, DIR_DN, 2)),
    ("Lw2'", (TGT_BM, DIR_UP, 2)),
    ("Uw2'", (TGT_TM, DIR_LT, 2)),
    ("Dw2'", (TGT_BM, DIR_RT, 2)),
    ("Fw2'", (TGT_TM, DIR_LU, 2)),
    ("Bw2'", (TGT_BM, DIR_RD, 2)),
    #
    ("x'", (TGT_AL, DIR_DN, 1)),
    ("y", (TGT_AL, DIR_RT, 1)),
    ("y'", (TGT_AL, DIR_LT, 1)),
]
NOTATION_TABLE.sort(key=lambda x: len(x[0]), reverse=True)


class Node:
    def __init__(self, notation, target, direction, count):
        self.notation = notation
        self.target = target
        self.direction = direction
        self.count = count

        self.is_start_hit = False
        self.is_end_hit = False

    def from_notation(notation):
        for nt, nd in NOTATION_TABLE:
            if notation.startswith(nt):
                return Node(nt, *nd), notation[len(nt) :]

        raise ValueError(notation)


class Route:
    def __init__(self, nodes):
        x = y = 0
        min_x = min_y = 0
        max_x = max_y = 0
        route = {(0, 0): 1}

        for node in nodes:
            x += node.direction[0] * node.count
            y += node.direction[1] * node.count

            min_x = min(x, min_x)
            min_y = min(y, min_y)
            max_x = max(x, max_x)
            max_y = max(y, max_y)

            if (x, y) in route:
                route[(x, y)] += 1
            else:
                route[(x, y)] = 1

        self.nodes = nodes
        self.width = max_x - min_x
        self.height = max_y - min_y
        self.start_x = -min_x
        self.start_y = -min_y

        nodes[0].is_start_hit = route[(0, 0)] > 1
        nodes[-1].is_end_hit = route[(x, y)] > 1

    def from_notation(notation):
        nodes = []

        while notation:
            node, notation = Node.from_notation(notation)
            nodes.append(node)

        return Route(nodes)


class RouteMap:
    def __init__(self, name, routes):
        self.name = name
        self.routes = routes
        self.width = sum([route.width for route in routes])
        self.height = max([route.height for route in routes])

        for route in routes:
            route.start_y += (self.height - route.height) / 2

    def from_notation(name, notation):
        routes = [Route.from_notation(nt) for nt in notation.split()]

        return RouteMap(name, routes)
