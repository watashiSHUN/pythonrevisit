import random
import sys
from collections import deque
from enum import Enum

import pygame
from pygame.math import Vector2

pygame.init()

cell_size = 40
cell_width = 20
# create a display surface, main game window
# NOTE: canvas, there can only be one, display by default
screen = pygame.display.set_mode(size=(cell_size * cell_width, cell_size * cell_width))
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
    UP_VECTOR = Vector2(-1, 0)
    DOWN_VECTOR = UP_VECTOR * -1
    LEFT_VECTOR = Vector2(-1, 0)
    RIGHT_VECTOR = LEFT_VECTOR * -1

    def __init__(self, game_width, game_height):
        # start from top left, going right
        self.direction = Direction.RIGHT  # up left down right
        # matrix width and height, when we draw, each grid is a cube
        self.game_width = game_width
        self.game_height = game_height
        # left is tail, right is head, each entry is a tuple (x,y) coordinate in game grid
        # popleft(), append()
        # NOTE: we can obtain the length from this internal data structure, we don't need to store it
        # NOTE: vector2, 2d vectors a) access by .x .y not [0] [1] b) supports vector additions
        self.snake = deque([Vector2(0, 0)])

        # NOTE: I cannot initiate an apple here, it might bump to "apple"
        self.apple = None
        self.create_apple()

    # return boolean, False = game over
    def move_snake(self, direction=None):
        # compute next step
        if direction is None or self.same_or_opposite_direction(direction):
            direction = self.direction
        # make a turn
        next_step = self.next_step(direction, self.snake[-1])
        # also update the direction
        self.direction = direction
        # return state
        # 1. increase length
        if next_step == self.apple:
            self.update_snake(next_step, increase_length=True)
            self.create_apple()  # FIXME called outside
            return True
        # 2. hit a wall or your own body
        if self.out_of_bound(next_step) or next_step in self.snake:
            return False
        # 3. continue moving
        self.update_snake(next_step, increase_length=False)
        return True

    def same_or_opposite_direction(self, direction):
        if (direction is Direction.UP or direction is Direction.DOWN) and (
            self.direction is Direction.UP or self.direction is Direction.DOWN
        ):
            return True
        if (direction is Direction.LEFT or direction is Direction.RIGHT) and (
            self.direction is Direction.LEFT or self.direction is Direction.RIGHT
        ):
            return True
        return False

    def next_step(self, direction, previous_vector):
        if direction is Direction.UP:
            return previous_vector + self.UP_VECTOR
        elif direction is Direction.DOWN:
            return previous_vector + self.DOWN_VECTOR
        elif direction is Direction.LEFT:
            return previous_vector + self.LEFT_VECTOR
        else:
            return previous_vector + self.RIGHT_VECTOR

    def out_of_bound(self, position):
        if position.x < 0 or position.x >= self.game_width:
            return True
        if position.y < 0 or position.y >= self.game_height:
            return True
        return False

    def update_snake(self, next_step, increase_length=False):
        self.snake.append(next_step)
        if not increase_length:
            self.snake.popleft()

    def create_apple(self):
        # called if move_snake takes the apple
        # random.randint(a,b) a<=x<=b
        while True:
            next_apple = Vector2(
                random.randint(0, self.game_height - 1),
                random.randint(0, self.game_width - 1),
            )
            if next_apple not in self.snake:
                # set apple index
                self.apple = next_apple
                return

    def draw(self):
        # draw the snake and the apple on to the canvas
        pass


# after each user move
# compute possible result
# then draw
