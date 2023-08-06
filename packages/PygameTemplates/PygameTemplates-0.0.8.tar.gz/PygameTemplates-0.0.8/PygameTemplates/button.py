from PygameTemplates.text_field_base import *


class Button(Base):
    def __init__(self, x, y, width, height, fit_text_options=None, base_colour=(255, 255, 255), message="", font_style="arial", font_size=None, font_colour=(0, 0, 0), bold=False, italics=False, antialias=True, horizontal_alignment="left", verticle_alignment="top", border_width=2, border_colour=(0, 0, 0), top_left=0, top_right=0, bottom_left=0, bottom_right=0):
        super().__init__(x, y, width, height, fit_text_options, base_colour, message, font_style, font_size, font_colour, bold, italics, antialias, horizontal_alignment, verticle_alignment, border_width, border_colour, top_left, top_right, bottom_left, bottom_right)

    def draw(self, wn):
        self._draw(wn)

    def click(self, mouse_pos):
        return self._select(mouse_pos)
