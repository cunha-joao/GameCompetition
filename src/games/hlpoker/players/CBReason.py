from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.round import Round
from games.hlpoker.state import HLPokerState
from games.hlpoker.action import HLPokerAction
from games.state import State
from random import choice
import pickle
import os

class CBReasonHLPokerPlayer(HLPokerPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.case_base = []
        self.load_cases()

    def load_cases(self):
        if os.path.exists('case_base.pkl'):
            with open('case_base.pkl', 'rb') as file:
                self.case_base = pickle.load(file)

    def save_cases(self):
        with open('case_base.pkl', 'wb') as file:
            pickle.dump(self.case_base, file)

    def get_action_with_cards(self, state: HLPokerState, private_cards, board_cards):
        # Recuperar o caso mais similar
        similar_case = self.retrieve(state, private_cards, board_cards)

        if similar_case:
            action = self.adapt_action(similar_case, state)
            if state.validate_action(action):
                return action

        # Se nenhum caso similar encontrado ou ação inválida, escolher aleatoriamente
        return choice(state.get_possible_actions())

    def retrieve(self, state: HLPokerState, private_cards, board_cards):
        # Implementação de recuperação usando uma métrica de similaridade
        best_case = None
        highest_similarity = -1
        for case in self.case_base:
            similarity = self.calculate_similarity(case, state, private_cards, board_cards)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_case = case
        return best_case

    def calculate_similarity(self, case, state: HLPokerState, private_cards, board_cards):
        # Calcular similaridade com base nas cartas privadas e comunitárias, rodada, sequência de ações e força da mão
        similarity = 0
        if case['round'] == state.get_current_round():
            similarity += 1
        similarity += len(set(case['private_cards']) & set(private_cards))
        similarity += len(set(case['board_cards']) & set(board_cards))
        similarity += self.sequence_similarity(case['sequence'], state.get_sequence())
        similarity += self.hand_strength_similarity(case['private_cards'], private_cards)
        return similarity

    def sequence_similarity(self, seq1, seq2):
        # Similaridade baseada na sequência de ações
        matches = 0
        length = min(len(seq1), len(seq2))
        for i in range(length):
            if seq1[i] == seq2[i]:
                matches += 1
        return matches / max(len(seq1), len(seq2), 1)

    def hand_strength_similarity(self, hand1, hand2):
        # Similaridade baseada na força da mão
        strength1 = self.hand_strength(hand1)
        strength2 = self.hand_strength(hand2)
        return 1 - abs(strength1 - strength2)

    def hand_strength(self, cards):
        # Calcular a força da mão usando uma heurística simples
        if not cards:
            return 0
        return sum(card.rank for card in cards) / len(cards)

    def adapt_action(self, case, state: HLPokerState):
        # Adaptar a ação do caso similar encontrado
        action = case['action']
        if state.get_current_round() != case['round']:
            # Exemplo de adaptação: ajustar a ação se a rodada atual for diferente
            if action == HLPokerAction.RAISE and state.get_current_round() == Round.Preflop:
                return HLPokerAction.CALL
        return action

    def retain(self, state: HLPokerState, action, private_cards, board_cards):
        # Verificar se o caso já existe na base de casos
        for case in self.case_base:
            if (case['round'] == state.get_current_round() and
                case['private_cards'] == private_cards and
                case['board_cards'] == board_cards and
                case['sequence'] == state.get_sequence() and
                case['action'] == action):
                return  # Não armazenar casos duplicados

        # Armazenar o novo caso na base de casos
        case = {
            'round': state.get_current_round(),
            'private_cards': private_cards,
            'board_cards': board_cards,
            'sequence': state.get_sequence(),
            'action': action,
            'result': state.get_result(self.name)
        }
        self.case_base.append(case)
        self.save_cases()

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
