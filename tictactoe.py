"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

# misc functions
def getXBoard(board):
    i = 0
    tempBoard = []
    tempSet = []
    while i < 3:
        tempSet.append(board[i][i])
        i += 1
    tempBoard.append(tempSet)
    tempSet2 = []
    i = 0
    while i < 3:
        tempSet2.append(board[2-i][i])
        i += 1
    tempBoard.append(tempSet2)
    return tempBoard

def invertBoard(board):
    tempBoard = []
    i = 0
    while i < 3:
        j = 0
        tempSet = []
        while j < 3:
            tempSet.append(board[j][i])
            j += 1
        tempBoard.append(copy.deepcopy(tempSet))
        tempSet.clear()
        i += 1
    return tempBoard

def initial_state():
    """
    Returns starting state of the board.
    """

    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_num = 0
    o_num = 0
    for i in board:
        for j in i:
            if j == "X":
                x_num += 1
            elif j == "O":
                o_num += 1
    if x_num > o_num:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = set()
    y = 0
    x = 0
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == EMPTY:
                possible.add((i,j))
         
    return possible

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    tempBoard = copy.deepcopy(board)
    possible = actions(board)

    if len(possible) == 0:
        raise Exception
    
    if action not in possible:
        print("Action:")
        print(action)
        raise Exception

    x = action[0]
    y = action[1]
    playerMove = player(tempBoard)
    tempBoard[x][y] = playerMove
    return tempBoard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #straight accross
    for i in board:
        accrossX = [X,X,X]
        accrossO = [O,O,O]
        if i == accrossX:
            return X
        elif i == accrossO:
            return O
    #straight down
    tempBoard = invertBoard(board)
    for i in tempBoard:
        downX = [X,X,X]
        downO = [O,O,O]
        if i == downX:
            return X
        elif i == downO:
            return O
    #sideways
    xBoard = getXBoard(board)
    for i in xBoard:
        stepX = [X,X,X]
        stepO = [O,O,O]
        if i == stepX:
            return X
        elif i == stepO:
            return O
    #no one won
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    emptySpace = False
    for i in board:
        for j in i:
            if j == EMPTY:
                emptySpace = True
                break

    #check if there is a winner
    if winner(board) != None:
        return True
    #check if there is an empty space
    elif emptySpace == True:
        return False
    #if there is no empty space and no one won, then there must be a tie
    elif winner(board) == None and emptySpace == False:
        return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #assuming that the terminal is true
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #returning an optimal action of (i,j)
    if terminal(board):
        return None
    move = ()
    aiSymbol = player(board)
    if aiSymbol is X:
        best = float('-inf')
    elif aiSymbol is O:
        best = float('inf')
    else:
        raise Exception
    
    moveValue = 0
    alpha = float('-inf')
    beta = float('inf')
    for action in actions(board):
        if aiSymbol is X:
            # minimize the value
            moveValue = minValue(result(board,action), alpha, beta)
        elif aiSymbol is O:
            # maximize the value
            moveValue = maxValue(result(board,action),alpha, beta)
        if aiSymbol is X and moveValue > best or aiSymbol is O and moveValue < best:
            del move
            move = action
            best = moveValue
    return move

def maxValue(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        v = max(v, minValue(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v

def minValue(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, maxValue(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v