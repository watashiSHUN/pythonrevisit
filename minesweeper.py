# have a board + number of bombs
# genereate number around the bombs
# allow players to dig
import random
from enum import Enum

class TileType(Enum):
    SPACE = 1
    NUMBER = 2
    BOMB = 3

class Tile:
    # operation: tile.type() or something similar
    # TODO alternatively, we can use isinstance() and have multiple subclasses
    def __init__(self, tile_type):
        # tile could be undiscovered (this is display state)
        self.discovered = True # default should be false
        self.type = tile_type
        self.num = 0 # TODO wasted for the other 2 types

    # tile could be a number (operation => ++)
    # tile could be a space  (operation, during setup, can change to number and space)
    # tile could be a bomb   (no operation)
    # enum vs class?
    def __str__(self):
        if self.discovered:
            if self.type is TileType.SPACE:
                return "_"
            elif self.type is TileType.NUMBER:
                return str(self.num)
            else:
                return "*"
        else:
            return " "

    # TODO dunder method
    def increment(self):
        if self.type is TileType.NUMBER:
            self.num += 1
        elif self.type is TileType.SPACE:
            self.type = TileType.NUMBER
            self.num += 1
        # else do nothing, if its a bomb, we cannot update

    def isBomb(self):
        return self.type is TileType.BOMB

# use bfs to expand a minesweeper
class Game:
    def __init__(self, size):
        self.dimension = size
        # size*size
        self.matrix = []
        for i in range(size):
            # add a row
            row = []
            for j in range(size):
                row.append(Tile(TileType.SPACE))
            self.matrix.append(row)
        # flatten thematrix, we can use index to specify which ones are mine
        # random.choices return result with sampling
        bombs = random.sample([i for i in range(size*size)], size)

        for b in bombs:
            i,j = self.convert(b)
            self.matrix[i][j] = Tile(TileType.BOMB)
            # for your surrondings, if there's number, plus 1, if theres no number, set to 1
            self.updateSurroundings(i,j)

    def updateSurroundings(self, i,j):
        # get the squares that is around (i,j)
        const = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for r_adjust, c_adjust in const:
            r = i+r_adjust
            c = j+c_adjust
            if (0 <= r < self.dimension and 0 <= c < self.dimension):
                self.matrix[r][c].increment()

    def convert(self, integer):
        # return (i,j)
        return(integer//self.dimension, integer%self.dimension)
        
    def print(self):
        for row in self.matrix:
            print("|"," | ".join([str(c) for c in row]),"|")

if __name__ == "__main__":
    g = Game(10)
    g.print()



