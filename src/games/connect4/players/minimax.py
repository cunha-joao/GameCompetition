from games.connect4.player import Connect4Player
from games.connect4.action import Connect4Action
from games.connect4.state import Connect4State
from games.state import State
import math

class MinimaxConnect4Player(Connect4Player):
    def __init__(self, name, depth=4):
        super().__init__(name)
        self.depth = depth

    def get_action(self, state: Connect4State):
        best_score = float('-inf')
        best_action = None

        for action in state.get_possible_actions():
            value = self.minimax(state, self.depth, float('-inf'), float('inf'), True, action)
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
            max_eval = float('-inf')
            for action in cloned_state.get_possible_actions():
                eval = self.minimax(cloned_state.clone(), depth - 1, alpha, beta, False, action)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for action in cloned_state.get_possible_actions():
                eval = self.minimax(cloned_state.clone(), depth - 1, alpha, beta, True, action)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def __heuristic(self, state: Connect4State):
        grid = state.get_grid()
        longest = 0

        # check each line
        for row in range(0, state.get_num_rows()):
            seq = 0
            for col in range(0, state.get_num_cols()):
                if grid[row][col] == self.get_current_pos():
                    seq += 1
                else:
                    if seq > longest:
                        longest = seq
                    seq = 0

            if seq > longest:
                longest = seq

        # check each column
        for col in range(0, state.get_num_cols()):
            seq = 0
            for row in range(0, state.get_num_rows()):
                if grid[row][col] == self.get_current_pos():
                    seq += 1
                else:
                    if seq > longest:
                        longest = seq
                    seq = 0

            if seq > longest:
                longest = seq

        # check each upward diagonal
        for row in range(3, state.get_num_rows()):
            for col in range(0, state.get_num_cols() - 3):
                seq1 = (1 if grid[row][col] == self.get_current_pos() else 0) + \
                       (1 if grid[row - 1][col + 1] == self.get_current_pos() else 0) + \
                       (1 if grid[row - 2][col + 2] == self.get_current_pos() else 0)

                seq2 = (1 if grid[row - 1][col + 1] == self.get_current_pos() else 0) + \
                       (1 if grid[row - 2][col + 2] == self.get_current_pos() else 0) + \
                       (1 if grid[row - 3][col + 3] == self.get_current_pos() else 0)

                if seq1 > longest:
                    longest = seq1

                if seq2 > longest:
                    longest = seq2

        # check each downward diagonal
        for row in range(0, state.get_num_rows() - 3):
            for col in range(0, state.get_num_cols() - 3):
                seq1 = (1 if grid[row][col] == self.get_current_pos() else 0) + \
                       (1 if grid[row + 1][col + 1] == self.get_current_pos() else 0) + \
                       (1 if grid[row + 2][col + 2] == self.get_current_pos() else 0)

                seq2 = (1 if grid[row + 1][col + 1] == self.get_current_pos() else 0) + \
                       (1 if grid[row + 2][col + 2] == self.get_current_pos() else 0) + \
                       (1 if grid[row + 3][col + 3] == self.get_current_pos() else 0)

                if seq1 > longest:
                    longest = seq1

                if seq2 > longest:
                    longest = seq2

        return longest

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass