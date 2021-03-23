import sys

import pygame

pygame.init()

# create a display surface, main game window
screen = pygame.display.set_mode(size=(400, 500))
# it knows that it needs to create a window, but doesn't know how long it should keep it
# so it creates it and then closes it


# game loop
# NOTE: run as many times as possible, depends on the computer
# for fast computer, it can run a lot more times than a slow computer
while True:
    # event loop: 1, up down left right 2, close the window, clicking "X"
    for event in pygame.event.get():
        # at the beginning of each loop, we try all possible events
        if event.type == pygame.QUIT:
            pygame.quit()  # the opposite of pygame.init()
            sys.exit()
    # draw all our elements
    # display on the main_display
    pygame.display.update()
