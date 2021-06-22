# used to close the program
import math
import random
import sys
import time

import pygame


# TODO add a game class
# TODO separate them to different classes
class DrawableRect:
    def __init__(self, coordinate, width, height, color):
        self.color = color
        self.rect = pygame.Rect(coordinate[0], coordinate[1], width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def get_rect(self):
        return self.rect


class Ball(DrawableRect):
    def __init__(self, width, color, coordinate, initial_movement):
        super().__init__(coordinate, width, width, color)
        self.init_coordinate = coordinate
        self.vector = initial_movement

    # draw ellipse instead of rect
    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    # players are not moving, their positions are fixed
    # return None or game winner
    def update_position(self, surface, left_player, right_player):
        # update the position if current_time > start_time or start_time is None
        start_time = self.__dict__.get("start_time", None)
        if start_time is not None and time.time() < start_time:
            return
        # 1) calculate the position without colision
        # 2) if there's collision, fix the trajectory
        # 3) check again, if out of bound, BREAK

        # 1)
        # return a new rectangle with the new position
        new_rect = self.rect.move(self.vector)
        # 2)
        # 2.1) y axis
        surface_rect = surface.get_rect()
        # python assignment doesn't return (unlike c/c++) if x=y vs if x==y
        if surface_rect.top - new_rect.top > 0:
            new_rect.move_ip(0, (surface_rect.top - new_rect.top) * 2)  # move down
            self.vector.y *= -1
        elif new_rect.bottom - surface_rect.bottom > 0:
            new_rect.move_ip(0, -(new_rect.bottom - surface_rect.bottom) * 2)  # move up
            self.vector.y *= -1
        # 2.2) x axis
        if new_rect.colliderect(left_player.get_rect()):
            new_rect.move_ip(
                (left_player.get_rect().right - new_rect.left) * 2, 0
            )  # move right
            self.vector.x *= -1
        elif new_rect.colliderect(right_player.get_rect()):
            new_rect.move_ip(
                -(new_rect.right - right_player.get_rect().left) * 2, 0
            )  # move left
            self.vector.x *= -1
        # 3)
        if not surface_rect.contains(new_rect):
            # determine the loser (intersect left or right)
            self.rect.x = self.init_coordinate[0]
            self.rect.y = self.init_coordinate[1]
            # time.time() return in seconds
            # pygame.time.get_ticks() return ms, since pygame.init()
            self.start_time = time.time() + 3
            # random trajectory
            # TODO display trajectory
            while True:
                self.vector.rotate_ip(random.uniform(0, 360))
                if abs(self.vector.x) > 2:
                    break
            return (
                right_player
                if not surface_rect.collidepoint(new_rect.midleft)
                else left_player
            )
        else:
            # self.vector is already updated
            self.rect = new_rect


class Player(DrawableRect):
    def __init__(self, coordinate, speed, width, height, color):
        super().__init__(coordinate, width, height, color)
        self.speed = speed  # baisically vector_y
        self.score = 0  # each player has a score

    def update_position(self, surface):
        # NOTE: alternative
        # event.type = pygame.KEYDOWN, event.key == pygame.KEY_DOWN -> set player movement, keyup -> player stops
        # holding key does not trigger an event
        keys = pygame.key.get_pressed()
        # all the key BEING pressed
        if keys[pygame.K_UP]:
            self.rect.top = max(self.rect.top - self.speed, 0)
        elif keys[pygame.K_DOWN]:
            self.rect.bottom = min(surface.get_height(), self.rect.bottom + self.speed)

    def update_score(self):
        self.score += 1

    # override
    def draw(self, surface):
        # create font objects
        font = pygame.font.Font("freesansbold.ttf", 500)
        # NOTE create a txt surface
        font_surface = font.render(f"{self.score}", True, SUPER_LIGHT_GREY)
        font_rect = font_surface.get_rect()
        font_rect.center = (
            surface.get_width()
            * (1 if self.rect.x < surface.get_width() // 2 else 3)
            // 4,
            surface.get_height() // 2,
        )
        # put a surface onto another, blit
        SCREEN.blit(font_surface, font_rect)
        # call parent
        super().draw(surface)


# TODO smarter AI that predicts the future
class AIPlayer(Player):
    def update_position(self, surface, ball_rect):
        if self.rect.centery > ball_rect.centery:
            self.rect.top = max(self.rect.top - self.speed, 0)
        elif self.rect.centery < ball_rect.centery:
            self.rect.bottom = min(surface.get_height(), self.rect.bottom + self.speed)


# setup
pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
BACKGROUND = pygame.Color("grey12")
LIGHT_GREY = (200, 200, 200)
SUPER_LIGHT_GREY = (50, 50, 50)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

BALL_WIDTH = 30
# surface, extra layer that holds material
# display surface (only1) + regular surface (infinite)

ball = Ball(
    BALL_WIDTH,
    LIGHT_GREY,
    ((SCREEN_WIDTH - BALL_WIDTH) // 2, (SCREEN_HEIGHT - BALL_WIDTH) // 2),
    pygame.math.Vector2(10, 5),  # TODO gets more difficult over time
    # TODO winner use the mouse to control the destination
)

# (x,y,w,h)
PLAYER_WIDTH = 10
PLAYER_HEIGHT = 150
PLAYER_SPEED = 5
# different concept, rect, rect can be put around shape and surfaces
# like a selector in photoshop
player = Player((0, 0), PLAYER_SPEED, PLAYER_WIDTH, PLAYER_HEIGHT, LIGHT_GREY)
# TODO, make copy constructor
opponent = AIPlayer(
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

    # update position of the drawables
    player.update_position(SCREEN)
    opponent.update_position(SCREEN, ball.get_rect())
    winner = ball.update_position(SCREEN, player, opponent)
    if winner is player:
        player.update_score()
    if winner is opponent:
        opponent.update_score()

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
