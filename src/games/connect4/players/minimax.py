import math
from games.connect4.action import Connect4Action
from games.connect4.result import Connect4Result
from games.connect4.state import Connect4State
from games.connect4.player import Connect4Player
from games.state import State


class MinimaxConnect4Player(Connect4Player):
    def __init__(self, name):
        super().__init__(name)

    def __heuristic(self, state: Connect4State):
        grid = state.get_grid()
        longest = 0

        # Check each line
        for row in range(state.get_num_rows()):
            for col in range(state.get_num_cols() - 3):
                if grid[row][col] == self.get_current_pos():
                    if grid[row][col + 1] == grid[row][col + 2] == grid[row][col + 3] == self.get_current_pos():
                        return math.inf  # Winning move
                    longest = max(longest, 1)
                    for i in range(1, 4):
                        if grid[row][col + i] == self.get_current_pos():
                            longest += 1
                        else:
                            break

        # Check each column
        for col in range(state.get_num_cols()):
            for row in range(state.get_num_rows() - 3):
                if grid[row][col] == self.get_current_pos():
                    if grid[row + 1][col] == grid[row + 2][col] == grid[row + 3][col] == self.get_current_pos():
                        return math.inf  # Winning move
                    longest = max(longest, 1)
                    for i in range(1, 4):
                        if grid[row + i][col] == self.get_current_pos():
                            longest += 1
                        else:
                            break

        # Check each diagonal
        for row in range(state.get_num_rows() - 3):
            for col in range(state.get_num_cols() - 3):
                if grid[row][col] == self.get_current_pos():
                    if grid[row + 1][col + 1] == grid[row + 2][col + 2] == grid[row + 3][col + 3] == self.get_current_pos():
                        return math.inf  # Winning move
                    longest = max(longest, 1)
                    for i in range(1, 4):
                        if grid[row + i][col + i] == self.get_current_pos():
                            longest += 1
                        else:
                            break

        # Check each anti-diagonal
        for row in range(3, state.get_num_rows()):
            for col in range(state.get_num_cols() - 3):
                if grid[row][col] == self.get_current_pos():
                    if grid[row - 1][col + 1] == grid[row - 2][col + 2] == grid[row - 3][col + 3] == self.get_current_pos():
                        return math.inf  # Winning move
                    longest = max(longest, 1)
                    for i in range(1, 4):
                        if grid[row - i][col + i] == self.get_current_pos():
                            longest += 1
                        else:
                            break

        return longest

    def minimax(self, state: Connect4State, depth: int, alpha: int = -math.inf, beta: int = math.inf,
                is_initial_node: bool = True):

        if state.is_finished():
            result = state.get_result(self.get_current_pos())
            if result == Connect4Result.WIN:
                return 1000000
            elif result == Connect4Result.LOOSE:
                return -1000000
            elif result == Connect4Result.DRAW:
                return 0

        if depth == 0:
            return self.__heuristic(state)

        if self.get_current_pos() == state.get_acting_player():
            value = -math.inf
            selected_action = None

            for action in state.get_possible_actions():
                pre_value = value
                next_state = state.clone()
                next_state.update(action)
                value = max(value, self.minimax(next_state, depth - 1, alpha, beta, False))
                if value > pre_value:
                    selected_action = action
                if value >= beta:
                    break
                alpha = max(alpha, value)

            return selected_action if is_initial_node else value

        else:
            value = math.inf

            for action in state.get_possible_actions():
                next_state = state.clone()
                next_state.update(action)
                value = min(value, self.minimax(next_state, depth - 1, alpha, beta, True))
                if value <= alpha:
                    break
                beta = min(beta, value)

            return value

    def get_action(self, state: Connect4State):
        return self.minimax(state, 10)

    def event_action(self, pos: int, action, new_state: State):
        # Ignore
        pass

    def event_end_game(self, final_state: State):
        # Ignore
        pass
