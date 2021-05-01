import sys
from collections import namedtuple
from queue import PriorityQueue

import pygame

# capital letters for constants
X_BOUND = 50
Y_BOUND = 40
WIDTH = 15


# 0 not-visited,
# 1 in-queue,
# 2 visited,
# 3 part of the path
# 4 src
# 5 dst
# 6 obstacle
STATE_COLOR = ["White", "Red", "Yellow", "Green", "Gold", "Blue", "Black"]
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
        # NOTE, _state and _parent would require a map to be indexed if not set here
        # TODO use enum, each value needs a property (color)
        self._state = 0
        self._parent = None

    # When the weight is equal, we will look for tie breaker
    def __lt__(self, other):
        return True

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
                pygame.draw.rect(
                    window,
                    pygame.Color(STATE_COLOR[node_state]),
                    (node_x, node_y, WIDTH - 1, WIDTH - 1),
                )
        pygame.display.update()

    def get_node(self, x, y):
        return self._grid[x][y]

    # implicit adj list, we don't store the edges as its a waste of space
    def get_neighbors(self, node):
        # can only go UP,LEFT,RIGHT,DOWN
        # TODO use pygame.vector2, support math operations
        for x, y in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            # make sure it's within range
            neighborx = node._x + x
            neighbory = node._y + y
            if 0 <= neighborx < self._y_bound and 0 <= neighbory < self._x_bound:
                neighbor_node = self.get_node(neighborx, neighbory)
                if neighbor_node._state != 6:
                    yield neighbor_node


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
    # src_node.parent is None
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
            # TODO same as yield next()?
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
# 2 pick obstacles
# 3 start a*
generator = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # the opposite of pygame.init()
            sys.exit()
        # NOTE [0] is left mouse button, [1] is middle, [2] is right
        # cannot be if if if, need if elif otherwise every executes in one go
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            node = get_node_from_position(pos, GRID)
            if state_machine == 0:
                src = node
                src._state = 4
                state_machine = 1
            elif state_machine == 1:
                # src node is already defined, cannot override it
                if node == src:
                    continue
                dst = node
                dst._state = 5
                state_machine = 2
            elif state_machine == 2:
                if node == src or node == dst:
                    continue
                node._state = 6
                # does not update state_machine
        if state_machine == 2 and pygame.key.get_pressed()[pygame.K_SPACE]:
            generator = a_star(src, dst, GRID)
            generator_finished = False
            state_machine = 3

    if generator and not generator_finished:
        generator_finished = next(generator)

    GRID.draw(WIN)

# TODO check when its not reachable
