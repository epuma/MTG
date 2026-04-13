import csv
import datetime
import json


class Collection:
    """
    Manages a user's card collection stored as a JSON file.

    Structure:
        {
            "<Edition name>": {
                "<Card name>": {
                    "quantity":  int,
                    "price":     [usd, usd_foil, tix],
                    "last_date": str,
                    "notes":     str
                }
            }
        }
    """

    def __init__(self):
        self.data = None

    # ------------------------------------------------------------------ I/O

    def load(self, file_name):
        with open(file_name, encoding='utf-8') as fh:
            self.data = json.load(fh)

    def save(self, file_name):
        with open(file_name, 'w', encoding='utf-8') as fh:
            json.dump(self.data, fh)

    def save_close(self, file_name):
        self.save(file_name)
        self.data = None

    def export_csv(self, file_name):
        """
        Export all owned cards (quantity > 0) to a CSV file.
        Columns: Edition, Card, Quantity, Market (USD), Foil (USD),
                 MTGO (TIX), Last Updated, Notes.
        """
        with open(file_name, 'w', newline='', encoding='utf-8') as fh:
            writer = csv.writer(fh)
            writer.writerow([
                'Edition', 'Card', 'Quantity',
                'Market (USD)', 'Foil (USD)', 'MTGO (TIX)',
                'Last Updated', 'Notes',
            ])
            for edition_name, cards in sorted(self.data.items()):
                for card_name, info in sorted(cards.items()):
                    if info['quantity'] > 0:
                        writer.writerow([
                            edition_name,
                            card_name,
                            info['quantity'],
                            info['price'][0],
                            info['price'][1],
                            info['price'][2],
                            info['last_date'],
                            info['notes'],
                        ])

    # ----------------------------------------------------------- Construction

    def newCollection(self, magic_obj, file_name='untitledCollection.json'):
        """Build a fresh collection skeleton from a Magic database object."""
        b = {}
        for edition_name, edition in magic_obj.data.items():
            b[edition_name] = {
                card_name: {'quantity': 0, 'price': ['N/A', 'N/A', 'N/A'],
                             'last_date': '', 'notes': ''}
                for card_name in edition.data
            }
        with open(file_name, 'w', encoding='utf-8') as fh:
            json.dump(b, fh)

    def updateCollection(self, magic_obj):
        """Add any sets/cards present in the database but missing from this collection."""
        for edition_name, edition in magic_obj.data.items():
            if edition_name not in self.data:
                self.data[edition_name] = {}
            for card_name in edition.data:
                if card_name not in self.data[edition_name]:
                    self.data[edition_name][card_name] = {
                        'quantity': 0,
                        'price': ['N/A', 'N/A', 'N/A'],
                        'last_date': '',
                        'notes': '',
                    }
        print('Collection updated.')

    # ------------------------------------------------------------ Accessors

    def getQuantity(self, edition, card):
        return self.data[edition][card]['quantity']

    def getPrice(self, edition, card):
        return self.data[edition][card]['price']

    def getDateUpdated(self, edition, card):
        return self.data[edition][card]['last_date']

    def getNotes(self, edition, card):
        return self.data[edition][card]['notes']

    # ------------------------------------------------------------ Mutators

    def updateQuantity(self, edition, card, quantity):
        self.data[edition][card]['quantity'] = quantity

    def updatePrice(self, edition, card, price):
        self.data[edition][card]['price'] = price
        self.data[edition][card]['last_date'] = (
            datetime.datetime.now().strftime('%B %d, %Y %I:%M %p')
        )

    def updateNotes(self, edition, card, notes):
        self.data[edition][card]['notes'] = notes

    # ------------------------------------------------------------ Aggregates

    def getTotalQuantity(self):
        return sum(
            card['quantity']
            for edition in self.data.values()
            for card in edition.values()
        )

    def getUniqueOwned(self):
        """Number of distinct cards with quantity > 0."""
        return sum(
            1
            for edition in self.data.values()
            for card in edition.values()
            if card['quantity'] > 0
        )

    def getTotalPrice(self):
        total = [0.0, 0.0, 0.0]
        for edition in self.data.values():
            for card in edition.values():
                qty = card['quantity']
                for i in range(3):
                    p = card['price'][i]
                    if p != 'N/A':
                        total[i] += qty * float(p)
        return total

    def __str__(self):
        lines = []
        total = 0
        for edition_name, cards in self.data.items():
            lines.append(f'\n{edition_name}')
            for card_name, info in cards.items():
                lines.append(f"  {card_name}: {info['quantity']}")
                total += info['quantity']
        lines.append(f'\nTotal cards: {total}')
        return '\n'.join(lines)
