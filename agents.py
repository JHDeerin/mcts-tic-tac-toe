"""
A set of AI agents that can play tic-tac-toe.
"""
import copy
import dataclasses
import math
import random
from typing import Dict

from game import Board, Mark, Point


@dataclasses.dataclass(frozen=True)
class Action:
    pos: Point
    player: Mark


class GameState:
    """
    An interface to let MCTS evaluate the current tic-tac-toe game state.
    """
    def __init__(self, board: Board, player: Mark):
        self.board = copy.deepcopy(board)
        self.player = copy.deepcopy(player)

    def get_next_state(self, action: Action) -> "GameState":
        if not action:
            return GameState(self.board, self.player)
        new_state = GameState(self.board, self.get_next_player(action.player))
        new_state.board.set_mark(action.pos, action.player)
        return new_state

    def get_next_player(self, current_player: Mark) -> Mark:
        if current_player == Mark.X:
            return Mark.O
        else:
            return Mark.X

    def get_actions(self) -> list:
        return [
            Action(pos, self.player)
            for pos in self.board.get_available_spaces()
        ]

    def get_score(self, player: Mark=None) -> float:
        if player is None:
            player = self.player

        if self.board.check_if_win_anywhere(player):
            return 1.0
        if not self.board.get_available_spaces():
            return 0.5
        return 0

    def is_terminal(self) -> bool:
        return (
            not self.board.get_available_spaces()
            or self.board.check_if_win_anywhere(Mark.X)
            or self.board.check_if_win_anywhere(Mark.O)
        )


class RandomAIAgent:
    def get_move(self, state: GameState) -> Action:
        return random.choice(state.get_actions())


class MCTSNode:
    """
    A node in a Monte-Carlo Tree Search tree.

    This represents the score of a given player AFTER taking the action
    associated with this node (TODO: Make sure this logic is followed
    consistently? Seems like it'd be easy for an off-by-1 error to slip in and
    accidentally give the score for the opposite player)
    """
    def __init__(self, action: Action=None):
        self.times_visited = 0
        # It's okay to still only have 1 score when we have multiple different
        # players because we still want to maximize regardless (responding to
        # the best possible opponent strategy by exploring that more is correct
        # behavior)
        self.total_score = 0
        self.action = action
        self.children = {}

    def utc1_score(self, total_parent_visits: int, exploration_rate: float=2.0) -> float:
        if self.times_visited == 0:
            return float('inf')
        # TODO: What's a better name for this variable?
        visited_amount = math.sqrt(math.log(total_parent_visits)/self.times_visited)
        return self.average_score() + exploration_rate * visited_amount

    def average_score(self) -> float:
        if self.times_visited == 0:
            return 0
        return self.total_score / self.times_visited

    def update(self, player_scores: Dict[Mark, float]):
        self.times_visited += 1
        if self.action:
            self.total_score += player_scores.get(self.action.player, 0)

    def expand(self, state: GameState):
        # NOTE: "State" should always be the state assuming we've ALREADY taken
        # this node's action
        actions = state.get_actions()
        self.children = {action: MCTSNode(action) for action in actions}

    def get_best_child(self) -> "MCTSNode":
        nodes_w_scores = {node: node.utc1_score(self.times_visited) for node in self.children.values()}
        return max(nodes_w_scores, key=nodes_w_scores.get)


class MCTSAgent:
    """
    A Monte-Carlo Tree Search implementation that can play tic-tac-toe.
    """
    def get_move(self, state: GameState, iterations: int=1000) -> Point:
        """
        Returns the move to play given the current board state.
        """
        root = MCTSNode()
        root.expand(state)
        for i in range(iterations):
            score = self.mcts(root, state)
            root.update(score)
        return self._get_best_move(root)

    def mcts(self, node: MCTSNode, state: GameState) -> Dict[Mark, float]:
        """
        Evaluates a stochastically-chosen game's outcome and returns its outcome
        for the current player, updating the search subtree contained within the
        given node along the way.
        """
        # NOTE: "State" should always be the state assuming we've ALREADY taken
        # the given node's action
        # TODO: Would it be less confusing to make nodes represent states
        # instead of actions (that way we don't have to worry about if
        # evaluating a node happens "before"/"after" the action takes place?)
        if node.children or node.times_visited > 0:
            if not node.children:
                node.expand(state)
            # Handle edge case where the expanded node still has no children
            # TODO: Is this always because the state is terminal?
            if node.children:
                best_child = node.get_best_child()
                player_scores = self.mcts(
                    best_child, state.get_next_state(best_child.action))
            else:
                player_scores = self.playout(state, node.action.player)
        else:
            player_scores = self.playout(state, node.action.player)
        node.update(player_scores)
        return player_scores

    # TODO:
    def playout(self, state: GameState, player: Mark) -> Dict[Mark, float]:
        current_state = state
        while not current_state.is_terminal():
            random_action = random.choice(current_state.get_actions())
            current_state = current_state.get_next_state(random_action)
        # Get the score for the original player (not the one who won)
        player_score = current_state.get_score(player)
        return {player: player_score}

    def _get_best_move(self, root: MCTSNode) -> Action:
        # NOTE: Should still work, since the child of the root node should still
        # all be counting the scores for the initial player
        actions_w_avg_score = {action: child.average_score() for action, child in root.children.items()}
        return max(actions_w_avg_score, key=actions_w_avg_score.get)