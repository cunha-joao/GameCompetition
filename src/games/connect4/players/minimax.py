from games.connect4.player import Connect4Player
from games.connect4.action import Connect4Action
from games.connect4.state import Connect4State
from games.state import State
import math

class MinimaxConnect4Player(Connect4Player):
    def __init__(self, name, depth=5):
        super().__init__(name)
        self.depth = depth
        self.transposition_table = {}

    def get_action(self, state: Connect4State):
        best_score = -math.inf
        best_action = None

        possible_actions = state.get_possible_actions()
        ordered_actions = sorted(possible_actions, key=lambda action: abs(action.get_col() - state.get_num_cols() // 2))

        for depth in range(1, self.depth + 1):
            for action in ordered_actions:
                value = self.minimax(state, depth, -math.inf, math.inf, True, action)
                if value > best_score:
                    best_score = value
                    best_action = action

        return best_action

    def minimax(self, state, depth, alpha, beta, maximizing_player, action):
        state_key = str(state.get_grid()) + str(maximizing_player)
        if state_key in self.transposition_table and self.transposition_table[state_key][0] >= depth:
            return self.transposition_table[state_key][1]

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

            self.transposition_table[state_key] = (depth, max_eval)
            return max_eval
        else:
            min_eval = math.inf
            for action in cloned_state.get_possible_actions():
                eval = self.minimax(cloned_state.clone(), depth - 1, alpha, beta, True, action)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            self.transposition_table[state_key] = (depth, min_eval)
            return min_eval

    def __heuristic(self, state: Connect4State):
        grid = state.get_grid()
        longest_self = 0
        longest_opponent = 0
        potential_wins_self = 0
        potential_wins_opponent = 0

        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols()):
                if grid[row][col] == self.get_current_pos():
                    longest_self, potential_wins_self = self.__evaluate_position(grid, row, col, longest_self, potential_wins_self, self.get_current_pos())
                elif grid[row][col] != 0:
                    longest_opponent, potential_wins_opponent = self.__evaluate_position(grid, row, col, longest_opponent, potential_wins_opponent, grid[row][col])

        return (longest_self - longest_opponent) + (potential_wins_self - potential_wins_opponent)

    def __evaluate_position(self, grid, row, col, longest, potential_wins, player):
        if col <= len(grid[0]) - 4:
            sequence = self.__count_sequence(grid, row, col, 0, 1, player)
            longest = max(longest, sequence)
            if sequence >= 3:
                potential_wins += 1
        if row <= len(grid) - 4:
            sequence = self.__count_sequence(grid, row, col, 1, 0, player)
            longest = max(longest, sequence)
            if sequence >= 3:
                potential_wins += 1
        if col <= len(grid[0]) - 4 and row <= len(grid) - 4:
            sequence = self.__count_sequence(grid, row, col, 1, 1, player)
            longest = max(longest, sequence)
            if sequence >= 3:
                potential_wins += 1
        if col <= len(grid[0]) - 4 and row >= 3:
            sequence = self.__count_sequence(grid, row, col, -1, 1, player)
            longest = max(longest, sequence)
            if sequence >= 3:
                potential_wins += 1
        return longest, potential_wins

    def __count_sequence(self, grid, row, col, d_row, d_col, player):
        count = 0
        while 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] == player:
            count += 1
            row += d_row
            col += d_col
        return count

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass

