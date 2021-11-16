"""
The logic for playing a game of Tic-Tac-Toe (or "Naughts and Crosses" in the UK).

This handles
"""
import dataclasses
import enum
import random
from typing import List

class Mark(enum.Enum):
    BLANK=0
    X=1
    O=2


@dataclasses.dataclass
class Point:
    row: int=0
    col: int=0


class Board:
    """
    The current state of the tic-tac-toe board
    """
    def __init__(self, board_size: int=3, num_dimensions: int=2):
        # TODO: Implement boards of different dimension than 2
        self._board = self._create_new_board(board_size, num_dimensions)
        self.board_size = board_size

    def _create_new_board(self, board_size: int=3, num_dimensions_remaining: int=2) -> list:
        """
        Get a new blank tic-tac-toe board composed of nested lists.
        """
        return [
            [Mark.BLANK, Mark.BLANK, Mark.BLANK],
            [Mark.BLANK, Mark.BLANK, Mark.BLANK],
            [Mark.BLANK, Mark.BLANK, Mark.BLANK],
        ]

    def __str__(self) -> str:
        display_chars = {
            Mark.BLANK: " ",
            Mark.X: "X",
            Mark.O: "O"
        }
        display_string = "==" * self.board_size + "\n"
        for row in self._board:
            row_display_chars = [display_chars[mark] for mark in row]
            display_string += '|'.join(row_display_chars)
            display_string += "\n"
        display_string += "==" * self.board_size + "\n"
        return display_string

    def set_mark(self, position: Point, mark: Mark) -> bool:
        try:
            self._board[position.row][position.col] = mark
        except IndexError:
            return None
        return self.check_if_win(position, mark)

    def get_mark(self, position: Point) -> Mark:
        try:
            return self._board[position.row][position.col]
        except IndexError:
            return None

    def get_available_spaces(self) -> List[Point]:
        available = []
        for row_index, row in enumerate(self._board):
            for col_index, mark in enumerate(row):
                if mark == Mark.BLANK:
                    available.append(Point(row_index, col_index))
        return available

    def check_if_win(self, last_placement: Point, team: Mark) -> bool:
        last_placed_mark = self.get_mark(last_placement)
        if last_placed_mark != team:
            # The place we're checking for a win doesn't belong to this team, so
            # they can't have a winning position here
            return False
        won_vertically = self._check_win_pos(last_placement, team, Point(1,0))
        won_horizontally = self._check_win_pos(last_placement, team, Point(0,1))
        won_diagonally_down = self._check_win_pos(last_placement, team, Point(1,1))
        won_diagonally_up = self._check_win_pos(last_placement, team, Point(-1,1))
        return won_vertically or won_horizontally or won_diagonally_down or won_diagonally_up

    def _check_win_pos(self, last_placement: Point, team: Mark, offset_dir: Point) -> bool:
        current_pos = last_placement
        # Move to the edge of the board
        while current_pos.row > 0 and current_pos.col > 0:
            current_pos = Point(current_pos.row - offset_dir.row, current_pos.col - offset_dir.col)
        # check we have at least N marks in a straight line
        for i in range(self.board_size):
            if self.get_mark(current_pos) != team:
                return False
            current_pos = Point(current_pos.row + offset_dir.row, current_pos.col + offset_dir.col)
        return True


def str_to_point(string: str) -> Point:
    row, col = string.split(",")
    return Point(int(row[0]), int(col[0]))


class RandomAIAgent:
    def get_move(self, board: Board) -> Point:
        return random.choice(board.get_available_spaces())


if __name__ == "__main__":
    board = Board()
    ai = RandomAIAgent()
    current_team = Mark.X
    ai_team = Mark.O
    is_game_running = True

    while is_game_running:
        print(board)
        available_moves = board.get_available_spaces()
        print(available_moves)
        if not available_moves:
            print("No more possible moves")
            exit(0)

        if current_team == ai_team:
            move_point = ai.get_move(board)
        else:
            move_str = input("Move (in format '1,2'): ")
            move_point = str_to_point(move_str)
        if board.set_mark(move_point, current_team):
            is_game_running = False
            print("WINNER!")
        if current_team == Mark.X:
            current_team = Mark.O
        else:
            current_team = Mark.X
