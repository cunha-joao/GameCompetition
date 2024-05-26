import heapq
from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState
from games.state import State

class AStarMinesweeperPlayer(MinesweeperPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: MinesweeperState):
        grid = state.get_grid()
        num_rows = state.get_num_rows()
        num_cols = state.get_num_cols()
        possible_actions = list(state.get_possible_actions())

        # Use a priority queue to select the best action based on A*
        open_list = []
        for index, action in enumerate(possible_actions):
            g_cost = self.calculate_cost(grid, action, num_rows, num_cols)
            h_cost = self.heuristic(grid, action, num_rows, num_cols)
            f_cost = g_cost + h_cost
            heapq.heappush(open_list, (f_cost, index, action))

        # Return the action with the lowest f_cost
        _, _, best_action = heapq.heappop(open_list)
        return best_action

    @staticmethod
    def calculate_cost(grid, action, num_rows, num_cols):
        row, col = action.get_row(), action.get_col()
        if grid[row][col] != MinesweeperState.EMPTY_CELL:
            return float('inf')  # Already revealed or marked

        # Cost based on the number of adjacent mines
        cost = 0
        for r in range(max(0, row - 1), min(num_rows, row + 2)):
            for c in range(max(0, col - 1), min(num_cols, col + 2)):
                if grid[r][c] > 0:  # Cell is a number
                    cost += grid[r][c]

        return cost

    @staticmethod
    def heuristic(grid, action, num_rows, num_cols):
        row, col = action.get_row(), action.get_col()

        # Heuristic based on the number of unrevealed neighbors
        unrevealed_neighbors = AStarMinesweeperPlayer.count_unrevealed_neighbors(grid, row, col, num_rows, num_cols)
        return unrevealed_neighbors

    @staticmethod
    def count_unrevealed_neighbors(grid, row, col, num_rows, num_cols):
        count = 0
        for r in range(max(0, row - 1), min(num_rows, row + 2)):
            for c in range(max(0, col - 1), min(num_cols, col + 2)):
                if (r != row or c != col) and grid[r][c] == MinesweeperState.EMPTY_CELL:
                    count += 1
        return count

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
