# have a board + number of bombs
# genereate number around the bombs
# allow players to dig
import random
from enum import Enum

TileType = Enum('TileType', 'SPACE NUMBER BOMB')

class Tile:
    # operation: tile.type() or something similar
    # TODO alternatively, we can use isinstance() and have multiple subclasses
    def __init__(self, tile_type):
        # tile could be undiscovered (this is display state)
        self.discovered = False # default should be false
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

    # __add__, any number is allowed, need to check input type
    # add semantically imply that the underlying number is unmodified
    # += 1 makes more sense in this case, butx+=y => x = x+y or x = x.__iadd__(y)
    # both __add__ and __iadd__ needs to return a value
    # return self actually does not create a new object as opposed to add
    # "rebinding"
    def __iadd__(self, number):
        # TODO check number type
        if self.type is TileType.BOMB:
            #noop
            return self
        self.type = TileType.NUMBER
        self.num += number
        return self

# use bfs? as an exercises, to expand a minesweeper
class Game:
    def __init__(self, size):
        self.undiscovered = size*size
        self.dimension = size
        # size*size
        self.matrix = []
        for i in range(size):
            # add a row
            row = []
            for j in range(size):
                row.append(Tile(TileType.SPACE))
            self.matrix.append(row)
        # flatten the matrix, we can use index to specify which ones are mine
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
                self.matrix[r][c] += 1

    def convert(self, integer):
        # return (i,j)
        return(integer//self.dimension, integer%self.dimension)

    def print(self):
        for row in self.matrix:
            print("|"," | ".join([str(c) for c in row]),"|")
    
    def reveal(self):
        # make all tiles discovered
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.matrix[i][j].discovered = True

    def expand(self,i,j):
        # base case
        # hit a boundary
        if i < 0 or i >= self.dimension or j < 0 or j >= self.dimension:
            return
        if self.matrix[i][j].discovered: # already processed
            return
        tile_type = self.matrix[i][j].type
        self.revealPosition(i,j)
        # cannot reach any where from a number
        if tile_type is TileType.NUMBER:
            # end
            return
        # recurse, up/down/left/right
        # must be space
        assert(tile_type is TileType.SPACE)
        for x,y in [(1,0),(-1,0),(0,1),(0,-1)]:
            self.expand(i+x,j+y)

    def revealPosition(self, i,j):
        self.matrix[i][j].discovered = True
        self.undiscovered -= 1
    
    def isUserWin(self):
        self.undiscovered == self.dimension

    def Play(self, i,j): # discover a tile
        # sanity check
        if 0 > i or i >= self.dimension:
            print(f"out of bound, 0 <= i < {self.dimension}")
            return False
        # 1 if out of bound, return false
        if 0 > j or j >= self.dimension:
            print(f"out of bound, 0 <= j < {self.dimension}")
            return False
        # 2 if already discovered, return false
        if self.matrix[i][j].discovered:
            print(f"already played {(i,j)}")
            return False
        # 3 if bomb return True (gg)
        tile_type = self.matrix[i][j].type
        if tile_type is TileType.BOMB:
            self.revealPosition(i,j)
            print("ooops, you lost")
            return True
        # anything below can be the winning condition
        # 4 if we hit a number
        if tile_type is TileType.NUMBER:
            self.revealPosition(i,j)
        # 5 if we hit a space, we will discover all tiles until the boundary
        # probably dfs, if we use bfs the intermediate queue will get huge
        elif tile_type is TileType.SPACE:
            self.expand(i,j)
        if self.isUserWin():
            print("you won")
            return True
        else:
            return False

if __name__ == "__main__":
    g = Game(5)
    while True:
        g.print()
        i,j = [int(x) for x in input("pick a position to dig (i,j):").split(',')]
        if g.Play(i,j):
            g.reveal()
            g.print()
            break




