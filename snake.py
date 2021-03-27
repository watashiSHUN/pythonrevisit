import random
import sys
from collections import deque
from enum import Enum

import pygame

# NOTE: check global table, if the module is already imported
# get it instead of load it again, even if you rename it
# both names are in the globals(). pygame + pygame.alias pointing to the same module
from pygame.math import Vector2


# snake game, creates a grid on display (move 1 grid per frame)
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


# Assume only 1 snake in snake game
class SnakeGame:
    # NOTE: you can have different coordinates
    # if using matrix, x is row, y is colon
    # if using game graphics, x is x coordinate (horizontal) y is y coordinate (vertical)
    # NOTE, we cannot use matrix coordinate, since when we draw, it expects graphics coordinate
    UP_VECTOR = Vector2(0, -1)
    DOWN_VECTOR = UP_VECTOR * -1
    LEFT_VECTOR = Vector2(-1, 0)
    RIGHT_VECTOR = LEFT_VECTOR * -1

    def __init__(self, game_width, game_height, game_cell):
        # start from top left, going right
        self.direction = Direction.RIGHT  # up left down right
        # matrix width and height, when we draw, each grid is a cube
        self.game_width = game_width
        self.game_height = game_height
        self.game_cell = game_cell
        # left is tail, right is head, each entry is a tuple (x,y) coordinate in game grid
        # popleft(), append()
        # NOTE: we can obtain the length from this internal data structure, we don't need to store it
        # NOTE: vector2, 2d vectors a) access by .x .y not [0] [1] b) supports vector additions
        self.snake = deque([Vector2(0, 0)])

        # NOTE: I cannot initiate an apple here, it might bump to "apple"
        self.apple = None
        self.create_apple()

    # return boolean, False = game over
    def update_snake_apple(self):
        next_step = self.next_step()
        # return state
        # 1. increase length
        if next_step == self.apple:
            self.update_snake(next_step, increase_length=True)
            self.create_apple()
            return True
        # 2. hit a wall or your own body
        if self.out_of_bound(next_step) or next_step in self.snake:
            return False
        # 3. continue moving
        self.update_snake(next_step, increase_length=False)
        return True

    def update_direction(self, direction):
        if not self.same_or_opposite_direction(direction):
            self.direction = direction  # make a turn

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

    def next_step(self):
        previous_vector = self.snake[-1]
        if self.direction is Direction.UP:
            return previous_vector + self.UP_VECTOR
        elif self.direction is Direction.DOWN:
            return previous_vector + self.DOWN_VECTOR
        elif self.direction is Direction.LEFT:
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

    def draw(self, surface):
        # draw the snake and the apple on to the canvas
        # rectangle
        # x, y(NOTE:coordinate of the topleft, NOT the center), width, height
        # TODO make apple flash
        apple_rect = pygame.Rect(
            # NOTE: the actual pixel postion = cell_index * cell_width
            self.apple.x * self.game_cell,
            self.apple.y * self.game_cell,
            self.game_cell - 1,
            self.game_cell - 1,
        )
        # surface(screen), color, object
        pygame.draw.rect(surface, pygame.Color("Red"), apple_rect)

        for snake_body in self.snake:
            snake_rect = pygame.Rect(
                # FIXME use variables to make this code more readable
                snake_body.x * self.game_cell,
                snake_body.y * self.game_cell,
                self.game_cell - 1,
                self.game_cell - 1,
            )
            pygame.draw.rect(surface, pygame.Color("Gold"), snake_rect)


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
# TODO, diff between rect and surface
# TODO, surface.getrect()
x_position = 200

# user event
# NOTE this controls the object speed, how often we move the snake
SCREEN_UPDATE = pygame.USEREVENT
# Create a timer event every 150milliseconds
# put it in event queue
pygame.time.set_timer(SCREEN_UPDATE, 500)

s = SnakeGame(cell_width, cell_width, cell_size)
# game loop
while True:
    # event loop: 1, up down left right 2, close the window, clicking "X"
    for event in pygame.event.get():
        # at the beginning of each loop, we try all possible events
        if event.type == pygame.QUIT:
            pygame.quit()  # the opposite of pygame.init()
            sys.exit()
        # add a timer event, for every interval, move snake
        if event.type == SCREEN_UPDATE:
            # 2. update the game state
            if not s.update_snake_apple():
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN:
            # 1. record the change direction as soon as we detect user input
            if event.key == pygame.K_UP:
                s.update_direction(Direction.UP)
            elif event.key == pygame.K_DOWN:
                s.update_direction(Direction.DOWN)
            elif event.key == pygame.K_LEFT:
                s.update_direction(Direction.LEFT)
            elif event.key == pygame.K_RIGHT:
                s.update_direction(Direction.RIGHT)
            # change direction, but does not move the snake yet

    # color->RBG tuple (255[100% of red],255,255)
    # screen.fill(pygame.Color("gold"))
    # NOTE: fill() is a method unique to screen
    # NOTE: drawing order matters, always draw the bottom layer, the backdraw, otherwise it might override the others
    # rect color is specified in draw (rect object is just a shape)

    # TODO, if no update event, do we still want to draw?
    # 3. draw
    screen.fill((175, 215, 70))
    s.draw(screen)
    pygame.display.update()

    # NOTE: run as many times as possible, depends on the computer
    # for fast computer, it can run a lot more times than a slow computer
    # each computer, we move the object for different amount because of this
    clock.tick(60)  # 60 frames per second


# after each user move
# compute possible result
# then draw
