def findNextCell(board):
     for i in range (0, 9):
        for j in range (0, 9):
            if(board[i][j] == 0):
                return [i, j]

def isFull(board):
    for i in range(0,9):
        for j in range(0,9):
            if(board[i][j] == 0): return False
    return True

def isValid(board, row, col, v): 
    for c in range(0, 9):
        if(board[row][c] == v): return False
    for r in range(0, 9): 
        if(board[r][col] == v): return False

    for r in range (0, 3):
        for c in range (0, 3):
            if(board[r + (row-row%3)][c + (col-col%3)] == v): return False
    return True

def verifyBoard(board):
    boardRow = len(board)
    if(boardRow != 9): return False
    boardCol = len(board[0])
    if(boardCol != 9): return False

    for r in range(0, 9):
        for c in range(0, 9):
            v = board[r][c]
            if(v>0):
                board[r][c] = 0
                if(isValid(board, r, c, v) == False):
                    board[r][c] = v
                    return False
                board[r][c] = v
    return True

def sudokuSol(board):
    if(isFull(board)):
        return True

    [i, j] = findNextCell(board)
    for v in range(1, 10):
        if(isValid(board, i, j, v)):
            board[i][j] = v
            if(sudokuSol(board) == True): 
                return True
            board[i][j] = 0
    
    return False

def solveSDKBoard(board):
    if(verifyBoard(board)):
        return sudokuSol(board)
    return False