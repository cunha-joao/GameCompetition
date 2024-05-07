from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.action import HLPokerAction
from games.hlpoker.round import Round
from games.hlpoker.state import HLPokerState
from games.state import State
import random

class ExpectimaxHLPokerPlayer(HLPokerPlayer):
    def __init__(self, name):
        super().__init__(name)

    def get_action_with_cards(self, state: HLPokerState, private_cards, board_cards):
        actions = state.get_possible_actions()
        best_action = None
        max_value = float('-inf')

        # Avalia cada ação possível usando o Expectimax
        for action in actions:
            value = self.expectimax(state, action, private_cards, board_cards, depth=2)  # Definindo profundidade de pesquisa
            if value > max_value:
                max_value = value
                best_action = action

        return best_action

    def expectimax(self, state, action, private_cards, board_cards, depth):
        if depth == 0 or state.is_finished():
            return self.evaluate(state, private_cards, board_cards)

        # Simula o efeito da ação
        simulated_state = state.clone()
        simulated_state.update(action)

        if state.get_acting_player() == 0:  # Supõe-se que o índice 0 seja este bot
            max_value = float('-inf')
            for next_action in simulated_state.get_possible_actions():
                value = self.expectimax(simulated_state, next_action, private_cards, board_cards, depth - 1)
                max_value = max(max_value, value)
            return max_value
        else:
            # Supõe-se um ambiente de adversário
            values = []
            for next_action in simulated_state.get_possible_actions():
                value = self.expectimax(simulated_state, next_action, private_cards, board_cards, depth - 1)
                values.append(value)
            return sum(values) / len(values) if values else 0

    def evaluate(self, state, private_cards, board_cards):
        if state.is_finished():
            if state.get_result(0) > 0:  # Supondo que 0 é o índice do bot
                return float('inf')  # Ganhou o jogo
            elif state.get_result(0) < 0:
                return float('-inf')  # Perdeu o jogo

        hand_strength = 0
        # Garantir que há cartas suficientes para avaliação
        if len(private_cards + board_cards) >= 5:
            hand_strength = self.calculate_hand_strength(private_cards, board_cards)

        # Calcular pot odds
        pot_odds = self.calculate_pot_odds(state)

        # Considerar a agressividade dos oponentes e as apostas feitas
        opponent_aggression = self.estimate_opponent_aggression(state)

        # Avaliação simplificada como uma combinação ponderada desses fatores
        return hand_strength * 0.5 + pot_odds * 0.3 + opponent_aggression * 0.2

    def event_my_action(self, action, new_state):
        pass

    def event_opponent_action(self, action, new_state):
        pass

    def event_new_game(self):
        pass

    def event_end_game(self, final_state: State):
        pass

    def event_result(self, pos: int, result: int):
        pass

    def event_new_round(self, round: Round):
        pass
