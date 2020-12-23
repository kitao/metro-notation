import math

from PIL import Image, ImageDraw, ImageFont

SCALE = 4
SCALE_FILTER = Image.LANCZOS


class Canvas:
    def __init__(self, width, height, color):
        self.width = int(width)
        self.height = int(height)
        self.color = color
        self.image = Image.new("RGB", (self.width * SCALE, self.height * SCALE), color)
        self.draw = ImageDraw.Draw(self.image)

    def line(self, x1, y1, x2, y2, thickness, color):
        x1 = int((int(x1) + 0.5) * SCALE)
        y1 = int((int(y1) + 0.5) * SCALE)
        x2 = int((int(x2) + 0.5) * SCALE)
        y2 = int((int(y2) + 0.5) * SCALE)
        thickness = int(thickness) * SCALE

        self.draw.line((x1, y1, x2, y2), color, thickness)

    def rect(self, x, y, width, height, color):
        x = int(x) * SCALE
        y = int(y) * SCALE
        width = int(width) * SCALE
        height = int(height) * SCALE

        self.draw.rectangle((x, y, x + width - 1, y + height - 1), color)

    def circle(self, x, y, size, color):
        x = int((int(x) + 0.5) * SCALE)
        y = int((int(y) + 0.5) * SCALE)
        size = int(size) * SCALE

        lt = int((size - 1) / 2)
        rb = int(size / 2)

        self.draw.ellipse((x - lt, y - lt, x + rb, y + rb), color)

    def text(self, x, y, text, font_name, font_size, color):
        x = int(x) * SCALE
        y = int(y) * SCALE
        font_size = int(font_size) * SCALE
        font = ImageFont.truetype(font_name, font_size)

        self.draw.text((x, y), text, font=font, fill=color)

    def text_size(self, text, font_name, font_size):
        font_size = int(font_size) * SCALE
        font = ImageFont.truetype(font_name, font_size)

        text_size = self.draw.textsize(text, font=font)

        return round(text_size[0] / SCALE), round(text_size[1] / SCALE)

    def show(self):
        self.image.resize((self.width, self.height), SCALE_FILTER).show()
