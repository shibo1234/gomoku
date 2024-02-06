import numpy as np
import copy
from typing import Callable, Optional
import time

class TicTacToe4:
    def __init__(self,
                 start_player: int = 1,
                 default_state_formatter: Callable[[tuple[int, ...]], str] = str,
                 size: int = 3):
        self.board = np.zeros(size * size, dtype=int)
        self.player = start_player
        self.default_state_formatter = default_state_formatter
        self.action_history = []
        self.size = size

    @classmethod
    def from_state(cls, state: tuple[int, ...], player: int):
        obj = TicTacToe()
        obj.update_state(state, player)
        return obj

    def __str__(self):
        format_str = '\n+---+---+---+\n|{:^size}|{:^size}|{:^size}|' * self.size + '\n+---+---+---+\n'
        return format_str.format(*np.array([' ', 'X', 'O'])[self.board].tolist())

    # TODO: use __str__
    def render(self, state_formatter: Optional[Callable[[tuple[int, ...]], str]] = None):
        formatter = state_formatter or self.default_state_formatter
        print(formatter(self.get_state()), flush=True)

    # TODO: optimize
    # iterate through all possible lines
    def __iter__(self):
        # for i in range(self.size):
        #     yield self.board[i * self.size: (i + 1) * self.size]
        # for i in range(self.size):
        #     yield self.board[i::self.size]
        #
        # yield self.board[::self.size + 1]
        # yield self.board[self.size - 1: self.size ** 2 - 1: self.size - 1]
        for i in (0, 1, 2, 3):
            yield self.board[i], self.board[i + 4], self.board[i + 8], self.board[i + 12]
        for i in (0, 4, 8, 10):
            yield self.board[i], self.board[i + 1], self.board[i + 2], self.board[i + 3]
        for i in (0,):
            yield self.board[i], self.board[i + 5], self.board[i + 10], self.board[i + 15]
        for i in (3,):
            yield self.board[i], self.board[i + 3], self.board[i + 6], self.board[i + 9]

    def update_state(self, state: tuple[int, ...], player: int):
        self.board = np.array(state, dtype=int)
        self.player = player

    def get_state(self) -> tuple[int, ...]:
        return tuple(self.board.astype(int).tolist())

    def get_actions(self):
        return set(np.where(self.board == 0)[0].tolist())

    def get_winner(self):
        start_time = time.time()
        for first, second, third, fourth in self:
            if first == second == third == fourth != 0:
                end_time = time.time()
                print("花费时间：" + str(end_time - start_time) + "")
                return first
        end_time = time.time()
        print("花费时间：" + str(end_time - start_time) + "")
        return 0

    def get_player(self):
        return self.player

    def get_last_player(self):
        return -self.player

    def is_terminated(self):
        return not self.get_actions() or self.get_winner()
    def clone(self):
        return copy.deepcopy(self)

    def move(self, action):
        if self.board[action] != 0:
            raise Exception("Invalid move")
        self.board[action] = self.player
        self.player = -self.player
        self.action_history.append(action)

    def agent_move(self, policy):
        best_action = policy(self.get_state(), self.player, self.get_actions())
        self.move(best_action)
        return best_action

    def reset(self, start_player=1):
        self.board *= 0
        self.player = start_player

    def spawn(self, action):
        clone = self.clone()
        clone.move(action)
        return clone

    # TODO: value function
    def utility(self, player):
        if self.is_terminated():
            if self.get_winner() == 0:
                return 0
            return 10 if self.get_winner() == player else -10
        return 0

    def last_player(self):
        return -self.player

    def apply_action(self, action):
        if self.board[action] != 0:
            raise Exception("Invalid move")
        self.board[action] = self.player
        self.player = -self.player
        self.action_history.append(action)

    def undo_action(self):
        if not self.action_history:
            raise Exception("No actions to undo")
        last_action = self.action_history.pop()
        self.board[last_action] = 0
        self.player = -self.player
