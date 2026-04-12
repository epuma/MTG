from .Card import Card
from .lib import clean_unicode


class Edition:
    """Represents one MTG set/edition with all its cards."""

    def __init__(self, data):
        self.data = {}
        for k, v in data.items():
            if k != 'cards':
                setattr(self, k, v)
        for card_data in data.get('cards', []):
            card = Card(card_data)
            self.data[clean_unicode(card_data['name'])] = card

    def getCard(self, name):
        return self.data[name]
