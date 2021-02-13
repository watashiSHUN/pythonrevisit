import random
# use a matrix
# [[_,_,_]
# [_,_,_]
# [_,_,_]]

class Player:
    # O, X, #, three kinds
    def __init__(self, symbol):
        self.symbol = symbol
    # takes a game state, play the next move
    # for inheritance
    def play(self, game):
        pass
    # TODO, python doesn't need the template design pattern
    # dynamic type???

# store the games
# easier to play, easier to tally
# store in matrix => easier to print (currently use this, check all lines, if one symbol ==> winner)
# empty set => easier for random computer to play
class Game:
    def __init__(self):
        self.board = [ ['_']*3 for i in range(3)]
        # used to play (pick a random point)
        # also used to calculate lines (set or list?)
        self.empty = set([(i,j) for i in range(3) for j in range(3)])
    def printBoard(self):
        for i in self.board:
            print(" ".join(i))
    # return char, winner char
    # inconclusive return None
    def determineWinner(self):
        # TODO fastest, each row, col, diagonal, has a map {'x':count}
        # rows
        for i in range(3):
            for j in range(1,3): # if 3 all equal
                candidate = True
                if self.board[i][j] == '_'  or self.board[i][j] != self.board[i][j-1]:
                    candidate = False
                    break # failed
            if candidate:
                return self.board[i][0]
        # colons
        for j in range(3):
            for i in range(1,3):
                candidate = True
                if self.board[i-1][j] == '_' or self.board[i-1][j] != self.board[i][j]:
                    candidate = False
                    break
            if candidate:
                return self.board[0][j]
        # two diagonals
        candidate = True
        for i in range(1,3):
            # j==i
            if self.board[i][i] == '_' or self.board[i][i] != self.board[i-1][i-1]:
                candidate = False
                break
        if candidate:
            return self.board[0][0]
        candidate = True
        for i in range(1,3):
            # j = 2-i
            if self.board[i][2-i] == '_' or self.board[i][2-i] != self.board[i-1][3-i]:
                candidate = False
                break
        if candidate:
            return self.board[0][2]
        return None
    # used to determine draw, or gameover
    def spots(self):
        return self.empty
    # return bool, valid play
    def play(self, symbol, coordinate):
        if coordinate in self.empty:
            self.board[coordinate[0]][coordinate[1]] = symbol
            self.empty.remove(coordinate)
            return True
        else:
            return False
# inheritance
class ComputerPlayer(Player):
    def play(self, game): # override
        # randomly pick a spot to play
        next_move = random.choice(list(game.spots()))
        # computer always play a valid move
        game.play(self.symbol, next_move)

# TODO human players
# computer players
def driver():
    # create two players
    players = {'X': ComputerPlayer('X'), 'O': ComputerPlayer('O')}
    # alternatively pass the game around players
    # at the end of each term, determine who have won
    game = Game()
    game_round = 0
    while game.spots():
        # select player
        if game_round%2 == 0:
            player = players['X']
        else:
            player = players['O']
        game_round+=1
        print("game round: ",game_round)
        player.play(game)
        game.printBoard()
        winner = game.determineWinner()
        if winner is not None:
            print("winner is ", winner)
            return
    print("game is a draw")

driver()
