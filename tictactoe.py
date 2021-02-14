import random

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

# inheritance
# computerplayer __init__(): player.__init__(self,....) => pass it to parent constructor, call it like class function
# or call super().__init__(), no need self
# add __xyz, private member variables
# TODO, then why the inheritance
# since we are calling parent constructor, we get parent member variable self.parent_field...
class ComputerPlayer(Player):
    def play(self, game): # override
        # randomly pick a spot to play
        # you can not index into a set, only array
        next_move = random.choice(list(game.spots()))
        # computer always play a valid move
        game.play(self.symbol, next_move)

class HumanPlayer(Player):
    def play(self, game):
        # expect i,j
        while True:
            user_input = input("coordinate(expected: i,j): ")
            i,j = user_input.split(',')
            coord = (int(i),int(j))
            if game.play(self.symbol, coord):
                return
            print("invalid input")

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
        self.row =[{},{},{}] # maps => {'x': how many}
        self.col =[{},{},{}]
        self.diagonal = [{},{}]

    def printBoard(self):
        for i in self.board:
            print(" ".join(i))
    # return winner char
    # inconclusive return None
    def determineWinner(self):
        def helper(*iterables):
            for iter in iterables:
                # each iter is a list of dictionary
                for d in iter:
                    if len(d) == 1:
                    # get the only key,value pair
                        for k,v in d.items():
                            if v == 3:
                                return k
        # values updated in play()
        return helper(self.row, self.col, self.diagonal)

    # used to determine draw, or gameover
    def spots(self):
        return self.empty
    # return bool, valid play
    def play(self, symbol, coordinate):
        if coordinate in self.empty:
            i,j = coordinate[0],coordinate[1]
            self.board[i][j] = symbol
            self.empty.remove(coordinate)
            # update row/col/diagonal
            self.row[i][symbol] = self.row[i].get(symbol,0)+1
            self.col[j][symbol] = self.col[j].get(symbol,0)+1
            # diagonal[0] = i,i; diagonal[1] = i,2-i
            if i == j:
                self.diagonal[0][symbol] = self.diagonal[0].get(symbol,0)+1
            if i == 2-j:
                self.diagonal[1][symbol] = self.diagonal[1].get(symbol,0)+1
            return True
        else:
            return False

# computer players
def driver():
    # create two players
    players = {'X': ComputerPlayer('X'), 'O': ComputerPlayer('O')}
    # players = {'X': ComputerPlayer('X'), 'O': HumanPlayer('O')}
    # alternatively pass the game around players
    # at the end of each term, determine who have won
    game = Game()
    game_round = 0
    while game.spots(): # total of 9, 3*3 matrix
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
