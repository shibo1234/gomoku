from .base_q_policy import BaseQPolicySingle


class MinMaxPolicy(BaseQPolicySingle):
    def __init__(self, game_cls):
        super().__init__()
        self.game_cls = game_cls


    def min_max(self, game, is_max_player):
        if game.is_terminated():
            winner = game.get_winner()
            if winner == self.original_player:
                return None, 1
            elif winner == 0:
                return None, 0
            else:
                return None, -1

        best_score = -float('inf') if is_max_player else float('inf')
        best_action = None
        new_game = game.clone()
        new_game.move(action)
         _, score = self.min_max(new_game, not is_max_player)
        if is_max_player and score > best_score or not is_max_player and score < best_score:
            best_score = score
            best_action = action

        return best_action, best_score

    def get_all_Qs(self, state: tuple[int], action_space: set[int]) -> dict[int, float]:
        q_values = {}
        for action in action_space:
            new_game = self.game_cls.from_state(state, self.original_player)
            new_game.move(action)
            score = self.min_max(new_game, new_game.last_player() != self.original_player)
            q_values[action] = score
        return q_values


    def update_Q(self, state: tuple[int], action: int, Q: float) -> None:
        raise NotImplementedError

