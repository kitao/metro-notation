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
CANVAS_H_MARGIN = 100
CANVAS_V_MARGIN = 100

ROUTEMAP_H_MARGIN = 150
ROUTEMAP_V_MARGIN = 80

TEXT_X_OFFSET = -2
TEXT_FONT_NAME = "Helvetica.ttc"
TEXT_FONT_SIZE = 32
TEXT_COLOR = "black"
TEXT_V_MARGIN = 35

CUBE_BLOCK_SIZE = 37
CUBE_BLOCK_MARGIN = 4
CUBE_SIDE_SIZE = 12
CUBE_LINE_THICKNESS = 3
CUBE_TOTAL_SIZE = CUBE_BLOCK_SIZE * 3 + CUBE_SIDE_SIZE * 2 + CUBE_BLOCK_MARGIN * 4
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
CUBE_H_MARGIN = 110

ROUTE_H_MARGIN = 80

NODE_LENGTH = 100
NODE_THICKNESS = 15
NODE_DOUBLE_THICKNESS = 7
NODE_THIN_THICKNESS = 3
NODE_POINT_SIZE = 9
NODE_COLOR = {
    LAYER_TP: "black",
    LAYER_MD: "limegreen",
    LAYER_BT: "skyblue",
    LAYER_TM: "black",
    LAYER_BM: "skyblue",
    LAYER_AL: "darkorange",
}

NODE_START_OUTER_SIZE = 27
NODE_START_INNER_SIZE = 19
NODE_START_COLOR = "gold"


def routemap_drawing_size(routemap):
    width = (
        CUBE_TOTAL_SIZE
        + CUBE_H_MARGIN
        + routemap.width * NODE_LENGTH
        + ROUTE_H_MARGIN * (len(routemap.routes) - 1)
    )
    height = (
        TEXT_FONT_SIZE
        + TEXT_V_MARGIN
        + max(CUBE_TOTAL_SIZE, routemap.height * NODE_LENGTH)
    )

    return width, height


