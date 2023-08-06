import pygame
from PygameTemplates.error_handling import CustomError

pygame.init()


class Rect:
    def __init__(self, *args):
        if len(args) == 1:
            args = args[0]

        self.x = args[0]
        self.y = args[1]
        self.width = args[2]
        self.height = args[3]

    def collide(self, *pos):
        if isinstance(pos[0], tuple) or isinstance(pos[0], list):
            x = pos[0][0]
            y = pos[0][1]
        elif len(pos) == 2:
            x = pos[0]
            y = pos[1]
        else:
            return False

        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def update(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __call__(self):
        return self.x, self.y, self.width, self.height

    def __add__(self, other):
        if isinstance(other, int):
            return self.x - other, self.y - other, self.width + other * 2, self.height + other * 2
        elif isinstance(other, Rect):
            return self.x + other.x, self.y + other.y, self.width + other.width, self.height + other.height

    def __sub__(self, other):
        if isinstance(other, int):
            return self.x + other, self.y + other, self.width - other * 2, self.height - other * 2
        elif isinstance(other, Rect):
            return self.x - other.x, self.y - other.y, self.width - other.width, self.height - other.height

    def __mul__(self, other):
        if isinstance(other, int):
            return self.x - (self.width * (other - 1) / 2), self.y - (self.height * (other - 1) / 2), self.width * other, self.height * other
        elif isinstance(other, Rect):
            return self.x * other.x, self.y * other.y, self.width * other.width, self.height * other.height

    def __truediv__(self, other):
        if isinstance(other, int):
            return self.x + (self.width * (other - 1) / 2), self.y + (self.height * (other - 1) / 2), self.width / other, self.height / other
        elif isinstance(other, Rect):
            return self.x / other.x, self.y / other.y, self.width / other.width, self.height / other.height


class Base:
    def __init__(self, x, y, width, height, fit_text_options=None, base_colour=(255, 255, 255), message="", font_style="arial", font_size=None, font_colour=(0, 0, 0), bold=False, italics=False, antialias=True, horizontal_alignment="left", verticle_alignment="top", border_width=2, border_colour=(0, 0, 0), top_left=0, top_right=0, bottom_left=0, bottom_right=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # none, text(shrinks the text), width(expands/shrinks the width of the box to fit the text), height(expands/shrinks the height of the box to fit the text), all(both width and height)
        # can be combined in tuple e.g.("text", "height")
        self.fit_text_options = fit_text_options

        self.rect_obj = Rect(self.x, self.y, self.width, self.height)
        self.base_colour = base_colour

        self.message = message
        self.font_style = font_style
        self.font_size = font_size
        self.font_colour = font_colour
        self.bold = bold
        self.italics = italics
        self.antialias = antialias
        self.horizontal_alignment = horizontal_alignment
        self.verticle_alignment = verticle_alignment

        self.border_width = border_width
        self.border_colour = border_colour

        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right

        self.finish_setup()

    def finish_setup(self):
        if self.font_size is None:
            self.font_size = self.get_font_size(self.message)

        self.fit_text(self.message)

    def fit_text(self, message):
        if not(isinstance(self.fit_text_options, tuple) or isinstance(self.fit_text_options, list)):
            self.fit_text_options = [self.fit_text_options]

        if len(self.fit_text_options) > 1 and self.fit_text_options.__contains__(None):
            raise CustomError("'fit_text_options' field cannot contain 'None' and another value")

        font = pygame.font.SysFont(self.font_style, self.font_size, bold=self.bold, italic=self.italics)
        text = font.render(message, self.antialias, self.font_colour)

        if self.fit_text_options.__contains__("width"):
            self.width = text.get_width()

        if self.fit_text_options.__contains__("height"):
            self.height = text.get_height()

        if self.fit_text_options.__contains__("all"):
            self.width = text.get_width()
            self.height = text.get_height()

        if self.fit_text_options.__contains__("text"):
            self.font_size = self.get_font_size(message)

    def get_font_size(self, message):
        font_size = 50

        if self.fit_text_options is None or self.fit_text_options.__contains__("text"):
            height = 0
            count = 0
            while height != self.height and count < 10:
                count += 1

                font = pygame.font.SysFont(self.font_style, font_size)
                text = font.render("", False, (0, 0, 0))

                height = text.get_height()
                font_size = round(self.height / text.get_height() * font_size)

            if self.fit_text_options is not None:
                font = pygame.font.SysFont(self.font_style, font_size, bold=self.bold, italic=self.italics)
                text = font.render(message, self.antialias, self.font_colour)

                if self.width < text.get_width():
                    font_size = round((self.width - 5) / text.get_width() * font_size)

        return font_size

    def _draw(self, wn):
        self.rect_obj.update(self.x, self.y, self.width, self.height)
        self.fit_text(self.message)
        
        # box
        if self.base_colour:
            pygame.draw.rect(wn, self.base_colour, self.rect_obj(), border_top_left_radius=self.top_left, border_top_right_radius=self.top_right, border_bottom_left_radius=self.bottom_left, border_bottom_right_radius=self.bottom_right)
        # border
        if self.border_colour:
            pygame.draw.rect(wn, self.border_colour, self.rect_obj + self.border_width // 2, width=self.border_width, border_top_left_radius=self.top_left, border_top_right_radius=self.top_right, border_bottom_left_radius=self.bottom_left, border_bottom_right_radius=self.bottom_right)
        
        # text
        if self.message:
            font = pygame.font.SysFont(self.font_style, self.font_size, bold=self.bold, italic=self.italics)
            text = font.render(self.message, self.antialias, self.font_colour)

            text_pos = [self.x, self.y]
            if self.horizontal_alignment == "center":
                text_pos[0] = (self.x + self.width / 2) - (text.get_width() / 2)
            elif self.horizontal_alignment == "right":
                text_pos[0] = self.x + self.width - text.get_width()
            if self.verticle_alignment == "center":
                text_pos[1] = (self.y + self.height / 2) - (text.get_height() / 2)
            elif self.verticle_alignment == "bottom":
                text_pos[1] = self.y + self.height - text.get_height()

            wn.blit(text, text_pos)

    def _select(self, mouse_pos):
        self.rect_obj.update(self.x, self.y, self.width, self.height)

        if self.rect_obj.collide(mouse_pos):
            return "box"

        border_rect = Rect(self.rect_obj + self.border_width)
        if border_rect.collide(mouse_pos):
            return "border"

        return False
