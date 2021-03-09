# puzzle is list of list
# [[3,9,-1, -1,5,-1,-1,-1],
#  [.....................]
#  ...
# ]

# cubes 0-2, 3-5, 6-8
def findCube(row, col):
    # // 3 => 0,1,2=0; 3,4,5=1; 6,7,8=2;
    returnV = []
    for i in range((row // 3) * 3, (row // 3) * 3 + 3):
        for j in range((col // 3) * 3, (col // 3) * 3 + 3):
            returnV.append((i, j))
    return returnV


def is_valid(puzzle, guess, row, col):
    # DOWNSIDE, this doesn't break early
    # 3 things to check
    # row
    # x is the element
    if guess in puzzle[row]:
        return False
    # col
    # x is the row index
    if guess in [puzzle[x][col] for x in range(9)]:
        return False
    # cube
    if guess in [
        puzzle[cube_row][cube_col] for cube_row, cube_col in findCube(row, col)
    ]:
        return False

    return True


# index to the missing[]
def dfs(missing, index, puzzle):
    if index >= len(missing):
        # the end, we found a solution
        return True
    # CAREFUL, index and missing[index] are pretty confusing
    row = missing[index] // 9
    col = missing[index] % 9
    # in current_position, try 1->9
    for i in range(1, 10):
        if is_valid(puzzle, i, row, col):
            puzzle[row][col] = i
            if dfs(missing, index + 1, puzzle):
                return True
    # if not find, need to set it to -1, otherwise the row/col/cube comparison will fail
    puzzle[row][col] = -1
    # don't need to set it back to -1 since we have missings (all necessary)
    return False


# returing whether a solution exists
def solve_sudoku(puzzle):
    missing = []
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == -1:
                missing.append(i * 9 + j)
    return dfs(missing, 0, puzzle)


if __name__ == "__main__":
    puzzle = [
        [3, 9, -1, -1, 5, -1, -1, -1, -1],
        [-1, -1, -1, 2, -1, -1, -1, -1, 5],
        [-1, -1, -1, 7, 1, 9, -1, 8, -1],
        [-1, 5, -1, -1, 6, 8, -1, -1, -1],
        [2, -1, 6, -1, -1, 3, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, 4],
        [5, -1, -1, -1, -1, -1, -1, -1, -1],
        [6, 7, -1, 1, -1, 5, -1, 4, -1],
        [1, -1, 9, -1, -1, -1, 2, -1, -1],
    ]
    print(solve_sudoku(puzzle))
    print(puzzle)
