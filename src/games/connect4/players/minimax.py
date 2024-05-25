from games.connect4.player import Connect4Player
from games.connect4.action import Connect4Action
from games.connect4.state import Connect4State
from games.state import State
import math

class MinimaxConnect4Player(Connect4Player):
    def __init__(self, name, depth=5):
        super().__init__(name)
        self.depth = depth

    def get_action(self, state: Connect4State):
        best_score = -math.inf
        best_action = None

        for action in state.get_possible_actions():
            value = self.minimax(state, self.depth, -math.inf, math.inf, True, action)
            if value > best_score:
                best_score = value
                best_action = action

        return best_action

    def minimax(self, state, depth, alpha, beta, maximizing_player, action):
        cloned_state = state.clone()
        cloned_state.update(action)

        if depth == 0 or cloned_state.is_finished():
            return self.__heuristic(cloned_state)

        if maximizing_player:
            max_eval = -math.inf
            for action in cloned_state.get_possible_actions():
                eval = self.minimax(cloned_state.clone(), depth - 1, alpha, beta, False, action)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for action in cloned_state.get_possible_actions():
                eval = self.minimax(cloned_state.clone(), depth - 1, alpha, beta, True, action)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def __heuristic(self, state: Connect4State):
        grid = state.get_grid()
        longest_self = 0
        longest_opponent = 0

        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols()):
                if grid[row][col] == self.get_current_pos():
                    if col <= state.get_num_cols() - 4:
                        longest_self = max(longest_self, self.__count_sequence(grid, row, col, 0, 1))
                    if row <= state.get_num_rows() - 4:
                        longest_self = max(longest_self, self.__count_sequence(grid, row, col, 1, 0))
                    if col <= state.get_num_cols() - 4 and row <= state.get_num_rows() - 4:
                        longest_self = max(longest_self, self.__count_sequence(grid, row, col, 1, 1))
                    if col <= state.get_num_cols() - 4 and row >= 3:
                        longest_self = max(longest_self, self.__count_sequence(grid, row, col, -1, 1))
                elif grid[row][col] != 0:
                    if col <= state.get_num_cols() - 4:
                        longest_opponent = max(longest_opponent, self.__count_sequence(grid, row, col, 0, 1))
                    if row <= state.get_num_rows() - 4:
                        longest_opponent = max(longest_opponent, self.__count_sequence(grid, row, col, 1, 0))
                    if col <= state.get_num_cols() - 4 and row <= state.get_num_rows() - 4:
                        longest_opponent = max(longest_opponent, self.__count_sequence(grid, row, col, 1, 1))
                    if col <= state.get_num_cols() - 4 and row >= 3:
                        longest_opponent = max(longest_opponent, self.__count_sequence(grid, row, col, -1, 1))

        return longest_self - longest_opponent

    def __count_sequence(self, grid, row, col, d_row, d_col):
        current_pos = grid[row][col]
        if current_pos == 0:
            return 0
        count = 1
        r, c = row + d_row, col + d_col
        while 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == current_pos:
            count += 1
            r += d_row
            c += d_col
        return count

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
