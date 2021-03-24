import sys
from enum import Enum

import pygame

pygame.init()

# create a display surface, main game window
# NOTE: canvas, there can only be one, display by default
screen = pygame.display.set_mode(size=(400, 500))
# it knows that it needs to create a window, but doesn't know how long it should keep it
# so it creates it and then closes it
clock = pygame.time.Clock()

# surfaces = layers, we can put stuff on
# create a surface(import image/write text/create empty) + display surface
test_surface = pygame.Surface(size=(100, 200))
# rectangle
# x, y(NOTE:coordinate of the topleft, NOT the center), width, height
test_rectangle = pygame.Rect(100, 200, 100, 100)  # less processing power
# TODO, diff between rect and surface
# TODO, surface.getrect()
x_position = 200

# game loop
while True:
    # event loop: 1, up down left right 2, close the window, clicking "X"
    for event in pygame.event.get():
        # at the beginning of each loop, we try all possible events
        if event.type == pygame.QUIT:
            pygame.quit()  # the opposite of pygame.init()
            sys.exit()
    # draw all our elements

    # color->RBG tuple (255[100% of red],255,255)
    # screen.fill(pygame.Color("gold"))
    # NOTE: fill() is a method unique to screen
    # rect color is specified in draw (rect object is just a shape)
    screen.fill((175, 215, 70))
    # display on the main_display
    # x,y topleft coordinate
    # NOTE: this is how we make animation
    x_position += 1
    # screen.blit(test_surface, (x_position, 250))
    # surface, color, object
    pygame.draw.rect(screen, pygame.Color("gold"), test_rectangle)
    pygame.display.update()
    # NOTE: run as many times as possible, depends on the computer
    # for fast computer, it can run a lot more times than a slow computer
    # each computer, we move the object for different amount because of this
    clock.tick(60)  # 60 times in a sec


# snake game, creates a grid on display (move 1 grid per frame)
# how to store snakes?
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

# Assume only 1 snake in snake game
class SnakeGame:
    def __init__(self, game_width, game_height):
        # start from top left, going right
        self.length = 1
        self.direction = Direction.RIGHT # up left down right 
        # matrix width and height, when we draw, each grid is a cube
        self.game_width = game_width
        self.game_height = game_height
        self.snake = # double ended queue

    def move_snake(self, direction):
        # return state 
        # 1. increase length
        # 2. hit a snag
        # 3. continue moving

        # if no direction is provided or the move can not be completed, we continue
    def create_apple(self):
        # called if move_snake takes the apple
# after each user move
# compute possible result
# then draw
