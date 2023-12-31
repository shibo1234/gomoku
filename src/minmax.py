

class MinMax:
    def __init__(self, game):
        self.game = game
        self.original_player = game.last_player()
        print(game.original_player)

    def min_max(self, game, is_max_player):
        if game.is_terminated():
            winner = game.get_winner()
            if winner == self.original_player:
                return None, 1
            elif winner == 0:
                return None, 0
            else:
                return None, -1

        if is_max_player:
            best_score = -float('inf')
            best_action = None
            for action in game.get_actions():
                new_game = game.clone()
                print("当前的action: ", action)
                new_game.move(action)
                print("当前进入递归的玩家： ", new_game.player)
                _, score = self.min_max(new_game, True)
                if score > best_score:
                    best_score = score
                    best_action = action
                print("max_player: ", new_game.player, "best_action: ", best_action, "best_score: ", best_score)
            return best_action, best_score
        else:
            best_score = float('inf')
            best_action = None
            for action in game.get_actions():
                new_game = game.clone()
                print("当前的action: ", action)
                new_game.move(action)
                print("当前递归的玩家： ", new_game.player)
                _, score = self.min_max(new_game, False)
                if score < best_score:
                    best_score = score
                    best_action = action
                print("min_player: ", new_game.player, "best_action: ", best_action, "best_score: ", best_score)
            return best_action, best_score

    def best_move(self):
        action, _ = self.min_max(self.game,  False)
        print("传进来的玩家: ", self.original_player)
        return action