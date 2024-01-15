from .base_q_policy import BaseQPolicySingle
from src.heuristics import TicTacToeHeuristic
from src.tictactoe import TicTacToe


class MinMaxPolicy(BaseQPolicySingle):
    def __init__(self, game_cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_cls = game_cls
        self.heuristic = TicTacToeHeuristic()

    def min_max(self, game: TicTacToe, is_max_player, cloned_game, depth):
        if game.is_terminated() and depth <= 3:
            winner = game.get_winner()
            if winner == cloned_game.player:
                return 10
            elif winner == 0:
                return 0
            else:
                return -10
        if depth > 3:
            return self.heuristic(game.get_state(), cloned_game.player)

        best_score = -float('inf') if is_max_player else float('inf')
        for action in game.get_actions():
            new_game = game.clone()
            new_game.move(action)
            score = self.min_max(new_game, not is_max_player, cloned_game, depth+1)
            if (is_max_player and score > best_score) or (not is_max_player and score < best_score):
                best_score = score
        return best_score

    def get_all_Qs(self, state: tuple[int, ...], player: int, action_space: set[int]) -> dict[int, float]:
        q_values = {}
        for action in action_space:
            new_game = self.game_cls.from_state(state, player)
            cloned_game = new_game.clone()
            new_game.move(action)
            score = self.min_max(new_game, False, cloned_game, depth=0)
            q_values[action] = score
        return q_values

    def update_Q(self, state: tuple[int, ...], player: int, action: int, Q: float) -> None:
        raise NotImplementedError

