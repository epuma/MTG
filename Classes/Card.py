from .lib import clean_unicode


class Card:
    """Represents a single Magic card, built from an MTGJson card dict."""

    def __init__(self, data):
        self.attrlist = []

        # Initialise every known attribute to None so callers can test
        # `card.foo is not None` without risking AttributeError.
        self.name = None
        self.manaCost = None
        self.cmc = None
        self.colors = None
        self.type = None
        self.supertypes = None
        self.types = None
        self.subtypes = None
        self.rarity = None
        self.text = None
        self.flavor = None
        self.artist = None
        self.number = None
        self.power = None
        self.toughness = None
        self.layout = None
        self.multiverseid = None
        self.imageName = None
        self.names = None
        self.loyalty = None
        self.variations = None
        self.watermark = None
        self.border = None
        self.timeshifted = None
        self.hand = None
        self.life = None
        self.reserved = None
        self.rulings = None
        self.foreignNames = None
        self.printings = None
        self.originalText = None
        self.originalType = None
        self.legalities = None

        for k, v in data.items():
            setattr(self, k, clean_unicode(v))
            self.attrlist.append(k)

    def __str__(self):
        lines = [f"{attr}: {getattr(self, attr)}" for attr in self.attrlist]
        return '\n'.join(lines)
