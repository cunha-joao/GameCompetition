from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.round import Round
from games.hlpoker.state import HLPokerState
from games.hlpoker.action import HLPokerAction
from games.state import State
from collections import Counter

class ExpectimaxHLPokerPlayer(HLPokerPlayer):
    def __init__(self, name):
        super().__init__(name)

    def get_action_with_cards(self, state: HLPokerState, private_cards, board_cards):
        best_action = self.expectimax(state, private_cards, board_cards, depth=3)
        return best_action

    def expectimax(self, state: HLPokerState, private_cards, board_cards, depth):
        if depth == 0 or state.is_finished():
            return self.evaluate(state, private_cards, board_cards)

        if state.get_acting_player() == self:  # Max node
            best_value = -float('inf')
            best_action = None
            for action in state.get_possible_actions():
                new_state = state.clone()
                # Simulate the update process by applying the action to the cloned state
                new_state = self.apply_action(new_state, action)
                value = self.expectimax(new_state, private_cards, board_cards, depth - 1)
                if value > best_value:
                    best_value = value
                    best_action = action
            return best_action if depth == 3 else best_value

        else:  # Expectation node
            total_value = 0
            actions = state.get_possible_actions()
            for action in actions:
                new_state = state.clone()
                # Simulate the update process by applying the action to the cloned state
                new_state = self.apply_action(new_state, action)
                prob = 1 / len(actions)
                total_value += prob * self.expectimax(new_state, private_cards, board_cards, depth - 1)
            return total_value

    def evaluate(self, state: HLPokerState, private_cards, board_cards):
        return self.hand_strength(private_cards, board_cards)

    def hand_strength(self, private_cards, board_cards):
        all_cards = private_cards + board_cards
        ranks = [card.rank for card in all_cards]
        suits = [card.suit for card in all_cards]
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)

        if max(rank_counts.values()) == 4:
            return 7  # Four of a kind
        elif sorted(rank_counts.values()) == [2, 3]:
            return 6  # Full house
        elif len(set(suits)) == 1:
            return 5  # Flush
        elif len(set(ranks)) == 5 and max(ranks) - min(ranks) == 4:
            return 4  # Straight
        elif max(rank_counts.values()) == 3:
            return 3  # Three of a kind
        elif sorted(rank_counts.values()) == [1, 2, 2]:
            return 2  # Two pair
        elif max(rank_counts.values()) == 2:
            return 1  # One pair
        else:
            return 0  # High card

    def apply_action(self, state: HLPokerState, action):
        new_state = state.clone()

        if action == HLPokerAction.FOLD:
            new_state.update(action)
            return new_state

        elif action == HLPokerAction.CALL:
            new_state.update(action)
            return new_state

        elif action == HLPokerAction.RAISE:
            new_state.update(action)
            return new_state

        if new_state.get_current_round() == Round.Showdown:
            return new_state

        return new_state

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