class Renderer:
    def __init__(self, width, height):
        self.canvas = Canvas(width, height, CANVAS_COLOR)

    @property
    def width(self):
        return self.canvas.width

    @property
    def height(self):
        return self.canvas.height

    def draw_node(self, x, y, node, is_start):
        color = NODE_COLOR[node.layer]

        for i in range(node.distance):
            x2 = x + node.direction[0] * NODE_LENGTH
            y2 = y + node.direction[1] * NODE_LENGTH

            if i == 0:
                if node.is_start_hit:
                    x = x * 0.8 + x2 * 0.2
                    y = y * 0.8 + y2 * 0.2

                start_color = color
                start_x = x
                start_y = y

            if i == node.distance - 1 and node.is_end_hit:
                x2 = x * 0.2 + x2 * 0.8
                y2 = y * 0.2 + y2 * 0.8

            if node.layer == LAYER_MD:
                self.canvas.line(x, y, x2, y2, NODE_THIN_THICKNESS, color)
            else:
                self.canvas.line(x, y, x2, y2, NODE_THICKNESS, color)

                if node.layer == LAYER_TM or node.layer == LAYER_BM:
                    self.canvas.line(x, y, x2, y2, NODE_DOUBLE_THICKNESS, CANVAS_COLOR)

            self.canvas.circle(x, y, NODE_THICKNESS, color)
            self.canvas.circle(x, y, NODE_POINT_SIZE, CANVAS_COLOR)

            self.canvas.circle(x2, y2, NODE_THICKNESS, color)
            self.canvas.circle(x2, y2, NODE_POINT_SIZE, CANVAS_COLOR)

            x = x2
            y = y2

        if is_start:
            self.canvas.circle(start_x, start_y, NODE_START_OUTER_SIZE, start_color)
            self.canvas.circle(
                start_x, start_y, NODE_START_INNER_SIZE, NODE_START_COLOR
            )

    def draw_route(self, x, y, route):
        x += route.start_x * NODE_LENGTH
        y += route.start_y * NODE_LENGTH

        for i, node in enumerate(route.nodes):
            self.draw_node(x, y, node, i == 0)

            x += node.direction[0] * node.distance * NODE_LENGTH
            y += node.direction[1] * node.distance * NODE_LENGTH

    def draw_cube_side(self, left, top, index, cube):
        if index < 3:
            x = (
                left
                + CUBE_SIDE_SIZE
                + CUBE_BLOCK_MARGIN
                + (CUBE_BLOCK_SIZE + CUBE_BLOCK_MARGIN) * index
            )
            y = top
        elif index < 6:
            x = left + CUBE_TOTAL_SIZE - CUBE_SIDE_SIZE
            y = (
                top
                + CUBE_SIDE_SIZE
                + CUBE_BLOCK_MARGIN
                + (CUBE_BLOCK_SIZE + CUBE_BLOCK_MARGIN) * (index - 3)
            )
        elif index < 9:
            x = (
                left
                + CUBE_SIDE_SIZE
                + CUBE_BLOCK_MARGIN
                + (CUBE_BLOCK_SIZE + CUBE_BLOCK_MARGIN) * (8 - index)
            )
            y = top + CUBE_TOTAL_SIZE - CUBE_SIDE_SIZE
        else:
            x = left
            y = (
                top
                + CUBE_SIDE_SIZE
                + CUBE_BLOCK_MARGIN
                + (CUBE_BLOCK_SIZE + CUBE_BLOCK_MARGIN) * (11 - index)
            )

        if index < 3 or 5 < index < 9:
            w = CUBE_BLOCK_SIZE
            h = CUBE_SIDE_SIZE
        else:
            w = CUBE_SIDE_SIZE
            h = CUBE_BLOCK_SIZE

        self.canvas.rect(x, y, w, h, CUBE_COLOR[cube][0])
        self.canvas.rect(
            x + CUBE_LINE_THICKNESS,
            y + CUBE_LINE_THICKNESS,
            w - CUBE_LINE_THICKNESS * 2,
            h - CUBE_LINE_THICKNESS * 2,
            CUBE_COLOR[cube][1],
        )

    def draw_cube_block(self, left, top, index_x, index_y, cube):
        x = y = CUBE_SIDE_SIZE + CUBE_BLOCK_MARGIN
        x += left + (CUBE_BLOCK_SIZE + CUBE_BLOCK_MARGIN) * index_x
        y += top + (CUBE_BLOCK_SIZE + CUBE_BLOCK_MARGIN) * index_y
        w = CUBE_BLOCK_SIZE
        h = CUBE_BLOCK_SIZE

        self.canvas.rect(x, y, w, h, CUBE_COLOR[cube][0])
        self.canvas.rect(
            x + CUBE_LINE_THICKNESS,
            y + CUBE_LINE_THICKNESS,
            w - CUBE_LINE_THICKNESS * 2,
            h - CUBE_LINE_THICKNESS * 2,
            CUBE_COLOR[cube][1],
        )

    def draw_cube(self, x, y, cube):
        for i in range(12):
            self.draw_cube_side(x, y, i, cube[i])

        for i in range(3):
            for j in range(3):
                self.draw_cube_block(x, y, j, i, cube[12 + i * 3 + j])

    def draw_letters(self, x, y, route):
        route_width = route.width * NODE_LENGTH
        letters = "".join([node.letters for node in route.nodes])
        letter_width, _ = self.canvas.text_size(letters, TEXT_FONT_NAME, TEXT_FONT_SIZE)

        self.canvas.text(
            x + (route_width - letter_width) / 2,
            y,
            letters,
            TEXT_FONT_NAME,
            TEXT_FONT_SIZE,
            TEXT_COLOR,
        )

    def draw_routemap(self, x, y, routemap):
        #
        # draw name
        #
        self.canvas.text(
            x + TEXT_X_OFFSET,
            y,
            "[" + routemap.name + "]",
            TEXT_FONT_NAME,
            TEXT_FONT_SIZE,
            TEXT_COLOR,
        )

        #
        # calculate offset
        #
        offset = (routemap.height * NODE_LENGTH - CUBE_TOTAL_SIZE) / 2
        cube_offset = max(offset, 0)
        route_offset = max(-offset, 0)

        #
        # draw cube
        #
        cube_y = TEXT_FONT_SIZE + TEXT_V_MARGIN + y + cube_offset
        self.draw_cube(x, cube_y, routemap.cube)

        #
        # draw letters and routes
        #
        x += CUBE_TOTAL_SIZE + CUBE_H_MARGIN

        for route in routemap.routes:
            self.draw_letters(x, y, route)

            route_y = TEXT_FONT_SIZE + TEXT_V_MARGIN + y + route_offset
            self.draw_route(x, route_y, route)

            x += route.width * NODE_LENGTH + ROUTE_H_MARGIN

    def show(self):
        self.canvas.show()

    def from_algorithm(algos_list):
        routemaps_list = [
            [RouteMap.from_letters(*algo) for algo in algos] for algos in algos_list
        ]

        #
        # create renderer
        #
        renderer_width = renderer_height = 0

        for i, routemaps in enumerate(routemaps_list):
            width = height = 0

            for j, routemap in enumerate(routemaps):
                w, h = routemap_drawing_size(routemap)
                width = max(w, width)
                height += h + (ROUTEMAP_V_MARGIN if j > 0 else 0)

            renderer_width += width + (ROUTEMAP_H_MARGIN if i > 0 else 0)
            renderer_height = max(height, renderer_height)

        renderer_width += CANVAS_H_MARGIN * 2
        renderer_height += CANVAS_V_MARGIN * 2

        renderer = Renderer(renderer_width, renderer_height)

        #
        # draw routemaps
        #
        x = CANVAS_H_MARGIN

        for routemaps in routemaps_list:
            y = CANVAS_V_MARGIN
            width = 0

            for routemap in routemaps:
                renderer.draw_routemap(x, y, routemap)

                w, h = routemap_drawing_size(routemap)
                width = max(w, width)
                y += h + ROUTEMAP_V_MARGIN

            x += width + ROUTEMAP_H_MARGIN

        return renderer
