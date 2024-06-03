from tictactoe import player, terminal

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
          [O, X, O]]          
          


def test_player():
    assert player(board1) == "X"
    assert player(board2) == "O"
    assert player(board3) == "X"

def test_terminal():
    assert terminal(board4) == True
    assert terminal(board5) == True
    assert terminal(board6) == True
    assert terminal(board2) == False