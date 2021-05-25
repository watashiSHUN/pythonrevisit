# used to close the program
import sys

import pygame

# setup
pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

BALL_WIDTH = 30
ball = pygame.Rect(
    (SCREEN_WIDTH - BALL_WIDTH) // 2,
    (SCREEN_HEIGHT - BALL_WIDTH) // 2,
    BALL_WIDTH,
    BALL_WIDTH,
)

BACKGROUND = pygame.Color("grey12")
LIGHT_GREY = (200, 200, 200)

# game loop
# (react to user input,
# update the code [setup],
# then render the screen)
while True:
    # all user interation == events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # main display surface, only a single one
    # pygame.draw ==> directly on display

    # multiple surfaces (attach to display)
    # can draw / put pictures onto a surface

    # rect, put around shapes/surfaces ???
    # pygame.draw(surface, color, rect)
    # TODO pygame.color('name') ==> returns a color object
    SCREEN.fill(BACKGROUND)
    pygame.draw.ellipse(SCREEN, LIGHT_GREY, ball)
    pygame.display.flip()
    # limits how fast the loop runs, 60fps
    # NOTE: computer do the while loop as fast as possible
    # result will then vary per machine
    clock.tick(60)
