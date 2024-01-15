import numpy as np
from copy import deepcopy
from typing import Callable, Optional


class TicTacToe(object):

    @classmethod
    def from_state(cls, state: tuple[int, ...], player: int):
        obj = TicTacToe()
        obj.board = np.array(state)
        obj.player = player
        return obj

    @classmethod
    def eval(cls, state, player):
        pass

    def __init__(self, start_player=1, default_state_formatter: Callable[[tuple[int, ...]], str] = str):
        self.board = np.zeros(9)
        self.player = start_player
        self.default_state_formatter = default_state_formatter
        self.action_history = []

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
        self.board = np.zeros(9)
        self.player = start_player
        
    def render(self, state_formatter: Optional[Callable[[tuple[int, ...]], str]] = None):
        formatter = state_formatter or self.default_state_formatter
        print(formatter(self.get_state()), flush=True)

    def get_state(self) -> tuple[int, ...]:
        return tuple(self.board.astype(int).tolist())

    def get_actions(self):
        return set(np.where(self.board == 0)[0].tolist())

    def get_winner(self):
      board = self.board.reshape([3,3])

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
