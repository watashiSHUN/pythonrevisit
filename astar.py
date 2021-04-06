from queue import PriorityQueue

import pygame

# capital letters for constants
WIDH = 800
WIN = pygame.display.set_mode((WIDH, WIDH))
pygame.display.set_caption("A* Path Finding Algorithm")

class Node:
