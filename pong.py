# used to close the program
import sys

import pygame


class Ball:
    def __init__(self, width, color, coordinate, initial_movement):
        self.width = width
        self.color = color
        # one single ball object, mutable
        self.rect = pygame.Rect(coordinate[0], coordinate[1], self.width, self.width)
        # use vector to denote speed and direction
        self.vector_x, self.vector_y = initial_movement

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def get_rect(self):
        return self.rect

    # TODO, if we want to manage the barriers in Ball class
    def update_position(self, screen_width, screen_height):
        screen_width = screen_width - self.width
        screen_height = screen_height - self.width

        self.rect.x += self.vector_x
        new_y = self.rect.y + self.vector_y
        # if fractional, part of the ball follows the old trajectory
        # the rest follows the new trajectory
        # comment out so that left player can fight against the wall

        if new_y < 0:
            self.rect.y = -new_y
            self.vector_y *= -1
        elif new_y > screen_height:
            self.rect.y = screen_height - (new_y - screen_height)
            self.vector_y *= -1
        else:
            self.rect.y = new_y

    # if we collide with players, we change trajectory
    def hit_players(self, left_player, right_player):
        if self.rect.colliderect(left_player) or self.rect.colliderect(right_player):
            self.vector_x *= -1


# TODO add a game class


class Player:
    def __init__(self, coordinate, speed, width, height, color):
        self.width = width
        self.color = color
        self.height = height
        self.speed = speed  # how much the controller can move the ball
        self.rect = pygame.Rect(coordinate[0], coordinate[1], width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def get_rect(self):
        return self.rect

    def update_position(self, height):
        # NOTE: alternative
        # event.type = pygame.KEYDOWN, event.key == pygame.KEY_DOWN -> set player movement, keyup -> player stops
        # holding key does not trigger an event
        keys = pygame.key.get_pressed()
        # all the key BEING pressed
        if keys[pygame.K_UP]:
            self.rect.top = max(self.rect.top - self.speed, 0)
        elif keys[pygame.K_DOWN]:
            self.rect.bottom = min(height, self.rect.bottom + self.speed)


class AIPlayer(Player):
    def __init__(self, coordinate, speed, width, height, color, ball_rect):
        super().__init__(coordinate, speed, width, height, color)
        self.ball_rect = ball_rect

    def update_position(self, height):
        if self.rect.centery > self.ball_rect.centery:
            self.rect.top = max(self.rect.top - self.speed, 0)
        elif self.rect.centery < self.ball_rect.centery:
            self.rect.bottom = min(height, self.rect.bottom + self.speed)


# NOTE: how rect update all attributes with one function
class ShunRect:
    def __init__(self, top, bottom):
        self.top = top
        self.bottom = bottom

    # intercept attribute assignment
    def __setattr__(self, key, value):
        if key not in self.__dict__:
            self.__dict__[key] = value  # constructor init
        elif key == "top":
            diff = value - self.__dict__["top"]
            self.__dict__[key] = value
            # assume there's bottom already
            self.__dict__["bottom"] = self.__dict__["bottom"] + diff
            # NOTE to avoid recursion self.top = value


shunrect = ShunRect(100, 50)
shunrect.top = 1000
print(shunrect.bottom)

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
    (10, 5),  # TODO gets more difficult over time
)

# (x,y,w,h)
PLAYER_WIDTH = 10
PLAYER_HEIGHT = 150
PLAYER_SPEED = 5
# different concept, rect, rect can be put around shape and surfaces
# like a selector in photoshop
player = Player((0, 0), PLAYER_SPEED, PLAYER_WIDTH, PLAYER_HEIGHT, LIGHT_GREY)
opponent = AIPlayer(
    (
        SCREEN_WIDTH - PLAYER_WIDTH,
        SCREEN_HEIGHT - PLAYER_HEIGHT,
    ),
    PLAYER_SPEED,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    LIGHT_GREY,
    ball.rect,
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

    player.update_position(SCREEN_HEIGHT)
    opponent.update_position(SCREEN_HEIGHT)

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
    ball.hit_players(player.get_rect(), opponent.get_rect())
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
