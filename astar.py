import sys
from collections import namedtuple
from queue import PriorityQueue

import pygame

# capital letters for constants
X_BOUND = 50
Y_BOUND = 40
WIDTH = 15

# put them in class becuase of the comparison
# state and methods that operates on these states
class Node:
    def __init__(self, x, y):
        # pylint will warn you about accessing protected member
        # NOTE we need x,y because when pop from priority_q we don't have their index
        self._x = x
        self._y = y

        # TODO wrap it in a method, since the allowed values are a limited set
        # TODO add new color, change 2 places, state and draw...
        self._state = 0
        # 0 is not-visited,
        # 1 is in-queue,
        # 2 is visited,
        # 3 is part of the path TODO use enum
        # 4 is src
        # 5 is dst
        self._parent = None

    # When the weight is equal, we will look for tie breaker
    def __lt__(self, other):
        return True

    # TODO should parent be a property of node?
    def set_parent(self, node):
        self._parent = node

    def manhattan_distance(self, node):
        return abs(self._x - node._x) + abs(self._y - node._y)

    # __eq__ and __hash__ for hashset, check if they've already been evaluated
    # NOTE in python 3, eq ==> !ne, implied relationship
    def __eq__(self, other):
        # isinstance will cover inheritance ==> father == children
        # but children != father (not implemented)
        if type(other) is type(self):
            return self._x == other._x and self._y == other._y
        return False

    # def __hash__(self):
    #     return hash((self._x, self._y))


class Grid:
    def __init__(self, x_bound, y_bound):
        # create the grid
        self._grid = []
        self._x_bound = x_bound
        self._y_bound = y_bound

        for x in range(y_bound):
            row = []
            for y in range(x_bound):
                row.append(Node(x, y))
            self._grid.append(row)

    def draw(self, window):
        # override everything in the canvas
        # TODO draw lines on top
        window.fill(pygame.Color("Black"))

        for x in range(self._y_bound):
            for y in range(self._x_bound):
                node = self.get_node(x, y)
                node_state = node._state
                # key, node._x = x in matrix
                # node_x is x in drawing (which is y)
                node_x = node._y * WIDTH
                node_y = node._x * WIDTH
                if node_state == 0:
                    pygame.draw.rect(
                        window,
                        pygame.Color("White"),
                        (node_x, node_y, WIDTH - 1, WIDTH - 1),
                    )
                elif node_state == 1:
                    pygame.draw.rect(
                        window,
                        pygame.Color("Red"),
                        (node_x, node_y, WIDTH - 1, WIDTH - 1),
                    )
                elif node_state == 2:
                    pygame.draw.rect(
                        window,
                        pygame.Color("Yellow"),
                        (node_x, node_y, WIDTH - 1, WIDTH - 1),
                    )
                elif node_state == 3:
                    pygame.draw.rect(
                        window,
                        pygame.Color("Green"),
                        (node_x, node_y, WIDTH - 1, WIDTH - 1),
                    )
                elif node_state == 4:
                    pygame.draw.rect(
                        window,
                        pygame.Color("Gold"),
                        (node_x, node_y, WIDTH - 1, WIDTH - 1),
                    )
                elif node_state == 5:
                    pygame.draw.rect(
                        window,
                        pygame.Color("Blue"),
                        (node_x, node_y, WIDTH - 1, WIDTH - 1),
                    )
        pygame.display.update()

    def get_node(self, x, y):
        return self._grid[x][y]

    def get_neighbors(self, node):
        # TODO obstables
        # can only go UP,LEFT,RIGHT,DOWN
        # TODO use pygame.vector2, supports math operations
        if node._y > 0:
            yield self.get_node(node._x, node._y - 1)
        if node._y < self._x_bound - 1:
            yield self.get_node(node._x, node._y + 1)
        if node._x > 0:  # moving up
            yield self.get_node(node._x - 1, node._y)
        if node._x < self._y_bound - 1:
            yield self.get_node(node._x + 1, node._y)


def get_node_from_position(position, grid):
    x, y = position
    x_coordinate = y // WIDTH
    y_coordinate = x // WIDTH
    return grid.get_node(x_coordinate, y_coordinate)


def construct_path(dest):
    # backtrace to source
    while dest is not None:
        dest._state = 3
        dest = dest._parent
        yield False


# TODO, does the name field(1st argument) matter for namedtuple?
# we don't store the heurstics, it needs to be recalculated
HeapEntry = namedtuple("HeapEntry", ["f", "g", "node", "parent"])


def a_star(src_node, dst_node, grid):
    # stops when destination is reached
    # priorityqueue doesn't support decrease key...so I think it should be the same as heapq
    # prorityqueue shares queue interface, put+get()
    priority_q = PriorityQueue()
    src_g, src_h = 0, src_node.manhattan_distance(dst_node)
    priority_q.put(HeapEntry(src_g + src_h, src_g, src_node, None))
    src_node._state = 1  # enqueue

    while not priority_q.empty():
        _, current_node_g, current_node, parent = priority_q.get()
        # this would require us to separate the f and node
        if current_node._state == 2:
            # obsolete case
            continue

        # add it to visited node set
        current_node._state = 2
        current_node.set_parent(parent)
        if current_node == dst_node:
            yield from construct_path(current_node)
            break
        # expand neighbors of next_node
        new_g = current_node_g + 1
        for neighbor in grid.get_neighbors(current_node):
            if neighbor._state == 2:
                # do nothing
                pass
            else:
                neighbor_h = neighbor.manhattan_distance(dst_node)
                # whether it's in the queue or not we just add it
                # TODO how to remove an object in the middle of the heap
                neighbor._state = 1  # enqueue
                priority_q.put((neighbor_h + new_g, new_g, neighbor, current_node))

        yield False  # makes it a generator
    yield True


WIN = pygame.display.set_mode((X_BOUND * WIDTH, Y_BOUND * WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

GRID = Grid(X_BOUND, Y_BOUND)

# draw loop
# different states
state_machine = 0
# 0 pick src
src = None
# 1 pick dst
dst = None
# 2 start a*
generator = None
# 3 no input, just draw
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # the opposite of pygame.init()
            sys.exit()
        # NOTE [0] is left mouse button, [1] is middle, [2] is right
        # cannot be if if if, need if elif otherwise every executes in one go
        if pygame.mouse.get_pressed()[0]:
            if state_machine == 0:
                pos = pygame.mouse.get_pos()
                src = get_node_from_position(pos, GRID)
                src._state = 4
                state_machine = 1
            elif state_machine == 1:
                pos = pygame.mouse.get_pos()
                dst = get_node_from_position(pos, GRID)
                dst._state = 5
                state_machine = 2
            elif state_machine == 2:
                generator = a_star(src, dst, GRID)
                generator_finished = False
                state_machine = 3

    if generator and not generator_finished:
        generator_finished = next(generator)

    GRID.draw(WIN)
