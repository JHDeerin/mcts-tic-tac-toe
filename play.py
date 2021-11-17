"""
Play a game of tic-tac-toe against an opponent
"""
from agents import GameState, MCTSAgent, RandomAIAgent
from game import Board, Mark, Point

def str_to_point(string: str) -> Point:
    row, col = string.split(",")
    return Point(int(row[0]), int(col[0]))


if __name__ == "__main__":
    board = Board()
    ai = MCTSAgent()
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
            move_point = ai.get_move(GameState(board, current_team)).pos
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
