import numpy as np
import copy
from typing import Callable, Optional

class TicTacToe:

    def __init__(self, start_player: int = 1, default_state_formatter: Callable[[tuple[int, ...]], str] = str):
        self.board = np.zeros(9, dtype=int)
        self.player = start_player
        self.default_state_formatter = default_state_formatter

    @classmethod
    def from_state(cls, state: tuple[int, ...], player: int):
        obj = TicTacToe()
        obj.update_state(state, player)
        return obj

    def __str__(self):
        format_str = '\n+---+---+---+\n|{:^3}|{:^3}|{:^3}|' * 3 + '\n+---+---+---+\n'
        return format_str.format(*np.array([' ', 'X', 'O'])[self.board].tolist())

<<<<<<< HEAD
    def __init__(self, start_player=1, default_state_formatter: Callable[[tuple[int, ...]], str] = str):
        self.board = np.zeros(9)
        self.player = start_player
        self.default_state_formatter = default_state_formatter
        self.action_history = []
=======
    # TODO: use __str__
    def render(self, state_formatter: Optional[Callable[[tuple[int, ...]], str]] = None):
        formatter = state_formatter or self.default_state_formatter
        print(formatter(self.get_state()), flush=True)

    # TODO: optimize
    # iterate through all possible lines
    def __iter__(self):
        for i in (0, 1, 2):
            yield self.board[i], self.board[i + 3], self.board[i + 6]
        for i in (0, 3, 6):
            yield self.board[i], self.board[i + 1], self.board[i + 2]
        for i in (0,):
            yield self.board[i], self.board[i + 4], self.board[i + 8]
        for i in (2,):
            yield self.board[i], self.board[i + 2], self.board[i + 4]

    def update_state(self, state: tuple[int, ...], player: int):
        self.board = np.array(state, dtype=int)
        self.player = player

    def get_state(self) -> tuple[int, ...]:
        return tuple(self.board.astype(int).tolist())

    def get_actions(self):
        return set(np.where(self.board == 0)[0].tolist())

    def get_winner(self):
        for first, second, third in self:
            if first == second == third != 0:
                return first
        return 0

    def get_player(self):
        return self.player

    def get_last_player(self):
        return -self.player

    def get_winner_old(self):
        board = self.board.reshape([3, 3])

        for i in range(3):
            if abs(board[i].sum()) == 3:
                return board[i][0]
            if abs(board[:, i].sum()) == 3:
                return board[0][i]

        for j in range(3):
            if abs(board.diagonal().sum()) == 3:
                return board[0, 0]

            if abs(np.fliplr(board).diagonal().sum()) == 3:
                return int(board[0, 2])
        return 0

    def is_terminated(self):
        return not self.get_actions() or self.get_winner()

    def clone(self):
        return copy.deepcopy(self)
>>>>>>> 1b10709 (heuristic experiment)

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


<<<<<<< HEAD
      for i in range(3):
        if abs(board[i].sum()) == 3:
            return board[i][0]
        if abs(board[:, i].sum()) == 3:
            return board[0][i]

      for j in range(3):
        if abs(board.diagonal().sum()) == 3:
          return board[0, 0]
        
        if abs(np.fliplr(board).diagonal().sum()) == 3:
            return int(board[0, 2]) 
      return 0

    def is_terminated(self):
        return not self.get_actions() or self.get_winner()
    
    def update_state(self, state, player):
        self.board = np.array(state, dtype=int)
        self.player = player
    
    def clone(self):
        return deepcopy(self)

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
=======
>>>>>>> 1b10709 (heuristic experiment)
