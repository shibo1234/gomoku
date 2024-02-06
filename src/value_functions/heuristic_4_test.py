from .base_value_function import BaseValueFunctionSingle
import random

# TODO: Try to add difference according to the next stone by which player.
# TODO: Rename constants.
# TODO: Add more scores according to patterns.
# There are logical issues about possible number of stones in a line.

COEFFICIENT_value_score1 = 1
CONSTANT_value_total = 12

COEFFICIENT_value_line_valueless = 1
CONSTANT_value_line_10 = 1
CONSTANT_value_line_20 = 3
CONSTANT_value_line_30 = 6
CONSTANT_value_line_01 = -1
CONSTANT_value_line_02 = -5
CONSTANT_value_line_03 = -CONSTANT_value_total

class Heuristic_4(BaseValueFunctionSingle):
    '''
    Heuristic for 4 * 4 Gomoku
    '''
    def __init__(self, board_size: int = 4, win_size: int = 4, player_1: int = 1, player_2: int = -1, empty: int = 0):
        '''
        :param board_size: the size of the board (grid)
        :param win_size: how many stones in a line adjacently to win
        :param player_1:
        :param player_2:
        :param empty:
        '''
        super().__init__()
        self.board_size = board_size
        self.win_size = win_size
        self.player_1 = player_1
        self.player_2 = player_2
        self.empty = empty

    @staticmethod
    def one_dim_to_two_dim(board_size: int, state_1d: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
        '''
        :param state_1d: 1d state
        :return: 2d state
        '''
        state_2d = [[None for _ in range(board_size)]for _ in range(board_size)]
        for i in range(board_size):
            for j in range(board_size):
                state_2d[i][j] = state_1d[i * board_size + j]
        state_2d = tuple(tuple(row) for row in state_2d)
        return state_2d

    @staticmethod
    def two_dim_to_one_dim(board_size: int, state_2d: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
        '''
        :param state_2d: 2d state
        :return: 1d state
        '''
        state_1d = [None for _ in range(board_size ** 2)]
        for i in range(board_size):
            for j in range(board_size):
                state_1d[i * board_size + j] = state_2d[i][j]
        state_1d = tuple(state_1d)
        return state_1d

    @staticmethod
    def value_line(board_size: int, win_size: int, line_num_player, line_num_blank, line_num_rival):
        '''
        :param board_size:
        :param win_size:
        :param line_num_player:
        :param line_num_blank:
        :param line_num_rival:
        :return: the score1 of a line
        '''
        if line_num_rival >= 1 and line_num_player >= 1:
            return (line_num_rival - line_num_blank) * COEFFICIENT_value_line_valueless
        elif line_num_player == 0:
            if line_num_rival == 0:
                return 0
            elif line_num_rival == 1:
                return CONSTANT_value_line_01
            elif line_num_rival == 2:
                return CONSTANT_value_line_02
            elif line_num_rival == 3:
                return CONSTANT_value_line_03
        else:
            if line_num_player == 1:
                return CONSTANT_value_line_10
            elif line_num_player == 2:
                return CONSTANT_value_line_20
            elif line_num_player == 3:
                return CONSTANT_value_line_30
    def get_V(self, state_1d: tuple[int, ...], player: int, action_space: set[int]) -> float:
        '''
        :param state_1d:
        :param player:
        :param action_space:
        :return: heuristic value
        '''
        sign = 1 if player == self.player_1 else -1
        score = random.uniform(0,1)
        return score * sign


