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
        self._state = 0  # 0 is not-visited, 1 is in-queue, 2 is visited, 3 is part of the path TODO use enum
        # NOTE we use this to prevent use of hash_set
        self._parent = None

    # When the weight is equal, we will look for tie breaker
    def __lt__(self, other):
        return True

    def set_parent(self, node):
        self._parent = node

    # move the following out, first number in an array
    # def __lt__(self, other):
    #     if type(self) is type(other):
    #         return (self._g + self._h) < (other._g + other._h)
    #     return False

    # __eq__ and __hash__ for hashset, check if they've already been evaluated
    # NOTE in python 3, eq ==> !ne, implied relationship
    # def __eq__(self, other):
    #     # isinstance will cover inheritance ==> father == children
    #     # but children != father (not implemented)
    #     if type(other) is type(self):
    #         return self._x == other._x and self._y == other._y
    #     return False

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
        pygame.display.update()

    def get_node(self, x, y):
        return self._grid[x][y]

    def get_neighbors(self, node):
        # TODO obstables
        # can only go UP,LEFT,RIGHT,DOWN
        # TODO use pygame.vector2, supports math operations
        # TODO return a generator
        return_value = []
        if node._y > 0:
            return_value.append(self.get_node(node._x, node._y - 1))
        if node._y < self._x_bound - 1:
            return_value.append(self.get_node(node._x, node._y + 1))
        if node._x > 0:  # moving up
            return_value.append(self.get_node(node._x - 1, node._y))
        if node._x < self._y_bound - 1:
            return_value.append(self.get_node(node._x + 1, node._y))
        return return_value


def construct_path(dest):
    # backtrace to source
    while dest is not None:
        dest._state = 3
        dest = dest._parent
        yield False


# TODO, does the name field matters for namedtuple?
# we don't store the heurstics, it needs to be recalculated
HeapEntry = namedtuple("HeapEntry", ["f", "g", "node", "parent"])


def a_star(src_x, src_y, dst_x, dst_y, grid):
    # manhattan distance
    def h(node):
        return abs(node._x - dst_x) + abs(node._y - dst_y)

    # stops when destination is reached
    # priorityqueue doesn't support decrease key...so I think it should be the same as heapq
    # prorityqueue shares queue interface, put+get()
    priority_q = PriorityQueue()
    # add a node into pq
    src_node = grid.get_node(src_x, src_y)
    src_g, src_h = 0, h(src_node)
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
        if current_node._x == dst_x and current_node._y == dst_y:
            yield from construct_path(current_node)
            break
        # expand neighbors of next_node
        new_g = current_node_g + 1
        for neighbor in grid.get_neighbors(current_node):
            if neighbor._state == 2:
                # do nothing
                pass
            else:
                neighbor_h = h(neighbor)
                # whether it's in the queue or not we just add it
                # TODO how to remove an object in the middle of the heap
                neighbor._state = 1  # enqueue
                priority_q.put((neighbor_h + new_g, new_g, neighbor, current_node))

        yield False  # makes it a generator
    yield True


WIN = pygame.display.set_mode((X_BOUND * WIDTH, Y_BOUND * WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

GRID = Grid(X_BOUND, Y_BOUND)
generator = a_star(0, 0, Y_BOUND // 2, X_BOUND - 1, GRID)
generator_finished = False
# draw loop
while True:
    # TODO is this the best way to
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # the opposite of pygame.init()
            sys.exit()

    # update and draw
    if not generator_finished:
        generator_finished = next(generator)

    GRID.draw(WIN)
