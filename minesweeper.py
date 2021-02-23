# have a board + number of bombs
# genereate number around the bombs
# allow players to dig
import random

class Tile:
    pass
    ### tile could be undiscovered(this is display state)
    # tile could be a number
    # tile could be a space
    # tile could be a bomb
    # TODO(TOSTR method)

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
                row.append(' ')
            self.matrix.append(row)
        # flatten thematrix, we can use index to specify which ones are mine
        # random.choices return result with sampling
        bombs = random.sample([i for i in range(size*size)], size)
        print(bombs)
        for b in bombs:
            i,j = self.convert(b)
            self.matrix[i][j] = '*'
            # for your surrondings, if there's number, plus 1, if theres no number, set to 1
            self.updateSurroundings(i,j)
    def updateSurroundings(self, i,j):
        # get the squares that is around (i,j)
        const = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for r_adjust, c_adjust in const:
            r = i+r_adjust
            c = j+c_adjust
            if (0 <= r < self.dimension and 0 <= c < self.dimension):
                fetch = self.matrix[r][c]
                if fetch == ' ':
                    self.matrix[r][c] = str(1)
                elif fetch != '*':
                    # must be an integer
                    self.matrix[r][c] = str(int(fetch)+1) 
    def convert(self, integer):
        # return (i,j)
        return(integer//self.dimension, integer%self.dimension)
    def print(self):
        for row in self.matrix:
            print("|"," | ".join(row),"|")

if __name__ == "__main__":
    g = Game(5)
    g.print()




