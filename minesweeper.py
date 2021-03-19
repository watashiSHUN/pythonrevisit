# have a board + number of bombs
# genereate number around the bombs
# allow players to dig
import random
from enum import Enum

TileType = Enum("TileType", "NUMBER BOMB")
GameState = Enum("GameState", "WIN LOSE CONTINUE")


class Tile:
    # operation: tile.type() or something similar
    # TODO alternatively, we can use isinstance() and have multiple subclasses
    def __init__(self, tile_type):
        # tile could be undiscovered (this is display state)
        self.discovered = False  # default should be false
        self.type = tile_type
        self.num = 0
        # by definition, 0/ space just means that there's zero bombs around it
        # very consistent definition

    # tile could be a number (operation => ++)
    # tile could be a space  (operation, during setup, can change to number and space)
    # tile could be a bomb   (no operation)
    # enum vs class?
    def __str__(self):
        if self.discovered:
            if self.type is TileType.NUMBER:
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
            # noop
            return self
        self.type = TileType.NUMBER
        self.num += number
        return self


# use bfs? as an exercises, to expand a minesweeper
class Game:
    # number of bombs control the difficulty
    def __init__(self, size=5, num_bombs=2):
        self.undiscovered = (
            size ** 2
        )  # squared instead of self.undiscovered*self.undiscovered
        self.dimension = size
        self.bombs = num_bombs
        # size*size
        self.matrix = []
        # dummy init
        # [[None for j in range(self.dimension)] for i in range(self.dimension)]
        self.createNewBoard()

    def createNewBoard(self):
        # although not called repeatedly, separate it for better readability
        for i in range(self.dimension):
            # add a row
            row = []
            for j in range(self.dimension):
                row.append(Tile(TileType.NUMBER))
            self.matrix.append(row)
        # flatten the matrix, we can use index to specify which ones are mine
        # random.choices return result with sampling
        # TODO, figure out how this sampling is done
        bombs = random.sample([i for i in range(self.undiscovered)], self.bombs)

        for b in bombs:
            i, j = self.convert(b)
            self.matrix[i][j] = Tile(TileType.BOMB)
            # for your surrondings, if there's number, plus 1, if theres no number, set to 1
            self.updateSurroundings(i, j)

    def updateSurroundings(self, i, j):
        # caveat: right end +2
        # caveat: dont confuse the min max
        # max(0,x) => at least 0
        for x in range(max(0, i - 1), min(i + 2, self.dimension)):
            for y in range(max(0, j - 1), min(j + 2, self.dimension)):
                if x == i and y == j:
                    continue
                self.matrix[x][y] += 1

    def convert(self, integer):
        # return (i,j)
        return (integer // self.dimension, integer % self.dimension)

    # return a string
    def __str__(self):
        visible_board = []
        for row in self.matrix:
            visible_board.append("| ")
            visible_board.append(" | ".join([str(c) for c in row]))
            visible_board.append(" |")
            visible_board.append("\n")
        return "".join(visible_board)

    def reveal(self):
        # make all tiles discovered
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.matrix[i][j].discovered = True

    def revealPosition(self, i, j):
        self.matrix[i][j].discovered = True
        self.undiscovered -= 1

    def isUserWin(self):
        return self.undiscovered == self.bombs

    # don't do boundary check
    # stop when we hit a bomb/number>1
    # otherwise recursively explore

    # return 3 possible state
    def Play(self, i, j):
        # if already discovered
        if self.matrix[i][j].discovered:
            return GameState.CONTINUE

        if self.matrix[i][j].type is TileType.BOMB:
            return GameState.LOSE

        # either case can return a win
        if self.matrix[i][j].num > 0:
            self.revealPosition(i, j)

        # 5 if we hit a space, we will discover all tiles until the boundary
        # probably dfs, if we use bfs the intermediate queue will get huge
        if self.matrix[i][j].num == 0:
            self.revealPosition(i, j)
            for x in range(max(0, i - 1), min(i + 2, self.dimension)):
                for y in range(max(0, j - 1), min(j + 2, self.dimension)):
                    if x == i and y == j:
                        continue
                    # expand
                    self.Play(x, y)

        if self.isUserWin():
            return GameState.WIN
        else:
            return GameState.CONTINUE


if __name__ == "__main__":
    # create the game
    dimension = 5
    bombs = 2
    g = Game(size=dimension, num_bombs=bombs)
    while True:
        print(g)
        try:
            i, j = [int(x) for x in input("pick a position to dig (i,j):").split(",")]
            # sanity check
            if i < 0 or j < 0 or i >= dimension or j >= dimension:
                raise ValueError
            game_state = g.Play(i, j)
            if game_state is not GameState.CONTINUE:
                g.reveal()
                print(g)
                if game_state is GameState.WIN:
                    print("you won")
                else:
                    print("you lost")
                break
        except ValueError:  # if we don't do this, it will catch interrupt, cannot exit from interpreter
            # value error
            print("invalid input")


# TODO(minesweeper solver: https://www.geeksforgeeks.org/minesweeper-solver/?ref=leftbar-rightbar)
