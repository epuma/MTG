import json

from .Card import Card
from .Edition import Edition
from .lib import clean_unicode


class Magic:
    """
    Loads the MTGJson database and exposes it as a dict of Edition objects
    keyed by full set name.

    Handles both MTGJson v2 (bare dict) and v5 (wrapped in {"data": ...}).
    """

    def __init__(self, json_file):
        with open(json_file, encoding='utf-8') as fh:
            raw = json.load(fh)

        # MTGJson v5 wraps everything in {"data": {...}, "meta": {...}}
        json_data = raw.get('data', raw)

        flat_list = []
        flat_cards = {}
        self.data = {}

        for _code, set_obj in json_data.items():
            edition_name = clean_unicode(set_obj['name'])
            edition = Edition(set_obj)
            self.data[edition_name] = edition
            for card_data in set_obj.get('cards', []):
                name = clean_unicode(card_data['name'])
                flat_list.append(name)
                flat_cards[name] = Card(card_data)

        self.flatList = sorted(set(flat_list))
        self.flatCards = flat_cards

    def __str__(self):
        editions = {
            clean_unicode(v.name): getattr(v, 'releaseDate', '')
            for v in self.data.values()
        }
        lines = [
            f"{name}  {date}"
            for name, date in sorted(editions.items(), key=lambda x: x[1])
        ]
        return '\n'.join(lines)

    def findCard(self, name):
        return self.flatCards.get(name)
