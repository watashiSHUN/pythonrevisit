from queue import PriorityQueue

import pygame

# capital letters for constants
WIDH = 800
WIN = pygame.display.set_mode((WIDH, WIDH))
pygame.display.set_caption("A* Path Finding Algorithm")

X_BOUND = 100
Y_BOUND = 100
WIDTH = 20

# put them in class becuase of the comparison
# state and methods that operates on these states
class Node:
    def __init__(self, x, y):
        # pylint will warn you about accessing protected member
        # NOTE we need x,y because when pop from priority_q we don't have their index
        self._x = x
        self._y = y

        # TODO wrap it in a method, since the allowed values are a limited set
        self._state = 0  # 0 is not-visited, 1 is in-queue, 2 is visited, TODO use enum
        # NOTE we use this to prevent use of hash_set
        # TODO self._parent (in the shortest path)

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

        for y in range(y_bound):
            row = []
            for x in range(x_bound):
                row.append(Node(x, y))
            self._grid.append(row)

    def draw(self, window):
        # override everything in the canvas
        window.fill(pygame.Color.WHITE)

        for y in range(self._y_bound):
            for x in range(self._x_bound):
                node = self.get_node(x, y)
                node_state = node._state
                node_x = node._x * WIDTH
                node_y = node._y * WIDTH
                if node_state == 0:
                    pygame.draw.rect(
                        window,
                        pygame.Color.WHITE,
                        (node_x, node_y, WIDTH - 1, WIDTH - 1),
                    )
                elif node_state == 1:
                    pygame.draw.rect(
                        window, pygame.Color.RED, (node_x, node_y, WIDTH - 1, WIDTH - 1)
                    )
                elif node_state == 2:
                    pygame.draw.rect(
                        window,
                        pygame.Color.YELLOW,
                        (node_x, node_y, WIDTH - 1, WIDTH - 1),
                    )
        # TODO draw lines on top
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
        if node._y < self._y_bound - 1:
            return_value.append(self.get_node(node._x, node._y + 1))
        if node._x > 0:
            return_value.append(self.get_node(node._x - 1, node._y))
        if node._x < self._x_bound - 1:
            return_value.append(self.get_node(node._x + 1, node._y))
        return return_value


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
    priority_q.put((src_g + src_h, src_g, src_h, src_node))
    src_node._state = 1  # enqueue

    while not priority_q.empty():

        _, next_node_g, next_node_h, next_node = priority_q.get()
        # this would require us to separate the f and node
        if next_node._state == 2:
            # obsolete case
            continue

        next_node._state = 2  # visited
        if next_node._x == dst_x and next_node._y == dst_y:
            # TODO reconstruct the path
            return next_node_g
        new_g = next_node_g + 1
        for neighbor in grid.get_neighbor(next_node):
            if neighbor._state == 2:
                # do nothing
                pass
            elif neighbor._state == 1:
                # TODO we will not have neighbor._g
                neighbor_h = h(neighbor)
                priority_q.put((neighbor_h + new_g, new_g, neighbor_h, neighbor))
                # instead update, we just insert,
                # at pop, check if its visited (if so ignore)
                # runing time will go up
                # TODO how to remove an object in the middle of the heap
            else:  # neighbor is not visited
                # set g and h
                # NOTE all neighbor._g is the same, they are one cube away from current
                neighbor_h = h(neighbor)
                neighbor._state = 1  # enqueue
                priority_q.put((neighbor_h + new_g, new_g, neighbor_h, neighbor))
