from queue import PriorityQueue

import pygame

# capital letters for constants
WIDH = 800
WIN = pygame.display.set_mode((WIDH, WIDH))
pygame.display.set_caption("A* Path Finding Algorithm")

X_BOUND = 100
Y_BOUND = 100


class Node:
    def __init__(self, x, y):
        # pylint will warn you about accessing protected member
        self._x = x
        self._y = y
        # member fields for A*
        self._g = None
        self._h = None  # when update f = g, h, h should stays the same

    def __lt__(self, other):
        if type(self) is type(other):
            return (self._g + self._h) < (other._g + other._h)
        return False

    # __eq__ and __hash__ for hashset, check if they've already been evaluated
    # NOTE in python 3, eq ==> !ne, implied relationship
    def __eq__(self, other):
        # isinstance will cover inheritance ==> father == children
        # but children != father (not implemented)
        if type(other) is type(self):
            return self._x == other._x and self._y == other._y
        return False

    def __hash__(self):
        return hash((self._x, self._y))

    # TODO, this assumes no obstable
    def neighbors(self):
        # can only go UP,LEFT,RIGHT,DOWN
        # TODO use pygame.vector2, supports math operations
        # TODO return a generator
        return_value = []
        if self._y > 0:
            return_value.append(Node(self._x, self._y - 1))
        if self._y < Y_BOUND - 1:
            return_value.append(Node(self._x, self._y + 1))
        if self._x > 0:
            return_value.append(Node(self._x - 1, self._y))
        if self._x < X_BOUND - 1:
            return_value.append(Node(self._x + 1, self._y))
        return return_value


# assume boundary is 0,x_bound,0,y_bound
def a_star(source, destination):
    # stops when destination is reached
    # priorityqueue doesn't support decrease key...so I think it should be the same as heapq
    priority_queue = PriorityQueue()
    priority_queue.put(source)
    pq_hashset = set(source)
    visited_hashset = set()
    while not priority_queue.empty():
        next_node = priority_queue.get()
        pq_hashset.remove(next_node)
        visited_hashset.add(next_node)
        for neighbor in next_node.neighbors():
            if neighbor in visited_hashset:
                pass
            elif neighbor in pq_hashset:
                # TODO promote if necessary
            else:  # neighbor is new
                # set g and h
                neighbor._g = next_node._g + 1
                neighbor._h = abs(neighbor._x - destination._x) + abs(
                    neighbor._y - destination._y
                )
                pq_hashset.add(neighbor)
                priority_queue.put(neighbor)
