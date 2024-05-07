from games.connect4.action import Connect4Action
from games.connect4.player import Connect4Player
from games.connect4.state import Connect4State
from games.state import State


class SurefireConnect4Player(Connect4Player):

    def __init__(self, name):
        super().__init__(name)
        self.first_move_done = False

    def get_action(self, state: Connect4State):
        if not self.first_move_done:
            self.first_move_done = True
            return Connect4Action(state.get_num_cols() // 2)

        best_action = self.heuristic_evaluation(state)

        return best_action

    def heuristic_evaluation(self, state: Connect4State):
        central_column = state.get_num_cols() // 2

        possible_actions = state.get_possible_actions()

        distances_to_central_column = [abs(action.get_col() - central_column) for action in possible_actions]

        best_action_index = distances_to_central_column.index(min(distances_to_central_column))
        best_action = possible_actions[best_action_index]

        return best_action

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
