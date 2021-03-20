def is_valid(board, col, row):
    # check diagonal
    for i in range(col):
        if abs(board[i] - row) == col - i:
            return False
    # TODO constant time check
    return True


def dfs(board, nextQ):
    if nextQ >= len(board):
        return True
    # Everything before nextQ is partial solution
    # Try all possiblility on nextQ
    for i in range(nextQ, len(board)):
        candidate = board[i]
        if is_valid(board, nextQ, candidate):
            board[i], board[nextQ] = board[nextQ], board[i]
            # swap i and nextQ
            if dfs(board, nextQ + 1):
                return True
            else:
                # swap back, the solution did not work
                # TODO justification
                board[i], board[nextQ] = board[nextQ], board[i]
    # Tried all possibilites, the partial solution won't work,
    # abort, this is a deadend
    return False


def solve_n_queens(n):
    assert n >= 1
    # Setup is n*n chessboard
    # Return an array, where each array[i] represents the position of ith queen
    queens = [i for i in range(n)]
    if dfs(queens, 0):
        print(queens)  # inplace
    else:
        # 2*2 is not possible
        print(f"not possible for {n}")


# add or remove constraints
def update_diagonal(row, col, board, integer=1):
    d_row, d_col, n = row, col, len(board)
    while d_row < n and d_col < n:
        board[d_row][d_col] += integer
        d_row += 1
        d_col += 1  # southeast
    d_row, d_col = row, col
    while d_row >= 0 and d_col < n:  # NOTE: col always += 1
        board[d_row][d_col] += integer
        d_row -= 1
        d_col += 1  # northeast
    # FIXME current position +=2 (should be alright)


def dfs_constraint_propagation(solution, col, board):
    n = len(solution)
    if col >= n:  # previous cols queens do not attack each other
        return True
    # place a queen in col
    for i in range(col, n):
        row = solution[i]
        if board[row][col] == 0:  # good to go
            # fill the rest of diagonals
            update_diagonal(row, col, board)
            # swap
            solution[i], solution[col] = solution[col], solution[i]
            if dfs_constraint_propagation(solution, col + 1, board):
                return True
            # failed
            # revert everything
            update_diagonal(row, col, board, -1)
            solution[i], solution[col] = (
                solution[col],
                solution[i],
            )
    return False


def solve_n_queens_constraint_propagation(n):
    # place a queen, then, we know where we can't put the queens
    # use array => row/col is kind of done for us, we just need to propagate diagonals
    # when we try a new queen -> propagate all its diagonals
    # when we backtrack, remove all of its diagonals
    board = [[0] * n for _ in range(n)]  # no queens attack
    solution = [i for i in range(n)]  # => board[solution[i]][i]
    if dfs_constraint_propagation(solution, 0, board):
        print(solution)  # inplace
    else:
        # 2*2 is not possible
        print(f"not possible for {n}")


if __name__ == "__main__":
    for i in range(1, 10):
        solve_n_queens(i)
        solve_n_queens_constraint_propagation(i)
