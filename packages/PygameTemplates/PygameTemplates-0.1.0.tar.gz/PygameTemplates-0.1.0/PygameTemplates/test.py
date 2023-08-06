from button import Button
import pygame
pygame.init()

WIDTH = 600
HEIGHT = 600
wn = pygame.display.set_mode((WIDTH, HEIGHT))


def redraw(box):
    wn.fill((255, 255, 255))

    box.draw(wn)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    box = TextBox(100, 100, 100, 100, prompt="username", fit_text_options="text")
    while run:
        clock.tick(60)
        redraw(box)

        # box.set_mouse(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                box.key_down(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                box.click(pygame.mouse.get_pos())
            # if event.type == pygame.MOUSEBUTTONUP:
            #     if box.picked_up:
            #         print(box.debug("pos")["data"])
            #     box.unclick()


main()
