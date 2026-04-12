import threading
from tkinter import Frame, Label, E, W

import scryfall


class PriceFrame(Frame):
    """
    Shows Market / Foil / MTGO prices fetched asynchronously from Scryfall.

    update_prices() accepts an optional on_complete callback that is invoked
    on the main thread once the price list is ready — used by MTGApp to
    save the price to the open collection without blocking the UI.
    """

    def __init__(self, root):
        super().__init__(root)
        self.grid(row=1, column=0)

        self.prices = ['N/A', 'N/A', 'N/A']

        Label(self, text='Market (USD)').grid(row=0, column=0, sticky=W)
        Label(self, text='Foil (USD)').grid(row=1, column=0, sticky=W)
        Label(self, text='MTGO (TIX)').grid(row=2, column=0, sticky=W)

        self._market = Label(self, text='N/A')
        self._foil   = Label(self, text='N/A')
        self._mtgo   = Label(self, text='N/A')

        self._market.grid(row=0, column=1, sticky=E)
        self._foil.grid(row=1, column=1, sticky=E)
        self._mtgo.grid(row=2, column=1, sticky=E)

    # ---------------------------------------------------------------- public

    def update_prices(self, card_obj, _edition, on_complete=None):
        """Kick off a background price fetch for card_obj."""
        card_name = _split_card_name(card_obj)
        # Reset to loading state immediately
        self._set_labels(['...', '...', '...'])
        self.prices = ['N/A', 'N/A', 'N/A']

        t = threading.Thread(
            target=self._worker,
            args=(card_name, on_complete),
            daemon=True,
        )
        t.start()

    # -------------------------------------------------------------- private

    def _worker(self, card_name, on_complete):
        prices = scryfall.get_card_prices(card_name)
        self.after(0, self._apply_prices, prices, on_complete)

    def _apply_prices(self, prices, on_complete):
        self.prices = prices
        self._set_labels(prices)
        if on_complete:
            on_complete(prices)

    def _set_labels(self, prices):
        market, foil, mtgo = prices
        self._market.config(text=f'${market}' if market != 'N/A' and market != '...' else market)
        self._foil.config(  text=f'${foil}'   if foil   != 'N/A' and foil   != '...' else foil)
        self._mtgo.config(  text=mtgo)


def _split_card_name(card_obj):
    """Return the canonical display name, joining split-card halves with //."""
    if card_obj.layout == 'split' and card_obj.names:
        return ' // '.join(card_obj.names)
    return card_obj.name
