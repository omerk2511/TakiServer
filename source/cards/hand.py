HAND_INITIAL_SIZE = 8


class Hand(object):
    def __init__(self, cards):
        self.cards = cards

    def append_cards(self, cards):
        self.cards.extend(cards)

    def remove_card(self, card):
        self.cards.remove(card)

    def card_exists(self, card, count=1):
        return self.cards.count(card) >= count

    def empty(self):
        return len(self.cards) == 0
