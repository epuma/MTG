import threading
from tkinter import Frame, Label, E, W

import scryfall


class PriceFrame(Frame):
    """
    Shows Market / Foil / MTGO prices fetched asynchronously from Scryfall.

    update_prices() — async fetch; fires on_complete when done.
    set_prices_direct() — display pre-fetched prices immediately (no API call).
    """

    def __init__(self, root):
        super().__init__(root)
        self.grid(row=1, column=0, padx=10, pady=(0, 5), sticky='N')
        self.columnconfigure(1, weight=1, minsize=70)

        self.prices = ['N/A', 'N/A', 'N/A']

        Label(self, text='Market (USD)').grid(row=0, column=0, sticky=W, padx=(0, 8))
        Label(self, text='Foil (USD)').grid(  row=1, column=0, sticky=W, padx=(0, 8))
        Label(self, text='MTGO (TIX)').grid(  row=2, column=0, sticky=W, padx=(0, 8))

        self._market = Label(self, text='N/A')
        self._foil   = Label(self, text='N/A')
        self._mtgo   = Label(self, text='N/A')

        self._market.grid(row=0, column=1, sticky=E)
        self._foil.grid(  row=1, column=1, sticky=E)
        self._mtgo.grid(  row=2, column=1, sticky=E)

    # ---------------------------------------------------------------- public

    def update_prices(self, card_obj, _edition, on_complete=None):
        """Kick off a background price fetch for card_obj."""
        card_name = _split_card_name(card_obj)
        self._set_labels(['…', '…', '…'])
        self.prices = ['N/A', 'N/A', 'N/A']

        threading.Thread(
            target=self._worker,
            args=(card_name, on_complete),
            daemon=True,
        ).start()

    def set_prices_direct(self, prices: list, cached: bool = False):
        """Display a pre-fetched price list without making any API call.
        Pass cached=True to append ' *' to each value (offline fallback)."""
        self.prices = prices
        self._set_labels(prices, cached=cached)

    # ---------------------------------------------------------------- private

    def _worker(self, card_name: str, on_complete):
        prices = scryfall.get_card_prices(card_name)
        self.after(0, self._apply_prices, prices, on_complete)

    def _apply_prices(self, prices: list, on_complete):
        self.prices = prices
        self._set_labels(prices)
        if on_complete:
            on_complete(prices)

    def _set_labels(self, prices: list, cached: bool = False):
        tag = ' *' if cached else ''
        market, foil, mtgo = prices
        self._market.config(
            text=f'${market}{tag}' if market not in ('N/A', '…') else market)
        self._foil.config(
            text=f'${foil}{tag}'   if foil   not in ('N/A', '…') else foil)
        self._mtgo.config(
            text=f'{mtgo}{tag}'    if mtgo   not in ('N/A', '…') else mtgo)


def _split_card_name(card_obj) -> str:
    if card_obj.layout == 'split' and card_obj.names:
        return ' // '.join(card_obj.names)
    return card_obj.name
