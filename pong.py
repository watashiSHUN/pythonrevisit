# used to close the program
import sys

import pygame


class Ball:
    def __init__(self, width, color, coordinate, initial_movement):
        self.width = width
        self.color = color
        self.x, self.y = coordinate
        # use vector to denote speed and direction
        self.vector_x, self.vector_y = initial_movement

    def draw(self, surface):
        # create rectangle to draw
        print(self.x, self.y)
        rect = pygame.Rect(self.x, self.y, self.width, self.width)
        pygame.draw.ellipse(surface, self.color, rect)

    # TODO, if we want to manage the barriers in Ball class
    def update_Position(self, screen_width, screen_height):
        screen_width = screen_width - self.width
        screen_height = screen_height - self.width

        new_x = self.x + self.vector_x
        new_y = self.y + self.vector_y
        # if fractional, part of the ball follows the old trajectory
        # the rest follows the new trajectory
        if new_x < 0:
            self.x = -new_x
            self.vector_x = -self.vector_x
        elif new_x > screen_width:
            self.x = screen_width - (new_x - screen_width)
            self.vector_x = -self.vector_x
        else:
            self.x = new_x

        if new_y < 0:
            self.y = -new_y
            self.vector_y = -self.vector_y
        elif new_y > screen_height:
            self.y = screen_height - (new_y - screen_height)
            self.vector_y = -self.vector_y
        else:
            self.y = new_y


# setup
pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
BACKGROUND = pygame.Color("grey12")
LIGHT_GREY = (200, 200, 200)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

BALL_WIDTH = 30
# surface, extra layer that holds material
# display surface (only1) + regular surface (infinite)

ball = Ball(
    BALL_WIDTH,
    LIGHT_GREY,
    ((SCREEN_WIDTH - BALL_WIDTH) // 2, (SCREEN_HEIGHT - BALL_WIDTH) // 2),
    (20, 10),
)

# (x,y,w,h)
PLAYER_WIDTH = 10
PLAYER_HEIGHT = 150
# different concept, rect, rect can be put around shape and surfaces
# like a selector in photoshop
player = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
opponent = pygame.Rect(
    SCREEN_WIDTH - PLAYER_WIDTH,
    SCREEN_HEIGHT - PLAYER_HEIGHT,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
)

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
    ball.update_Position(SCREEN_WIDTH, SCREEN_HEIGHT)
    ball.draw(SCREEN)
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
