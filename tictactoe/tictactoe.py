"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


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
    x_moves = 0
    o_moves = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == X:
                x_moves += 1
            elif board[i][j] == O:
                o_moves += 1
    if x_moves <= o_moves:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = []

    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                result.append((i, j))

    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if isinstance(action, list):
        raise Exception("Invalid type")
    if len(action) != 2:
        raise Exception("Action should be a coordinate")
    i = action[0]
    j = action[1]
    if i < 0 or i > 2:
        raise Exception("Row value out of bounds")
    if j < 0 or j > 2:
        raise Exception("Column value out of bounds")

    if board[i][j] != EMPTY:
        raise Exception("Invalid action, postion already taken")

    local_board = copy.deepcopy(board)

    current_player = player(board)

    local_board[i][j] = current_player

    return local_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for p in [X, O]:
        # row winner
        for i in range(0, 3):
            if board[i][0] == p and board[i][1] == p and board[i][2] == p:
                return p
        # column winner
        for j in range(0, 3):
            if board[0][j] == p and board[1][j] == p and board[2][j] == p:
                return p
        # orthogonal
        if board[0][0] == p and board[1][1] == p and board[2][2] == p:
            return p
        if board[0][2] == p and board[1][1] == p and board[2][0] == p:
            return p
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in range(0, 3):
        for col in range(0, 3):
            if board[row][col] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    if w == O:
        return -1
    return 0


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max([v, min_value(result(board, action))])
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min([v, max_value(result(board, action))])
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    optimal = None
    if player(board) == X:
        v = -math.inf
        
        for action in actions(board):
            result_board = result(board, action)
            value = min_value(result_board)
            if value > v:
                v = value
                optimal = action
    else:
        v = math.inf
        
        for action in actions(board):
            result_board = result(board, action)
            value = max_value(result_board)
            if value < v:
                v = value
                optimal = action

    return optimal