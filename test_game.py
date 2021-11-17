from re import X
from _pytest.mark.structures import Mark
import pytest


from game import Board, Mark, Point


@pytest.fixture
def board() -> Board:
    return Board()


def test_empty_board_is_not_a_win(board: Board):
    """
    ======
     | |
     | |
     | |
    ======
    """
    assert board.check_if_win(last_placement=Point(0,2), team=Mark.X) == False
    assert board.check_if_win_anywhere(team=Mark.O) == False
    assert board.check_if_win_anywhere(team=Mark.X) == False


def test_full_draw_board_is_not_a_win(board: Board):
    """
    ======
    X|O|X
    O|X|X
    O|X|O
    ======
    """
    board.set_mark(Point(0,0), Mark.X)
    board.set_mark(Point(0,2), Mark.X)
    board.set_mark(Point(1,1), Mark.X)
    board.set_mark(Point(1,2), Mark.X)
    board.set_mark(Point(2,1), Mark.X)
    board.set_mark(Point(0,1), Mark.O)
    board.set_mark(Point(1,0), Mark.O)
    board.set_mark(Point(2,0), Mark.O)
    board.set_mark(Point(2,2), Mark.O)
    assert board.check_if_win(last_placement=Point(0,2), team=Mark.X) == False
    assert board.check_if_win_anywhere(team=Mark.X) == False
    assert board.check_if_win(last_placement=Point(1,0), team=Mark.O) == False
    assert board.check_if_win_anywhere(team=Mark.O) == False


def test_simple_vertical_win(board: Board):
    """
    ======
     |O|
     |O|
     |O|
    ======
    """
    board.set_mark(Point(0,1), Mark.O)
    board.set_mark(Point(1,1), Mark.O)
    board.set_mark(Point(2,1), Mark.O)
    assert board.check_if_win(last_placement=Point(2,1), team=Mark.O) == True
    assert board.check_if_win_anywhere(team=Mark.O) == True


def test_simple_upwards_diagonal_board_counts_as_win(board: Board):
    """
    ======
     | |X
     |X|
    X| |
    ======
    """
    board.set_mark(Point(0,2), Mark.X)
    board.set_mark(Point(1,1), Mark.X)
    board.set_mark(Point(2,0), Mark.X)

    assert board.check_if_win(last_placement=Point(0,2), team=Mark.X) == True
    assert board.check_if_win_anywhere(team=Mark.X) == True


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


def test_mcts_ai_error_pos():
    """
    ======
    X|O|
    O|O|X
    X|X|
    ======

    In a test game w/ O to move, the AI played 0,2 instead of 2,2, letting me
    win; need to confirm this happens and fix it if so
    """
    # TODO: Implement this
    pass
