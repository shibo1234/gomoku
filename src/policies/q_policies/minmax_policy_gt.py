from .base_q_policy import BaseQPolicySingle
from src.value_functions import BaseValueFunction
from src.value_functions import TTTHeuristicValueFunctionGT

from typing import Optional

class MinMaxPolicyGT(BaseQPolicySingle):
    # TODO: BaseGame
    def __init__(self,
                 game_cls: type,
                 max_depth: Optional[int] = None,
                 heuristic: Optional[BaseValueFunction] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_cls = game_cls
        self.max_depth = max_depth
        self.heuristic = heuristic

    def _max_utility_actions(self, game, player, depth=None):
        if game.is_terminated():
            return game.utility(player), set()
        if depth is not None and depth == 0:
            return self.heuristic.get_V(game.get_state(), player, game.get_actions()), set()
        utility_map = dict()
        best_set = set()
        max_utility = None
        for action in game.get_actions():
            result = game.spawn(action)
            next_depth = None if depth is None else depth - 1
            min_utility, _ = self._min_utility_actions(result, player, next_depth)
            utility_map[action] = min_utility
            if max_utility is None:
                max_utility = min_utility
            elif max_utility < min_utility:
                max_utility = min_utility
        for action, utility in utility_map.items():
            if utility == max_utility:
                best_set.add(action)
        return max_utility, best_set

    def _min_utility_actions(self, game, player, depth=None):
        if game.is_terminated():
            return game.utility(player), set()
        if depth is not None and depth == 0:
            return self.heuristic.get_V(game.get_state(), player, game.get_actions()), set()
        utility_map = dict()
        best_set = set()
        min_utility = None
        for action in game.get_actions():
            result = game.spawn(action)
            next_depth = None if depth is None else depth - 1
            max_utility, _ = self._max_utility_actions(result, player, next_depth)
            utility_map[action] = max_utility
            if min_utility is None:
                min_utility = max_utility
            elif min_utility > max_utility:
                min_utility = max_utility
        for action, utility in utility_map.items():
            if utility == min_utility:
                best_set.add(action)
        return min_utility, best_set

    def h_minimax_search(self, game):
        return self._max_utility_actions(game,
                                         game.player, self.max_depth)

    def get_all_Qs(self, state: tuple[int, ...], player: int, action_space: set[int]) -> dict[int, float]:
        q_dict = dict()
        game = self.game_cls.from_state(state, player)
        for action in action_space:
            sub_game = game.spawn(action)
            q_dict[action] = self._min_utility_actions(sub_game, player, self.max_depth-1)[0]
        return q_dict

    def update_Q(self, state: tuple[int, ...], player: int, action: int, Q: float) -> None:
        raise NotImplementedError

