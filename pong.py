# used to close the program
import sys

import pygame


class Ball:
    def __init__(self, width, color, coordinate, initial_movement):
        self.width = width
        self.color = color
        # one single ball object, mutable
        self.ball = pygame.Rect(coordinate[0], coordinate[1], self.width, self.width)
        # use vector to denote speed and direction
        self.vector_x, self.vector_y = initial_movement

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.ball)

    # TODO, if we want to manage the barriers in Ball class
    def update_position(self, screen_width, screen_height):
        screen_width = screen_width - self.width
        screen_height = screen_height - self.width

        new_x = self.ball.x + self.vector_x
        new_y = self.ball.y + self.vector_y
        # if fractional, part of the ball follows the old trajectory
        # the rest follows the new trajectory
        # comment out so that left player can fight against the wall
        # if new_x < 0:
        #     self.ball.x = -new_x
        #     self.vector_x *= -1
        if new_x > screen_width:
            self.ball.x = screen_width - (new_x - screen_width)
            self.vector_x *= -1
        else:
            self.ball.x = new_x

        if new_y < 0:
            self.ball.y = -new_y
            self.vector_y *= -1
        elif new_y > screen_height:
            self.ball.y = screen_height - (new_y - screen_height)
            self.vector_y *= -1
        else:
            self.ball.y = new_y

    # if we collide with players, we change trajectory
    def hit_players(self, left_player, right_player):
        if self.ball.colliderect(left_player) or self.ball.colliderect(right_player):
            self.vector_x *= -1


# TODO add a game class


class Player:
    def __init__(self, coordinate, speed, width, height, color):
        self.width = width
        self.color = color
        self.height = height
        self.speed = speed  # how much the controller can move the ball
        self.player = pygame.Rect(coordinate[0], coordinate[1], width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.player)

    # TODO put a rectangle over the drawing surface
    def update_position(self, key, height):
        if key == pygame.K_UP and self.player.top > 0:
            self.player.top = max(self.player.top - self.speed, 0)
        elif key == pygame.K_DOWN and self.player.bottom < height:
            self.player.bottom = min(height, self.player.bottom + self.speed)


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
    (10, 5),
)

# (x,y,w,h)
PLAYER_WIDTH = 10
PLAYER_HEIGHT = 150
PLAYER_SPEED = 5
# different concept, rect, rect can be put around shape and surfaces
# like a selector in photoshop
player = Player((0, 0), PLAYER_SPEED, PLAYER_WIDTH, PLAYER_HEIGHT, LIGHT_GREY)
opponent = Player(
    (
        SCREEN_WIDTH - PLAYER_WIDTH,
        SCREEN_HEIGHT - PLAYER_HEIGHT,
    ),
    PLAYER_SPEED,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    LIGHT_GREY,
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
            # TODO, does not handle key press + key release
            # if event.type == pygame.KEYDOWN:
    # holding key does not trigger an event
    keys = pygame.key.get_pressed()
    # all the key BEING pressed
    if keys[pygame.K_UP]:
        player.update_position(pygame.K_UP, SCREEN_HEIGHT)
    elif keys[pygame.K_DOWN]:
        player.update_position(pygame.K_DOWN, SCREEN_HEIGHT)

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
    player.draw(SCREEN)
    opponent.draw(SCREEN)
    ball.update_position(SCREEN_WIDTH, SCREEN_HEIGHT)
    ball.hit_players(player.player, opponent.player)
    ball.draw(SCREEN)
    # TODO check for collision, rect1.colliderect(rect2)
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
