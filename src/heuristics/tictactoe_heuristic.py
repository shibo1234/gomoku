import numpy as np


class TicTacToeHeuristic():
    def __init__(self):
        pass

    def __call__(self, state: tuple[int, ...], player: int) -> float:
        # p means current player
        # a means opponent player
        a1 = a2 = p1 = p2 = 0
        curr_state = np.array(state).reshape(3, 3)
        temp_state = curr_state.copy()

        curr_state[temp_state == player] = 1
        curr_state[(temp_state != player) & (temp_state != 0)] = -1

        lines = list(curr_state[:]) + list(curr_state.T[:]) + [np.diag(curr_state)] + [np.diag(np.fliplr(curr_state))]
        for line in lines:
            unique, counts = np.unique(line, return_counts=True)
            counts_dict = dict(zip(unique, counts))
            if 1 in counts_dict and -1 not in counts_dict:
                if counts_dict[1] == 1:
                    p1 += 1
                elif counts_dict[1] == 2:
                    p2 += 1
            if -1 in counts_dict and 1 not in counts_dict:
                if counts_dict[-1] == 1:
                    a1 += 1
                elif counts_dict[-1] == 2:
                    a2 += 1

        scores = {'p1': p1, 'p2': p2, 'a1': a1, 'a2': a2}

        return scores['p1'] + scores['p2'] * 3 - scores['a2'] * 3 - scores['a1']





