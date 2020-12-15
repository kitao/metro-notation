import math

from PIL import Image, ImageDraw, ImageFont


class Canvas:
    def __init__(self, width, height, color):
        self.image = Image.new("RGB", (width, height), color)
        self.draw = ImageDraw.Draw(self.image)

    def line(self, x1, y1, x2, y2, width, color):
        self.draw.line((x1, y1, x2, y2), color, width)

    def circle(self, x, y, width, color):
        lt = max(round(width / 2) - 1, 0)
        rb = math.floor(width / 2)
        self.draw.ellipse((x - lt, y - lt, x + rb, y + rb), color)

    def text(self, x, y, text, font_name, font_size, color):
        font = ImageFont.truetype(font_name, font_size)
        self.draw.text((x, y), text, font=font, fill=color)

    def text_size(self, text, font_name, font_size):
        font = ImageFont.truetype(font_name, font_size)
        return self.draw.textsize(text, font=font)

    def scale(self, scale):
        width = int(self.image.width * scale)
        height = int(self.image.height * scale)
        self.image = self.image.resize((width, height), Image.LANCZOS)

    def show(self):
        self.image.show()
