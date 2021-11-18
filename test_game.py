import pytest

from game import Board, Mark, Point
from agents import Action, GameState, MCTSAgent


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


def test_simple_horizontal_win(board: Board):
    """
    ======
     |O|
     |O|
    X|X|X
    ======
    """
    board.set_mark(Point(0,1), Mark.O)
    board.set_mark(Point(1,1), Mark.O)
    board.set_mark(Point(2,0), Mark.X)
    board.set_mark(Point(2,1), Mark.X)
    board.set_mark(Point(2,2), Mark.X)
    assert board.check_if_win(last_placement=Point(2,2), team=Mark.X) == True
    assert board.check_if_win_anywhere(team=Mark.X) == True


def test_simple_horizontal_upper_win(board: Board):
    """
    ======
    O|O|O
     |X|
    X|X|
    ======
    """
    board.set_mark(Point(0,0), Mark.O)
    board.set_mark(Point(0,1), Mark.O)
    board.set_mark(Point(0,2), Mark.O)
    board.set_mark(Point(1,1), Mark.X)
    board.set_mark(Point(2,0), Mark.X)
    board.set_mark(Point(2,1), Mark.X)
    assert board.check_if_win(last_placement=Point(0,1), team=Mark.O) == True
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


def test_mcts_ai_miss_win_error_pos(board: Board):
    """
    ======
    X|O|
    O|O|X
    X|X|
    ======

    In a test game w/ O to move, the AI played 0,2 instead of 2,2, letting me
    win; need to confirm this happens and fix it if so

    FIXED: Turned out to be a bug w/ how GameState was checking draws (forgot
    to check that the other player wasn't winning either)
    """
    # TODO: Implement this
    board.set_mark(Point(0,0), Mark.X)
    board.set_mark(Point(1,2), Mark.X)
    board.set_mark(Point(2,0), Mark.X)
    board.set_mark(Point(2,1), Mark.X)
    board.set_mark(Point(0,1), Mark.O)
    board.set_mark(Point(1,0), Mark.O)
    board.set_mark(Point(1,1), Mark.O)
    state = GameState(board, player=Mark.O)

    ai = MCTSAgent()
    ai_action = ai.get_move(state, iterations=2, verbose=True)
    expected = Action(Point(2,2), player=Mark.O)
    assert ai_action == expected


def test_mcts_ai_miss_win_error_pos_2(board: Board):
    """
    ======
    O| |O
     |X|
    X| |
    ======
    Ditto case; AI to move as X, AI played 2,1 instead of 0,1, letting me win from behind

    ...this could just be a sampling issue (apparently 9! ~= 300,000, which is
    higher than I thought, so it might simply not be covering every case...but
    then why did it fail for the top case?)
    """
    board.set_mark(Point(1,1), Mark.X)
    board.set_mark(Point(2,0), Mark.X)
    board.set_mark(Point(0,0), Mark.O)
    board.set_mark(Point(0,2), Mark.O)
    state = GameState(board, player=Mark.X)

    ai = MCTSAgent()
    ai_action = ai.get_move(state, verbose=True)
    expected = Action(Point(0,1), player=Mark.X)
    assert ai_action == expected


def test_mcts_ai_miss_win_error_pos_2_miss_winning_move(board: Board):
    """
    ======
    O| |O
     |X|X
    X| |
    ======
    """
    board.set_mark(Point(1,1), Mark.X)
    board.set_mark(Point(1,2), Mark.X)
    board.set_mark(Point(2,0), Mark.X)
    board.set_mark(Point(0,0), Mark.O)
    board.set_mark(Point(0,2), Mark.O)
    state = GameState(board, player=Mark.O)

    ai = MCTSAgent()
    ai_action = ai.get_move(state, verbose=True)
    expected = Action(Point(0,1), player=Mark.O)
    assert ai_action == expected


def test_mcts_ai_error_pos_2_miss_state_score(board: Board):
    """
    ======
    O| |O
     |X|
    X|X|
    ======
    """
    board.set_mark(Point(1,1), Mark.X)
    board.set_mark(Point(2,0), Mark.X)
    board.set_mark(Point(2,1), Mark.X)
    board.set_mark(Point(0,0), Mark.O)
    board.set_mark(Point(0,1), Mark.O)
    board.set_mark(Point(0,2), Mark.O)
    state = GameState(board, player=Mark.O)

    assert state.get_score(player=Mark.O) == 1.0


def test_mcts_ai_miss_win_error_pos_3(board: Board):
    """
    ======
     | |X
     |X|
     | |O
    ======
    """
    board.set_mark(Point(1,1), Mark.X)
    board.set_mark(Point(0,2), Mark.X)
    board.set_mark(Point(2,2), Mark.O)
    state = GameState(board, player=Mark.O)

    ai = MCTSAgent()
    ai_action = ai.get_move(state, verbose=True)
    expected = Action(Point(2,0), player=Mark.O)
    assert ai_action == expected


def test_mcts_ai_miss_win_error_pos_4(board: Board):
    """
    ======
     | |O
     |X|X
    X| |O
    ======
    """
    board.set_mark(Point(1,1), Mark.X)
    board.set_mark(Point(1,2), Mark.X)
    board.set_mark(Point(2,0), Mark.X)
    board.set_mark(Point(0,2), Mark.O)
    board.set_mark(Point(2,2), Mark.O)
    state = GameState(board, player=Mark.O)

    ai = MCTSAgent()
    ai_action = ai.get_move(state, verbose=True)
    expected = Action(Point(1,0), player=Mark.O)
    assert ai_action == expected
