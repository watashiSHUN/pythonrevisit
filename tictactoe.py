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


# TODO how to test correctness
# inheritance
# computerplayer __init__(): player.__init__(self,....) => pass it to parent constructor, call it like class function
# or call super().__init__(), no need self
# add __xyz, private member variables
# TODO, then why the inheritance
# since we are calling parent constructor, we get parent member variable self.parent_field...
class ComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def play(self, game):  # override
        # randomly pick a spot to play
        # you can not index into a set, only array
        next_move = random.choice(list(game.spots()))
        # computer always play a valid move
        game.play(self.symbol, next_move)


# TODO, never takes middle?
class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
        self.endstate = 0
        self.map = {}
        # key = state:
        # value =
        # <move, winner at the end if everyone plays optimally, how many empty spots left (fewer step is superior)>
        # TODO(shunxian) override a comparison

    # total steps 0-8
    def play(self, game):
        flat = game.getFlatBoard()
        # move = self.findBestMove(flat, self.symbol)[0]
        # move = self.minimax(flat, self.symbol)[0]
        move = self.minimax_prune(flat, self.symbol, None, None)[0]
        print(f"endstate: {self.endstate}")
        # cast move to i,j
        i = move // 3
        j = move % 3
        game.play(self.symbol, (i, j))

    # return (best move for mover_symbol, game winner if we keep playing, winning with how many empties left)
    # assume the game_state is not over yet
    def findBestMove(self, game_state, mover_symbol):
        # base case, computed before
        if game_state in self.map:
            # print(
            #     "debug visited, after playing one step, we should always hit statement"
            # )
            return self.map[game_state]
        result = None
        # compute possible places to put mover_sybmol (for loop, this is the time we have to use anyway)
        empty_list = [i for i, v in enumerate(game_state) if v == " "]
        empties = len(empty_list)
        next_state = list(game_state[:])
        for e in empty_list:
            # tentatively make a move
            next_state[e] = mover_symbol
            # compute if this is a winning move
            winner = SmartComputerPlayer.computeWinner(next_state, e)
            if winner == mover_symbol or empties == 1:  # NOTE: this is pruning
                self.map[game_state] = (e, winner, empties - 1)
                return self.map[game_state]
            # if we won or draw, the game_state can not progress further
            # the result can be used to return
            # make one move we won => no result will perform better
            # make one move we tie => only one move can be made
            else:
                # I've already played e
                # the game has not finished, let opponent play
                opp_symbol = "X" if mover_symbol == "O" else "O"
                opp_move, opp_winner, opp_empties = self.findBestMove(
                    # game_state needs to be tuple, so we can use it as a key in the dictionary
                    tuple(next_state),
                    opp_symbol,
                )
                if result is None:
                    result = (e, opp_winner, opp_empties)
                # result has value already
                # old result => I lost
                elif result[1] == opp_symbol:
                    # tie/win or I still lost, but lost less
                    if opp_winner != opp_symbol or empties - 1 < result[2]:
                        result = (e, opp_winner, opp_empties)
                # old result => I won
                elif result[1] == mover_symbol:
                    # I won and with more empties
                    if opp_winner == mover_symbol and empties - 1 > result[2]:
                        result = (e, opp_winner, opp_empties)
                else:
                    # old result = draw
                    if opp_winner == mover_symbol:
                        result = (e, opp_winner, opp_empties)
            next_state[e] = " "  # reset for dfs
        self.map[game_state] = result
        # SmartComputerPlayer.printflat(game_state)
        # print("best move:", result, mover_symbol)
        return result

    # return (best move, score) # if I win, its positive score
    # win 100 + empties (the more the better)
    # lost -100 - empties
    # draw 0, no empties
    # if opponent win, its negative score
    # assume game is not over
    def minimax(self, game_state, is_max):
        if game_state in self.map:
            return self.map[game_state]
        # compute possible places to put mover_sybmol (for loop, this is the time we have to use anyway)
        # if we compute "gg" here, then we need to check everything, if we compute "gg" after playing last step
        # we only need to check the last step
        winner = SmartComputerPlayer.computeWinnerWithNoLast(game_state)
        empty_list = [i for i, v in enumerate(game_state) if v == " "]
        empties = len(empty_list)

        # return
        evaluate_result = self.endresult_helper(winner, empties, game_state)
        if evaluate_result is not None:
            return evaluate_result

        next_state = list(game_state[:])
        if is_max:
            # get the best outcome
            result = -200  # any result will be better than this
            move = 0
            for e in empty_list:
                # possible_moves
                next_state[e] = self.symbol
                # if we win, no point of keep playing (trim)
                min_best_move, score = self.minimax(tuple(next_state), False)
                if score > result:
                    move = e
                    result = score
                next_state[e] = " "
            self.map[game_state] = (move, result)
            return (move, result)
        else:
            result = 200  # any result will be less than this
            move = 0
            opp_label = "X" if self.symbol == "O" else "O"
            for e in empty_list:
                next_state[e] = opp_label
                # if opp doesn't take this, we can't trim, we will have to come back to it
                max_best_move, score = self.minimax(tuple(next_state), True)
                if score < result:
                    move = e
                    result = score
                next_state[e] = " "
            self.map[game_state] = (move, result)
            return (move, result)

    def endresult_helper(self, winner, empties, game_state):
        self.endstate += 1
        if winner == self.symbol:
            # print("win")
            # SmartComputerPlayer.printflat(game_state)
            return (None, 100 + empties)
        elif winner is not None:
            # print("lose")
            # SmartComputerPlayer.printflat(game_state)
            return (None, -(100 + empties))
        elif empties == 0:
            # print("draw")
            # SmartComputerPlayer.printflat(game_state)
            return (None, 0)  # draw
        self.endstate -= 1
        return None

    # alpha, maximizer can garantee at current level or above
    # beta, best value minimizer can garantee at current level or above
    # NOTE: this is so that we can trim more, alpha can also be any value that parent level or current is greater, but it will trim less

    # at current level, we can boost alpha, so that any level below will have less nodes
    # current maximizer has not finished evaluating, parent maximizer　>= X is irrelevant
    # somewhere down the path, maximizer can play a move that gets better than minimizer
    # if current maximizer has value < alpha...we need to keep evaluating, next one might be higher
    def minimax_prune(self, game_state, is_max, alpha, beta):
        if game_state in self.map:
            return self.map[game_state]
        winner = SmartComputerPlayer.computeWinnerWithNoLast(game_state)
        empty_list = [i for i, v in enumerate(game_state) if v == " "]
        empties = len(empty_list)

        evaluate_result = self.endresult_helper(winner, empties, game_state)
        if evaluate_result is not None:
            return evaluate_result

        next_state = list(game_state[:])

        move = 0
        result = None
        # read beta (parent is minimizer)
        if is_max:
            for e in empty_list:
                # possible_moves
                next_state[e] = self.symbol
                min_best_move, score = self.minimax_prune(
                    tuple(next_state), False, alpha, beta
                )
                if result is None or score > result:
                    move, result = e, score
                next_state[e] = " "

                # update alpha (reduce range, only update when greater)
                # at least one result is retrieved from children (after minimax_prune)
                # current state will not update beta
                if alpha is None or result > alpha:
                    alpha = result

                # beta == None means I am the first child to be evaluated
                # if equals, then parent minimizer will just pick existing beta
                # any furhter evaluation will get no better result
                if beta is not None and result >= beta:
                    # Do not update the map, since solution from current state is incomplete
                    return (move, result)  # NOTE: this result will not be used

            self.map[game_state] = (move, result)
            return (move, result)
        # read alpha (parent is maximizer)
        else:
            opp_label = "X" if self.symbol == "O" else "O"
            for e in empty_list:
                next_state[e] = opp_label
                max_best_move, score = self.minimax_prune(
                    tuple(next_state), True, alpha, beta
                )
                if result is None or score < result:
                    move, result = e, score
                next_state[e] = " "

                if beta is None or result < beta:
                    beta = result

                if alpha is not None and result <= alpha:
                    return (move, result)

            self.map[game_state] = (move, result)
            return (move, result)

    @staticmethod
    def printflat(game):
        for i in range(3):
            print(",".join(game[i * 3 : (i + 1) * 3]))

    # only the last step can produce a winner
    # otherwise the game has already finished => compute winner after each play
    # test only the last step (index)
    # which is why we compute winner after each play
    # TODO winner(move, letter) -> evaluate if this move makes letter a winner
    @staticmethod
    def computeWinner(game_state, last_move):
        mover_symbol = game_state[last_move]
        row = last_move // 3
        if (game_state[row * 3 : (row + 1) * 3]).count(mover_symbol) == 3:
            return mover_symbol
        col = last_move % 3
        if [game_state[i * 3 + col] for i in range(3)].count(mover_symbol) == 3:
            return mover_symbol
        # diagonal
        diagonal = [0, 4, 8]
        inverse_diagonal = [2, 4, 6]
        if last_move in diagonal:
            if [game_state[i] for i in diagonal].count(mover_symbol) == 3:
                return mover_symbol
        if last_move in inverse_diagonal:
            if [game_state[i] for i in inverse_diagonal].count(mover_symbol) == 3:
                return mover_symbol

    def computeWinnerWithNoLast(game_state):
        for var in range(3):
            if all(
                [i == game_state[var * 3] for i in game_state[var * 3 : (var + 1) * 3]]
            ):
                if game_state[var * 3] != " ":
                    return game_state[var * 3]
            if all([game_state[var] == game_state[i * 3 + var] for i in range(3)]):
                if game_state[var] != " ":
                    return game_state[var]
        # diagonal
        diagonal = [0, 4, 8]
        inverse_diagonal = [2, 4, 6]
        if all([game_state[0] == game_state[i] for i in diagonal]):
            if game_state[0] != " ":
                return game_state[0]
        if all([game_state[2] == game_state[i] for i in inverse_diagonal]):
            if game_state[2] != " ":
                return game_state[2]


