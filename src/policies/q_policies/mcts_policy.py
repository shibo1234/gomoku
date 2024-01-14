import random
from copy import deepcopy
import math
from .base_q_policy import BaseQPolicySingle


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
        self.q_values = {action: 0 for action in self.actions}


class MCTS(BaseQPolicySingle):
    def __init__(self, game_cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_cls = game_cls
        self.root = None
        self.iteration = 2000
        self.exploration_constant = 1 / math.sqrt(2)

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

    def simulated_game(self, node):
        self.visited = True
        if math.factorial(len(node.game.get_actions())) <= self.iteration:
            return self.simulate_by_brute_force(node)
        else:
            return self.simulate_by_sampling(node)

    def simulate_by_brute_force(self, node):
        if node.game.is_terminated():
            return self.calculate_reward(node)
        outcomes = []
        for action in node.game.get_actions():
            new_game = deepcopy(node.game)
            new_game.move(action)
            child_node = TreeNode(new_game, node)
            outcome = self.simulated_game(child_node)
            outcomes.append(outcome)
        return max(outcomes)

    def simulate_by_sampling(self, node):
        new_game = deepcopy(node.game)
        while not new_game.is_terminated():
            possible_actions = new_game.get_actions()
            action = random.choice(list(possible_actions))
            new_game.move(action)

        return self.calculate_reward(TreeNode(new_game, node))

    def calculate_reward(self, node):
        winner = node.game.get_winner()
        if winner == node.game.player:
            return -1
        elif winner == 0:
            return 0
        else:
            return 1

    def execute_round(self):
        """
        execute a selection-expansion-simulation-backpropagation round

        """
        node = self.select_child(self.root)
        reward = self.simulated_game(node)
        self.back_propogate(node, reward)

    def back_propogate(self, node, reward):
        while node is not None:
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
        self.root = TreeNode(self.game_cls.from_state(state, player), None)

        for _ in range(self.iteration):
            self.execute_round()

        action_scores = {}
        for action in action_space:
            child_node = self.root.children.get(action)
            if child_node and child_node.num_visited > 0:
                action_scores[action] = child_node.total_reward / child_node.num_visited
            else:
                action_scores[action] = 0

        return action_scores

    def find_node_matching_state(self, node, state):
        if node is None:
            return None
        if node.state == state:
            return node
        for child in node.children.values():
            result = self.find_node_matching_state(child, state)
            if result is not None:
                return result
        return None

    def update_Q(self, state: tuple[int, ...], player: int, action: int, Q: float) -> None:
        raise NotImplementedError
