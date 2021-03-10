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


if __name__ == "__main__":
    for i in range(1, 10):
        solve_n_queens(i)
