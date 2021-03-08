# puzzle is list of list
# [[3,9,-1, -1,5,-1,-1,-1],
#  [.....................]
#  ...
# ]

# cubes 0-2, 3-5, 6-8
def findCube(index):
    # return a list of size 3*3, convert to matrix index puzzle[row][col]
    single = index % 9
    double = index // 9
    if 0 <= single <= 2:
        s = [0, 1, 2]
    elif 3 <= single <= 5:
        s = [3, 4, 5]
    else:
        s = [6, 7, 8]

    if 0 <= double <= 2:
        d = [0, 1, 2]
    elif 3 <= double <= 5:
        d = [3, 4, 5]
    else:
        d = [6, 7, 8]
    returnV = []
    for i in d:
        for j in s:
            returnV.append(i * 9 + j)
    return returnV


# index is the index in puzzle
def dfs(missing, index, puzzle):
    if index >= len(missing):
        # the end, we found a solution
        return True
    row = missing[index] // 9
    col = missing[index] % 9
    # in current_position, try 1->9
    for i in range(1, 10):
        # make sure current number works
        # 3 things to check
        # row
        # x is the element
        if sum([1 for x in puzzle[row] if x == i]) > 0:
            continue  # skip
        # col
        # x is the row index
        if sum([1 for x in range(9) if puzzle[x][col] == i]) > 0:
            continue  # skip
        # cube
        flag = False
        for cube in findCube(index):
            cube_row = cube // 9
            cube_col = cube % 9
            if puzzle[cube_row][cube_col] == i:
                flag = True
                break
        if flag:
            continue  # skip
        # set index to i
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
