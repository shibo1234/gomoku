import random
from copy import deepcopy
from src.value_functions import BaseValueFunction
import math
from .base_q_policy import BaseQPolicySingle
from typing import Optional
from src.tictactoe import TicTacToe


class TreeNode():
    def __init__(self, game, parent):
        self.game = game
        self.state = game.get_state()
        self.actions = game.get_actions()
        self.is_terminated = game.is_terminated()
        self.fully_expand = self.is_terminated
        self.parent = parent
        self.num_visited = 0
        self.total_reward = 0
        self.children = {}
        self.visited = False
        self.depth = 0
        # heuristic call
        # self.layer = self.parent.layer + 1 if parent is not None else 0

class MCTS(BaseQPolicySingle):
    def __init__(self, game_cls,
                 heuristic: Optional[BaseValueFunction] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_cls = game_cls
        self.root = None
        self.iteration = 2000
        self.exploration_constant = 1 / math.sqrt(2)
        self.heuristic = heuristic

    def select_child(self, node):
        while not node.is_terminated:
            if node.fully_expand:
                new_node = self.get_best_move(node, self.exploration_constant)
                if new_node is None:
                    raise Exception("No best move found")
                node = new_node
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.actions
        for action in actions:
            if action not in node.children:
                new_game = deepcopy(node.game)
                new_game.move(action)
                new_node = TreeNode(new_game, node)
                node.children[action] = new_node
                if len(actions) == len(node.children):
                    node.fully_expand = True
                return new_node
        raise Exception("No actions to expand")

    def simulated_game(self, node, cloned_game, limit=3):
        # if node.depth >= limit:
        #     return self.heuristic.get_V(node.game.get_state(), cloned_game.player, node.game.get_actions())
        # else:
            return self.simulate_by_sampling(node, cloned_game)

    def simulate_by_sampling(self, node, cloned_game,limit=3):
        new_game = deepcopy(node.game)
        while not new_game.is_terminated():
            possible_actions = new_game.get_actions()
            action = random.choice(list(possible_actions))
            new_game.move(action)
            # node.depth += 1
            # if node.depth >= limit:
            #     return self.heuristic.get_V(node.game.get_state(), cloned_game.player, node.game.get_actions())
        if node.game.get_winner() == cloned_game.player:
            return 10
        elif node.game.get_winner() == 0:
            return 0
        else:
            return -10

    def execute_round(self, cloned_game):
        """
        execute a selection-expansion-simulation-backpropagation round
        """
        node = self.select_child(self.root)
        reward = self.simulated_game(node, cloned_game,3)
        self.back_propogate(node, reward)

    def back_propogate(self, node, reward):
        while node is not None:
            node.visited = True
            node.num_visited += 1
            node.total_reward += reward
            reward = -reward
            node = node.parent

    def get_best_move(self, node, exploration_constant):
        best_value = float("-inf")
        best_nodes = []
        for action, child in node.children.items():
            node_value = (child.total_reward / child.num_visited
                          + exploration_constant * math.sqrt(2 * math.log(node.num_visited) / child.num_visited))
            if node_value > best_value:
                best_value = node_value
                best_nodes = [child]
            elif node_value == best_value:
                best_nodes.append(child)
        return random.choice(best_nodes) if best_nodes else None

    def get_all_Qs(self, state: tuple[int, ...], player: int, action_space: set[int]) -> dict[int, float]:
        action_scores = {}
        if math.factorial(len(action_space)) <= self.iteration:
            for action in action_space:
                new_game = self.game_cls.from_state(state, player)
                cloned_game = new_game.clone()
                new_game.move(action)
                score = self.min_max(new_game, False, cloned_game, depth=3)
                action_scores[action] = score
        else:
            self.root = TreeNode(self.game_cls.from_state(state, player), None)
            cloned_game = self.game_cls.from_state(state, player)
            for _ in range(self.iteration):
                self.execute_round(cloned_game)
            for action in action_space:
                child_node = self.root.children.get(action)
                action_scores[action] = child_node.total_reward

        return action_scores

    def min_max(self, game: TicTacToe, is_max_player, cloned_game, depth):
        if game.is_terminated():
            winner = game.get_winner()
            if winner == cloned_game.player:
                return 10
            elif winner == 0:
                return 0
            else:
                return -10
        if depth == 0:
            return self.heuristic.get_V(game.get_state(), cloned_game.player, game.get_actions())

        best_score = -float('inf') if is_max_player else float('inf')
        for action in game.get_actions():
            game.apply_action(action)
            score = self.min_max(game, not is_max_player, cloned_game, depth - 1)
            game.undo_action()
            if (is_max_player and score > best_score) or (not is_max_player and score < best_score):
                best_score = score
        return best_score

    def update_Q(self, state: tuple[int, ...], player: int, action: int, Q: float) -> None:
        raise NotImplementedError
