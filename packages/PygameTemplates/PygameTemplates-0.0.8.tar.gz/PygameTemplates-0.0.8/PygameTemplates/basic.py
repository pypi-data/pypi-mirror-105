import pygame
pygame.init()

WIDTH = 600
HEIGHT = 600
wn = pygame.display.set_mode((WIDTH, HEIGHT))


def redraw():
    wn.fill((255, 255, 255))

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        redraw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False


main()
