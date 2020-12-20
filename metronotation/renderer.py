from .canvas import Canvas
from .routemap import (
    CUBE_BB,
    CUBE_BF,
    CUBE_GB,
    CUBE_GF,
    CUBE_OB,
    CUBE_OF,
    CUBE_RB,
    CUBE_RF,
    CUBE_WB,
    CUBE_WF,
    CUBE_YB,
    CUBE_YF,
    LAYER_AL,
    LAYER_BM,
    LAYER_BT,
    LAYER_MD,
    LAYER_TM,
    LAYER_TP,
    Node,
    Route,
    RouteMap,
)

CANVAS_COLOR = "white"
CANVAS_L_MARGIN = 400
CANVAS_T_MARGIN = 280
CANVAS_R_MARGIN = 400
CANVAS_B_MARGIN = 330
CANVAS_SCALE = 4

ROUTEMAP_V_MARGIN = 300

NAME_X_OFFSET = -50
NAME_FONT_NAME = "Helvetica.ttc"
NAME_FONT_SIZE = 130
NAME_COLOR = "gray"
NAME_V_MARGIN = 80

CUBE_Y_OFFSET = 30
CUBE_BLOCK_WIDTH = 150
CUBE_BLOCK_MARGIN = 15
CUBE_EDGE_WIDTH = 50
CUBE_LINE_THICKNESS = 13
CUBE_TOTAL_WIDTH = CUBE_BLOCK_WIDTH * 3 + CUBE_EDGE_WIDTH * 2 + CUBE_BLOCK_MARGIN * 4
CUBE_COLOR = {
    CUBE_RF: ("red", "red"),
    CUBE_OF: ("orange", "orange"),
    CUBE_BF: ("blue", "blue"),
    CUBE_GF: ("green", "green"),
    CUBE_WF: ("lightgray", "lightgray"),
    CUBE_YF: ("black", "yellow"),
    CUBE_RB: ("red", "white"),
    CUBE_OB: ("orange", "white"),
    CUBE_BB: ("blue", "white"),
    CUBE_GB: ("green", "white"),
    CUBE_WB: ("lightgray", "white"),
    CUBE_YB: ("yellow", "white"),
}
CUBE_H_MARGIN = 380

LETTERS_FONT_NAME = "Helvetica.ttc"
LETTERS_FONT_SIZE = 130
LETTERS_COLOR = "black"
LETTERS_V_MARGIN = 150

ROUTE_H_MARGIN = 300

NODE_LENGTH = 400
NODE_WIDTH = 65
NODE_DOUBLE_WIDTH = 31
NODE_THIN_WIDTH = 17
NODE_POINT_WIDTH = 41
NODE_COLOR = {
    LAYER_TP: "black",
    LAYER_MD: "limegreen",
    LAYER_BT: "skyblue",
    LAYER_TM: "black",
    LAYER_BM: "skyblue",
    LAYER_AL: "darkorange",
}

START_POINT_OUTER_WIDTH = 107
START_POINT_INNER_WIDTH = 73
START_POINT_COLOR = "gold"


class Renderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = Canvas(width, height, CANVAS_COLOR)

    def render_node(self, x, y, node, is_start):
        color = NODE_COLOR[node.layer]

        for i in range(node.count):
            x2 = x + node.direction[0] * NODE_LENGTH
            y2 = y + node.direction[1] * NODE_LENGTH

            if i == 0:
                if node.is_start_hit:
                    x = x * 0.8 + x2 * 0.2
                    y = y * 0.8 + y2 * 0.2

                start_color = color
                start_x = x
                start_y = y

            if i == node.count - 1 and node.is_end_hit:
                x2 = x * 0.2 + x2 * 0.8
                y2 = y * 0.2 + y2 * 0.8

            if node.layer == LAYER_MD:
                self.canvas.line(x, y, x2, y2, NODE_THIN_WIDTH, color)
            else:
                self.canvas.line(x, y, x2, y2, NODE_WIDTH, color)

                if node.layer == LAYER_TM or node.layer == LAYER_BM:
                    self.canvas.line(x, y, x2, y2, NODE_DOUBLE_WIDTH, CANVAS_COLOR)

            self.canvas.circle(x, y, NODE_WIDTH, color)
            self.canvas.circle(x, y, NODE_POINT_WIDTH, CANVAS_COLOR)

            self.canvas.circle(x2, y2, NODE_WIDTH, color)
            self.canvas.circle(x2, y2, NODE_POINT_WIDTH, CANVAS_COLOR)

            x = x2
            y = y2

        if is_start:
            self.canvas.circle(start_x, start_y, START_POINT_OUTER_WIDTH, start_color)
            self.canvas.circle(
                start_x, start_y, START_POINT_INNER_WIDTH, START_POINT_COLOR
            )

    def render_route(self, x, y, route):
        letters = "".join([node.letters for node in route.nodes])
        nw = self.canvas.text_size(letters, LETTERS_FONT_NAME, LETTERS_FONT_SIZE)[0]
        nx = x + (route.width * NODE_LENGTH - nw) / 2

        self.canvas.text(
            nx, y, letters, LETTERS_FONT_NAME, LETTERS_FONT_SIZE, LETTERS_COLOR
        )

        x += route.start_x * NODE_LENGTH
        y += LETTERS_FONT_SIZE + LETTERS_V_MARGIN + route.start_y * NODE_LENGTH

        for i, node in enumerate(route.nodes):
            self.render_node(x, y, node, i == 0)

            x += node.direction[0] * node.count * NODE_LENGTH
            y += node.direction[1] * node.count * NODE_LENGTH

    def render_cube_edge(self, left, top, index, cube):
        if index < 3:
            x = (
                left
                + CUBE_EDGE_WIDTH
                + CUBE_BLOCK_MARGIN
                + (CUBE_BLOCK_WIDTH + CUBE_BLOCK_MARGIN) * index
            )
            y = top
        elif index < 6:
            x = left + CUBE_TOTAL_WIDTH - CUBE_EDGE_WIDTH
            y = (
                top
                + CUBE_EDGE_WIDTH
                + CUBE_BLOCK_MARGIN
                + (CUBE_BLOCK_WIDTH + CUBE_BLOCK_MARGIN) * (index - 3)
            )
        elif index < 9:
            x = (
                left
                + CUBE_EDGE_WIDTH
                + CUBE_BLOCK_MARGIN
                + (CUBE_BLOCK_WIDTH + CUBE_BLOCK_MARGIN) * (8 - index)
            )
            y = top + CUBE_TOTAL_WIDTH - CUBE_EDGE_WIDTH
        else:
            x = left
            y = (
                top
                + CUBE_EDGE_WIDTH
                + CUBE_BLOCK_MARGIN
                + (CUBE_BLOCK_WIDTH + CUBE_BLOCK_MARGIN) * (11 - index)
            )

        if index < 3 or 5 < index < 9:
            w = CUBE_BLOCK_WIDTH
            h = CUBE_EDGE_WIDTH
        else:
            w = CUBE_EDGE_WIDTH
            h = CUBE_BLOCK_WIDTH

        self.canvas.rect(x, y, w, h, CUBE_COLOR[cube][0])
        self.canvas.rect(
            x + CUBE_LINE_THICKNESS,
            y + CUBE_LINE_THICKNESS,
            w - CUBE_LINE_THICKNESS * 2,
            h - CUBE_LINE_THICKNESS * 2,
            CUBE_COLOR[cube][1],
        )

    def render_cube_block(self, left, top, index_x, index_y, cube):
        x = y = CUBE_EDGE_WIDTH + CUBE_BLOCK_MARGIN
        x += left + (CUBE_BLOCK_WIDTH + CUBE_BLOCK_MARGIN) * index_x
        y += top + (CUBE_BLOCK_WIDTH + CUBE_BLOCK_MARGIN) * index_y
        w = CUBE_BLOCK_WIDTH
        h = CUBE_BLOCK_WIDTH

        self.canvas.rect(x, y, w, h, CUBE_COLOR[cube][0])
        self.canvas.rect(
            x + CUBE_LINE_THICKNESS,
            y + CUBE_LINE_THICKNESS,
            w - CUBE_LINE_THICKNESS * 2,
            h - CUBE_LINE_THICKNESS * 2,
            CUBE_COLOR[cube][1],
        )

    def render_cube(self, x, y, cube):
        for i in range(12):
            self.render_cube_edge(x, y, i, cube[i])

        for i in range(3):
            for j in range(3):
                self.render_cube_block(x, y, j, i, cube[12 + i * 3 + j])

    def render_routemap(self, x, y, routemap):
        if routemap.name:
            self.canvas.text(
                x + NAME_X_OFFSET,
                y,
                "[" + routemap.name + "]",
                NAME_FONT_NAME,
                NAME_FONT_SIZE,
                NAME_COLOR,
            )

            y += NAME_FONT_SIZE + NAME_V_MARGIN

        if routemap.cube:
            y_offset = (
                CUBE_Y_OFFSET
                + (
                    LETTERS_FONT_SIZE
                    + LETTERS_V_MARGIN
                    + routemap.height * NODE_LENGTH
                    - CUBE_TOTAL_WIDTH
                )
                / 2
            )
            self.render_cube(x, y + y_offset, routemap.cube)

            x += CUBE_TOTAL_WIDTH + CUBE_H_MARGIN

        for route in routemap.routes:
            self.render_route(x, y, route)

            x += route.width * NODE_LENGTH + ROUTE_H_MARGIN

    def get_routemap_drawing_size(routemap):
        width = (
            routemap.width * NODE_LENGTH + (len(routemap.routes) - 1) * ROUTE_H_MARGIN
        )
        if routemap.cube:
            width += CUBE_TOTAL_WIDTH + CUBE_H_MARGIN

        height = LETTERS_FONT_SIZE + LETTERS_V_MARGIN + routemap.height * NODE_LENGTH
        if routemap.name:
            height += NAME_FONT_SIZE + NAME_V_MARGIN

        return width, height

    def show(self):
        self.canvas.show()

    def render_algorithms(algo_list):
        routemaps = [RouteMap.from_letters(*algo) for algo in algo_list]

        width = height = 0

        for i, routemap in enumerate(routemaps):
            w, h = Renderer.get_routemap_drawing_size(routemap)

            width = max(w, width)
            height += h + (ROUTEMAP_V_MARGIN if i > 0 else 0)

        width += CANVAS_L_MARGIN + CANVAS_R_MARGIN
        height += CANVAS_T_MARGIN + CANVAS_B_MARGIN

        renderer = Renderer(width, height)

        x = CANVAS_L_MARGIN
        y = CANVAS_T_MARGIN

        for routemap in routemaps:
            renderer.render_routemap(x, y, routemap)

            _, h = Renderer.get_routemap_drawing_size(routemap)
            y += h + ROUTEMAP_V_MARGIN

        renderer.canvas.scale(1 / CANVAS_SCALE)
        renderer.width = renderer.canvas.width
        renderer.height = renderer.canvas.height

        return renderer

    def merge(renderers):
        width = sum([renderer.width for renderer in renderers])
        height = max([renderer.height for renderer in renderers])
        merged_renderer = Renderer(width, height)

        x = 0
        for renderer in renderers:
            merged_renderer.canvas.copy(x, 0, renderer.canvas)
            x += renderer.canvas.image.width

        return merged_renderer
