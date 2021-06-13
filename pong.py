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
# surface, extra layer that holds material
# display surface (only1) + regular surface (infinite)

# different concept, rect, rect can be put around shape and surfaces
# like a selector in photoshop
ball = pygame.Rect(
    (SCREEN_WIDTH - BALL_WIDTH) // 2,
    (SCREEN_HEIGHT - BALL_WIDTH) // 2,
    BALL_WIDTH,
    BALL_WIDTH,
)

# (x,y,w,h)
PLAYER_WIDTH = 10
PLAYER_HEIGHT = 150
player = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
opponent = pygame.Rect(
    SCREEN_WIDTH - PLAYER_WIDTH,
    SCREEN_HEIGHT - PLAYER_HEIGHT,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
)

BACKGROUND = pygame.Color("grey12")
LIGHT_GREY = (200, 200, 200)

# game loop
# (react to user input,
# update the code [setup],
# then render the screen)
while True:
    # all user interation == events
    # return fetched events also discard them from the event queue
    # next event.get() will be different
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # main display surface, only a single one
    # pygame.draw ==> directly on display

    # multiple surfaces (attach to display)
    # can draw / put pictures onto a surface

    # Visuals, draw ontop of eachothers
    # rect, put around shapes/surfaces ???
    # pygame.draw(surface, color, rect)
    SCREEN.fill(BACKGROUND)
    # NOTE: pygame.draw draw directly on the display
    # NOTE: draw takes a surface, color, rectangle
    pygame.draw.rect(SCREEN, LIGHT_GREY, player)
    pygame.draw.rect(SCREEN, LIGHT_GREY, opponent)
    pygame.draw.ellipse(SCREEN, LIGHT_GREY, ball)
    pygame.draw.line(
        SCREEN,
        LIGHT_GREY,
        (SCREEN_WIDTH // 2, 0),
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT),
        2,
    )
    pygame.display.flip()
    # limits how fast the loop runs, 60fps
    # NOTE: computer do the while loop as fast as possible
    # result will then vary per machine
    clock.tick(60)
