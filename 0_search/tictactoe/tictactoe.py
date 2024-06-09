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
    x = 0
    o = 0
    empty = 0
    for row in board:
        x += row.count("X")
        o += row.count("O")
    
    if x == o:
        return "X"
    else:
        return "O"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = set()
    row_count = 0
    for i, row in enumerate(board):
        for j, element in enumerate(row):
            if element == None:
                action_set.add((i, j))

    return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    new_board = copy.deepcopy(board)
    try:
        if new_board[action[0]][action[1]] == "O" or new_board[action[0]][action[1]] == "X":
            raise ValueError("Invalid move!")
        else:
            new_board[action[0]][action[1]] = player(board)
            return new_board
    except IndexError:
        raise ValueError("Invalid move!")
        


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    columns =[[], [], []]
    diagonals = [[board[0][0], board[1][1], board[2][2]], [board[0][2], board[1][1], board[2][0]]]
    #checking if the same value is present diagonally
    for diagonal in diagonals:
        if len(set(diagonal)) == 1 and None not in set(diagonal):
            return diagonal[0]

    #initialise empty cells, empty = None
    empty_cells = False
    for row in board:
        #creating column list to check result
        columns[0].append(row[0])
        columns[1].append(row[1])
        columns[2].append(row[2])

        if len(set(row)) == 1 and None not in set(row):
            return row[0]
    
    for column in columns:
        if len(set(column)) == 1 and None not in set(column):
            return column[0]
    
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #checking if there are still empty cells
    columns =[[], [], []]
    diagonals = [[board[0][0], board[1][1], board[2][2]], [board[0][2], board[1][1], board[2][0]]]
    #checking if the same value is present diagonally
    for diagonal in diagonals:
        if len(set(diagonal)) == 1 and None not in set(diagonal):
            return True

    #initialise empty cells, empty = None
    empty_cells = False
    for row in board:
        #creating column list to check result
        columns[0].append(row[0])
        columns[1].append(row[1])
        columns[2].append(row[2])

        if None in row:
            empty_cells = True

        if len(set(row)) == 1 and None not in set(row):
            return True
    
    for column in columns:
        if len(set(column)) == 1 and None not in set(column):
            return True
    
    if empty_cells == True:
        return False
    else:
        return True
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
