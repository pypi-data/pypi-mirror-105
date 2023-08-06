from PygameTemplates.text_field_base import *


class Label(Base):
    def __init__(self, x, y, width, height, moveable=False, fit_text_options=None, base_colour=(255, 255, 255), message="", font_style="arial", font_size=None, font_colour=(0, 0, 0), bold=False, italics=False, antialias=True, horizontal_alignment="left", verticle_alignment="top", border_width=2, border_colour=(0, 0, 0), top_left=0, top_right=0, bottom_left=0, bottom_right=0):
        super().__init__(x, y, width, height, fit_text_options, base_colour, message, font_style, font_size, font_colour, bold, italics, antialias, horizontal_alignment, verticle_alignment, border_width, border_colour, top_left, top_right, bottom_left, bottom_right)
        self.moveable = moveable
        self.picked_up = False
        self.offset = (0, 0)
        self.point = None
        self.grabbed = False

    def draw(self, wn):
        self._draw(wn)

    def set_mouse(self, mouse_pos):
        if self.moveable:
            if not self.grabbed:
                selected = self._select(mouse_pos)
                if selected == "box":
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
                    self.point = None

                elif selected == "border":
                    if self.x - self.border_width <= mouse_pos[0] <= self.x + self.width * 0.1:
                        if self.y - self.border_width <= mouse_pos[1] <= self.y + self.height * 0.1:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENWSE)
                            self.point = "nw"
                        elif self.y + self.height * 0.9 <= mouse_pos[1] <= self.y + self.height + self.border_width:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENESW)
                            self.point = "sw"
                        else:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
                            self.point = "w"

                    elif self.x + self.width * 0.9 <= mouse_pos[0] <= self.x + self.width + self.border_width:
                        if self.y - self.border_width <= mouse_pos[1] <= self.y + self.height * 0.1:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENESW)
                            self.point = "ne"
                        elif self.y + self.height * 0.9 <= mouse_pos[1] <= self.y + self.height + self.border_width:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENWSE)
                            self.point = "se"
                        else:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
                            self.point = "e"
                    else:
                        if self.y - self.border_width <= mouse_pos[1] <= self.y + self.height * 0.1:
                            self.point = "n"
                        elif self.y + self.height * 0.9 <= mouse_pos[1] <= self.y + self.height + self.border_width:
                            self.point = "s"
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)

                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.point = None

        if self.picked_up:
            self.x = mouse_pos[0] + self.offset[0]
            self.y = mouse_pos[1] + self.offset[1]

        if self.grabbed:
            self.resize(mouse_pos)

    def click(self, mouse_pos):
        cursor = pygame.mouse.get_cursor().data[0]
        if cursor == pygame.SYSTEM_CURSOR_SIZEALL:
            self.picked_up = True
            self.offset = (self.x - mouse_pos[0], self.y - mouse_pos[1])
        elif self.point is not None:
            self.grabbed = True

    def unclick(self):
        if self.picked_up:
            self.picked_up = False
        if self.grabbed:
            self.grabbed = False

    def debug(self, *args):
        if args.__contains__("pos"):
            return {"data": (self.x, self.y),
                    "string": f"x: {self.x}\ny: {self.y}"}
        
    def resize(self, mouse_pos):
        if self.point == "nw":
            moved = max(self.x - mouse_pos[0], self.y - mouse_pos[1]) - self.border_width
            self.x -= moved
            self.y -= moved
            self.width += moved
            self.height += moved
        elif self.point == "n":
            moved = self.y - mouse_pos[1] - self.border_width
            self.y -= moved
            self.height += moved
        if self.point == "ne":
            moved = max(mouse_pos[0] - (self.x + self.width), self.y - mouse_pos[1]) - self.border_width
            self.y -= moved
            self.width += moved
            self.height += moved
        if self.point == "e":
            moved = mouse_pos[0] - (self.x + self.width) - self.border_width
            self.width += moved
        if self.point == "se":
            moved = max(mouse_pos[0] - (self.x + self.width), mouse_pos[1] - (self.y + self.height)) - self.border_width
            self.width += moved
            self.height += moved
        if self.point == "s":
            moved = mouse_pos[1] - (self.y + self.height) - self.border_width
            self.height += moved
        if self.point == "sw":
            moved = max(self.x - mouse_pos[0], mouse_pos[1] - (self.y + self.height)) - self.border_width
            self.x -= moved
            self.width += moved
            self.height += moved
        if self.point == "w":
            moved = self.x - mouse_pos[0] - self.border_width
            self.x -= moved
            self.width += moved