class HumanPlayer(Player):
    def play(self, game):
        # expect i,j
        while True:
            user_input = input("coordinate(expected: i,j): ")
            # surround user input in try_catch
            try:
                i, j = user_input.split(",")
                coord = (int(i), int(j))
                # could raise invalid error in the gameplay function
                if game.play(self.symbol, coord):
                    return
                else:
                    raise ValueError
            except ValueError:
                print("invalid input, Try again")


# player be aware of the game, but the game doesn't need to know about players(passive)
# store the games
# easier to play, easier to tally
# store in matrix => easier to print (currently use this, check all lines, if one symbol ==> winner)
# empty set => easier for random computer to play
class Game:
    def __init__(self):
        self.board = [[" "] * 3 for i in range(3)]
        # used to play (pick a random point)
        # also used to calculate lines (set or list?)
        self.empty = set([(i, j) for i in range(3) for j in range(3)])
        self.row = [{}, {}, {}]  # maps => {'x': how many}
        self.col = [{}, {}, {}]
        self.diagonal = [{}, {}]

    # TODO construct a game from a flat
    def getFlatBoard(self):
        return tuple(self.board[i][j] for i in range(3) for j in range(3))

    # first function to define
    def printBoard(self):
        for i in self.board:
            print("|", " | ".join(i), "|")

    # return winner char
    # inconclusive return None
    def determineWinner(self):
        def helper(*iterables):
            for iter in iterables:
                # each iter is a list of dictionary
                for d in iter:
                    if len(d) == 1:
                        # get the only key,value pair
                        for k, v in d.items():
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
            i, j = coordinate[0], coordinate[1]
            self.board[i][j] = symbol
            self.empty.remove(coordinate)
            # update row/col/diagonal
            self.row[i][symbol] = self.row[i].get(symbol, 0) + 1
            self.col[j][symbol] = self.col[j].get(symbol, 0) + 1
            # diagonal[0] = i,i; diagonal[1] = i,2-i
            if i == j:
                self.diagonal[0][symbol] = self.diagonal[0].get(symbol, 0) + 1
            if i == 2 - j:
                self.diagonal[1][symbol] = self.diagonal[1].get(symbol, 0) + 1
            return True
        else:
            return False


def driver():
    # create two players
    # players = {'X': SmartComputerPlayer('X'), 'O': SmartComputerPlayer('O')}
    players = {"X": SmartComputerPlayer("X"), "O": HumanPlayer("O")}
    # players = {"X": SmartComputerPlayer("X"), "O": ComputerPlayer("O")}
    # alternatively pass the game around players
    # at the end of each term, determine who have won
    game = Game()
    current_player = players["X"]
    while game.spots():  # total of 9, 3*3 matrix
        current_player.play(game)
        game.printBoard()
        # TODO check winner after each move
        winner = game.determineWinner()
        if winner is not None:
            print("winner is ", winner)
            return
        # switch players
        current_player = (
            players["X"] if current_player == players["O"] else players["O"]
        )
        print()  # newline
    print("game is a draw")


driver()
