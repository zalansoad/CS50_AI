from tictactoe import player, terminal, actions

X = "X"
O = "O"
EMPTY = None

board1 = [[EMPTY, EMPTY, EMPTY],
          [EMPTY, EMPTY, EMPTY],
          [EMPTY, EMPTY, EMPTY]]
board2 = [[EMPTY, X, EMPTY],
          [EMPTY, EMPTY, EMPTY],
          [EMPTY, EMPTY, EMPTY]]
board3 = [[EMPTY, X, EMPTY],
          [EMPTY, O, O],
          [EMPTY, X, EMPTY]]
board4 = [[X, X, X],
          [EMPTY, O, O],
          [EMPTY, X, EMPTY]]
board5 = [[O, X, EMPTY],
          [O, EMPTY, O],
          [O, X, EMPTY]]

board6 = [[O, X, EMPTY],
          [O, O, X],
          [EMPTY, X, O]]
board7 = [[EMPTY, EMPTY, X],
          [EMPTY, X, EMPTY],
          [X, EMPTY, EMPTY]]         
          
def test_actions():
    assert actions(board3) =={(0, 0), (0, 2), (1, 0), (2, 0), (2, 2)}
    assert actions(board4) =={(1, 0), (2, 0), (2, 2)}
    assert actions(board5) =={(0, 2), (1, 1), (2, 2)}
    assert actions(board6) =={(0, 2), (2, 0)}
    

def test_player():
    assert player(board1) == "X"
    assert player(board2) == "O"
    assert player(board3) == "X"

def test_terminal():
    assert terminal(board1) == False
    assert terminal(board2) == False
    assert terminal(board3) == False
    assert terminal(board4) == True
    assert terminal(board5) == True
    assert terminal(board6) == True
    assert terminal(board7) == True
    