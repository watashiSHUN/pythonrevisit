import random
from functools import reduce

class Player:
    # assumed to be O/X, the game is played between 2
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
    def __init__(self,letter):
        super().__init__(letter)

    def play(self, game): # override
        # randomly pick a spot to play
        # you can not index into a set, only array
        next_move = random.choice(list(game.spots()))
        # computer always play a valid move
        game.play(self.symbol, next_move)

# TODO, never takes middle?
class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
        self.map = {} # state: move, winner at the end if everyone plays optimally

    # total steps 0-8
    def play(self, game):
        flat = game.getFlatBoard()
        move, score = self.findBestMove(flat, self.symbol)
        # cast move to i,j
        i = move // 3
        j = move % 3
        game.play(self.symbol, (i,j))

    # assume mover will try its best
    # mover is the next to move
    def findBestMove(self, game_state, mover_symbol):
        # base case
        if game_state in self.map:
            return self.map[game_state]
        # compute winner (game ends at this stage)
        winner = SmartComputerPlayer.computeWinner(game_state)
        result = None
        if winner is not None:
            result = (None, winner)
        else: # winner == None
            empty_spots = [i for i,v in enumerate(game_state) if v == ' ']
            if not empty_spots: # draw
                result = (None, None)
            # TODO use game object
            # try all the moves
            else:
                next_symbol = 'X' if mover_symbol=='O' else 'O'
                base = list(game_state[:])
                for move in empty_spots:
                    base[move] = mover_symbol
                    next_move, winner = self.findBestMove(tuple(base),next_symbol)
                    base[move] = ' ' # reset for dfs
                    # cases where we need to update the optimal
                    if result is None:
                        result = (move, winner)
                    # win >= draw >= lose
                    elif winner == mover_symbol:
                        result = (move, winner)
                    elif winner is None and result[1] == next_symbol:
                        # update
                        result = (move, winner)
                    
        self.map[game_state] = result

        # print('best move:', result, mover_symbol)
        return result
                

    # TODO, I don't want to call self
    # do I need @staticmethod
    @staticmethod
    def helper(a,b):
        return a if a == b and a != ' ' else None

    @staticmethod
    def printflat(game):
        for i in range(3):
            print(",".join(game[i*3:(i+1)*3]))

    @staticmethod
    def computeWinner(game_state):
        # row
        # [[0,1,2].[3,4,5],[6,7,8]]
        for row in [game_state[i*3:(i+1)*3] for i in range(3)]:
            result = reduce(SmartComputerPlayer.helper, row)
            if result:
                return result
        # col
        for col in [[game_state[i*3+j] for i in range(3)] for j in range(3)]:
            result = reduce(SmartComputerPlayer.helper, col)
            if result:
                return result
        # diagonal
        diagonal = [0,4,8]
        inverse_diagona = [2,4,6]
        result = reduce(SmartComputerPlayer.helper, [game_state[i] for i in diagonal])
        if result:
            return result
        result = reduce(SmartComputerPlayer.helper, [game_state[i] for i in inverse_diagona])
        if result:
            return result
        

class HumanPlayer(Player):
    def play(self, game):
        # expect i,j
        while True:
            user_input = input("coordinate(expected: i,j): ")
            # surround user input in try_catch
            try:
                i,j = user_input.split(',')
                coord = (int(i),int(j))
                # could raise invalid error in the gameplay function
                if game.play(self.symbol, coord):
                    return
            except:
                print("invalid input")

# store the games
# easier to play, easier to tally
# store in matrix => easier to print (currently use this, check all lines, if one symbol ==> winner)
# empty set => easier for random computer to play
class Game:
    def __init__(self):
        self.board = [ [' ']*3 for i in range(3)]
        # used to play (pick a random point)
        # also used to calculate lines (set or list?)
        self.empty = set([(i,j) for i in range(3) for j in range(3)])
        self.row =[{},{},{}] # maps => {'x': how many}
        self.col =[{},{},{}]
        self.diagonal = [{},{}]

    def getFlatBoard(self):
        return tuple(self.board[i][j] for i in range(3) for j in range(3))
    # first function to define
    def printBoard(self):
        for i in self.board:
            print('|', " | ".join(i), '|')
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

def driver():
    # create two players
    # players = {'X': ComputerPlayer('X'), 'O': ComputerPlayer('O')}
    players = {'X': SmartComputerPlayer('X'), 'O': HumanPlayer('O')}
    # alternatively pass the game around players
    # at the end of each term, determine who have won
    game = Game()
    current_player = players['O']
    while game.spots(): # total of 9, 3*3 matrix
        current_player.play(game)
        game.printBoard()
        # TODO check winner after each move
        winner = game.determineWinner()
        if winner is not None:
            print("winner is ", winner)
            return
        # switch players
        current_player = players['X'] if current_player == players['O'] else players['O']
        print() #newline
    print("game is a draw")

driver()
