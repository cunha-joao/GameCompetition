from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.action import MinesweeperAction
from games.minesweeper.state import MinesweeperState


class MonteCarloMinesweeperPlayer(MinesweeperPlayer):
    def __init__(self, name, num_simulations=1):
        super().__init__(name)
        self.num_simulations = num_simulations

    def get_action(self, state: MinesweeperState):
        possible_actions = list(state.get_possible_actions())
        if not possible_actions:
            return None

        # Dicionário para armazenar a contagem de vezes que cada ação resulta em mina
        mine_count = {action: 0 for action in possible_actions}

        # Simular cada ação para estimar o risco
        for action in possible_actions:
            for _ in range(self.num_simulations):
                simulated_state = state.clone()
                simulated_state.update(action)
                if simulated_state.get_grid()[action.get_row()][action.get_col()] == MinesweeperState.MINE_CELL:
                    mine_count[action] += 1

        # Ação com a menor probabilidade de ser uma mina
        best_action = min(mine_count, key=mine_count.get)
        return best_action

    def event_action(self, pos: int, action, new_state):
        # Este método pode ser usado para registrar ações ou resultados
        pass

    def event_end_game(self, final_state):
        # Este método pode ser usado para limpeza ou análise no final do jogo
        pass
