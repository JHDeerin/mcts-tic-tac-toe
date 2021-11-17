from re import X
from _pytest.mark.structures import Mark
import pytest


from game import Board, Mark, Point


@pytest.fixture
def board() -> Board:
    return Board()

def test_upwards_diagonal_board_counts_as_win(board: Board):
    """
    ======
    X|O|X
    O|X|
    X|O|O
    ======
    """
    board.set_mark(Point(0,0), Mark.X)
    board.set_mark(Point(0,2), Mark.X)
    board.set_mark(Point(1,1), Mark.X)
    board.set_mark(Point(2,0), Mark.X)
    board.set_mark(Point(0,1), Mark.O)
    board.set_mark(Point(1,0), Mark.O)
    board.set_mark(Point(2,1), Mark.O)
    board.set_mark(Point(2,2), Mark.O)

    assert board.check_if_win(last_placement=Point(0,2), team=Mark.X) == True
    assert board.check_if_win_anywhere(team=Mark.X) == True
