from PygameTemplates.text_field_base import *


class TextBox(Base):
    def __init__(self, x, y, width, height, prompt="", cursor_gap=None, cursor_speed=50, cursor_width=2, cursor_height=None, cursor_colour=(0, 0, 0), fit_text_options=None, base_colour=(255, 255, 255), message="", font_style="arial", font_size=None, font_colour=(0, 0, 0), bold=False, italics=False, antialias=True, horizontal_alignment="left", verticle_alignment="top", border_width=2, border_colour=(0, 0, 0), top_left=0, top_right=0, bottom_left=0, bottom_right=0):
        super().__init__(x, y, width, height, fit_text_options, base_colour, message, font_style, font_size, font_colour, bold, italics, antialias, horizontal_alignment, verticle_alignment, border_width, border_colour, top_left, top_right, bottom_left, bottom_right)
        self.prompt = prompt

        self.selected = False
        self.cursor_state = True
        self.cursor_gap = cursor_gap
        self.cursor_speed = cursor_speed

        self.cursor_width = cursor_width
        self.cursor_height = cursor_height
        self.cursor_colour = cursor_colour

        self.cycle = 0

    def draw(self, wn):
        self._draw(wn)

        if self.message == "" and not self.selected:
            self.fit_text(self.prompt)
            font = pygame.font.SysFont(self.font_style, self.font_size, bold=self.bold, italic=self.italics)
            text = font.render(self.prompt, self.antialias, self.font_colour)

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

        if self.selected:
            self.cycle += 1
            if self.cycle % self.cursor_speed == 0:
                self.cursor_state = not self.cursor_state

            if self.cursor_state:
                font = pygame.font.SysFont(self.font_style, self.font_size, bold=self.bold, italic=self.italics)
                text = font.render(self.message, self.antialias, self.font_colour)

                if self.cursor_height is None:
                    cursor_height = text.get_height()
                else:
                    cursor_height = self.cursor_height

                if self.cursor_gap is None:
                    if self.message:
                        cursor_gap = 5 / len(self.message)
                    else:
                        cursor_gap = 5
                else:
                    cursor_gap = self.cursor_gap

                start_pos = (self.x + cursor_gap + text.get_width(), self.y + cursor_gap)
                end_pos = (self.x + cursor_gap + text.get_width(), self.y + cursor_height - cursor_gap)

                pygame.draw.line(wn, self.cursor_colour, start_pos, end_pos, self.cursor_width)

    def click(self, mouse_pos):
        if self._select(mouse_pos):
            self.selected = True
            self.cursor_state = True
            self.cycle = 0
        else:
            self.selected = False

    def key_down(self, key):
        if self.selected:
            if key.key == pygame.K_BACKSPACE:
                self.message = self.message[:-1]
            elif key.key == pygame.K_RETURN or key.key == pygame.K_KP_ENTER:
                self.selected = False
                return True
            else:
                self.message += key.unicode
            return False
