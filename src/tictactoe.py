import numpy as np
from copy import deepcopy


class TicTacToe(object):
    def __init__(self, start_player=1):
        self.board = np.zeros(9)
        self.player = start_player

    def move(self, action):
        if self.board[action] != 0:
            raise Exception("Invalid move")
        self.board[action] = self.player
        self.player = -self.player

    def agent_move(self, policy):
        best_action = policy(self.get_state(), self.player, self.get_actions())
        self.move(best_action)
        return best_action
        
    def reset(self, start_player=1):
        self.board = np.zeros(9)
        self.player = start_player
        
    def render(self):
        print(self.board.reshape([3, 3]))

    def get_state(self):
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