import math

from PIL import Image, ImageDraw, ImageFont


class Canvas:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color
        self.image = Image.new("RGB", (width, height), color)
        self.draw = ImageDraw.Draw(self.image)

    def line(self, x1, y1, x2, y2, thickness, color):
        self.draw.line((x1, y1, x2, y2), color, thickness)

    def rect(self, x, y, width, height, color):
        self.draw.rectangle((x, y, x + width - 1, y + height - 1), color)

    def circle(self, x, y, diameter, color):
        lt = max(round(diameter / 2) - 1, 0)
        rb = math.floor(diameter / 2)
        self.draw.ellipse((x - lt, y - lt, x + rb, y + rb), color)

    def text(self, x, y, text, font_name, font_size, color):
        font = ImageFont.truetype(font_name, font_size)
        self.draw.text((x, y), text, font=font, fill=color)

    def text_size(self, text, font_name, font_size):
        font = ImageFont.truetype(font_name, font_size)
        return self.draw.textsize(text, font=font)

    def copy(self, x, y, canvas):
        self.image.paste(canvas.image, (x, y))

    def scale(self, scale):
        self.width = int(self.image.width * scale)
        self.height = int(self.image.height * scale)
        self.image = self.image.resize((self.width, self.height), Image.LANCZOS)

    def show(self):
        self.image.show()
