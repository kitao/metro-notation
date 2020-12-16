from .canvas import Canvas
from .routemap import (
    TGT_AL,
    TGT_BM,
    TGT_BT,
    TGT_MD,
    TGT_TM,
    TGT_TP,
    Node,
    Route,
    RouteMap,
)

CANVAS_COLOR = "white"
CANVAS_L_MARGIN = 400
CANVAS_R_MARGIN = 400
CANVAS_T_MARGIN = 280
CANVAS_B_MARGIN = 330
CANVAS_SCALE = 4

ROUTEMAP_V_MARGIN = 300

NAME_OFFSET = -150
NAME_FONT_NAME = "Helvetica.ttc"
NAME_FONT_SIZE = 130
NAME_COLOR = "gray"
NAME_V_MARGIN = 80

NOTATION_FONT_NAME = "Helvetica.ttc"
NOTATION_FONT_SIZE = 130
NOTATION_COLOR = "black"
NOTATION_V_MARGIN = 100

ROUTE_H_MARGIN = 300

NODE_LENGTH = 400
NODE_WIDTH = 65
NODE_DOUBLE_WIDTH = 31
NODE_THIN_WIDTH = 17
NODE_POINT_WIDTH = 41
NODE_COLOR = {
    TGT_TP: "black",
    TGT_MD: "limegreen",
    TGT_BT: "skyblue",
    TGT_TM: "black",
    TGT_BM: "skyblue",
    TGT_AL: "darkorange",
}

START_POINT_OUTER_WIDTH = 107
START_POINT_INNER_WIDTH = 73
START_POINT_COLOR = "gold"


class Renderer:
    def __init__(self, width, height):
        self.canvas = Canvas(width, height, CANVAS_COLOR)

    def render_node(self, x, y, node, is_start):
        color = NODE_COLOR[node.target]

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

            if node.target == TGT_MD:
                self.canvas.line(x, y, x2, y2, NODE_THIN_WIDTH, color)
            else:
                self.canvas.line(x, y, x2, y2, NODE_WIDTH, color)

                if node.target == TGT_TM or node.target == TGT_BM:
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
        notation = "".join([node.notation for node in route.nodes])
        nw = self.canvas.text_size(notation, NOTATION_FONT_NAME, NOTATION_FONT_SIZE)[0]
        nx = x + (route.width * NODE_LENGTH - nw) / 2

        self.canvas.text(
            nx, y, notation, NOTATION_FONT_NAME, NOTATION_FONT_SIZE, NOTATION_COLOR
        )

        x += route.start_x * NODE_LENGTH
        y += NOTATION_FONT_SIZE + NOTATION_V_MARGIN + route.start_y * NODE_LENGTH

        for i, node in enumerate(route.nodes):
            self.render_node(x, y, node, i == 0)

            x += node.direction[0] * node.count * NODE_LENGTH
            y += node.direction[1] * node.count * NODE_LENGTH

    def render_routemap(self, x, y, routemap):
        self.canvas.text(
            x + NAME_OFFSET,
            y,
            "[" + routemap.name + "]",
            NAME_FONT_NAME,
            NAME_FONT_SIZE,
            NAME_COLOR,
        )

        y += NAME_FONT_SIZE + NAME_V_MARGIN

        for route in routemap.routes:
            self.render_route(x, y, route)

            x += route.width * NODE_LENGTH + ROUTE_H_MARGIN

    def get_routemap_drawing_size(routemap):
        width = (
            routemap.width * NODE_LENGTH + (len(routemap.routes) - 1) * ROUTE_H_MARGIN
        )
        height = (
            NAME_FONT_SIZE
            + NAME_V_MARGIN
            + NOTATION_FONT_SIZE
            + NOTATION_V_MARGIN
            + routemap.height * NODE_LENGTH
        )

        return width, height

    def show(self):
        self.canvas.show()

    def from_algorithm(algo_list):
        routemaps = [RouteMap.from_notation(*algo) for algo in algo_list]

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

        return renderer

    def merge(renderers):
        width = height = 0
        for renderer in renderers:
            width += renderer.canvas.image.width
            height = max(renderer.canvas.image.height, height)

        merged_renderer = Renderer(width, height)

        x = 0
        for renderer in renderers:
            merged_renderer.canvas.image.paste(renderer.canvas.image, (x, 0))
            x += renderer.canvas.image.width

        return merged_renderer
