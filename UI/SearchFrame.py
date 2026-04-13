from tkinter import Frame, StringVar, OptionMenu, Button, Entry, Label


class SearchFrame(Frame):
    """
    Edition/card selectors with a real-time text filter for card names.

    Layout:
      Row 0: [Edition dropdown]  [Card dropdown]  [Enter button]
      Row 1: [Filter label]      [Filter entry]   [Clear button]

    Public helpers for keyboard navigation (used by MTGApp):
      select_relative(delta)         — move ±1 within filtered card list
      select_edition_relative(delta) — move ±1 in edition list
      get_visible_cards()            — current filtered card list
    """

    def __init__(self, root):
        super().__init__(root)
        self.grid(row=0, column=0)

        self.mtg_object = root.mtg_object

        self.edition_options = sorted(self.mtg_object.data.keys())
        self.edition_variable = StringVar()
        self.card_variable    = StringVar()
        self._filter_var      = StringVar()

        self.edition_variable.trace('w', self._on_edition_changed)
        self._filter_var.trace('w', self._apply_filter)

        self.edition_option_menu = OptionMenu(self, self.edition_variable,
                                              *self.edition_options)
        self.card_option_menu = OptionMenu(self, self.card_variable, '')

        self.edition_variable.set(self.edition_options[0])

        self.edition_option_menu.grid(row=0, column=0, sticky='W')
        self.card_option_menu.grid(   row=0, column=1, sticky='W')
        Button(self, text='Enter', command=root.update_ui).grid(
            row=0, column=2, padx=(4, 0))

        Label(self, text='Filter:').grid(row=1, column=0, sticky='E', pady=(2, 0))
        Entry(self, textvariable=self._filter_var, width=24).grid(
            row=1, column=1, sticky='W', pady=(2, 0))
        Button(self, text='Clear', command=self._clear_filter).grid(
            row=1, column=2, padx=(4, 0), pady=(2, 0))

    # ---------------------------------------------------------------- public

    def get_visible_cards(self) -> list:
        """Cards currently shown in the dropdown (after filter is applied)."""
        query     = self._filter_var.get().lower()
        all_cards = self._all_cards()
        return [c for c in all_cards if query in c.lower()] if query else all_cards

    def select_relative(self, delta: int) -> bool:
        """Move card selection by delta within visible cards. Returns True if changed."""
        cards   = self.get_visible_cards()
        current = self.card_variable.get()
        try:
            idx = cards.index(current)
        except ValueError:
            idx = 0
        new_idx = max(0, min(len(cards) - 1, idx + delta))
        if new_idx != idx:
            self.card_variable.set(cards[new_idx])
            return True
        return False

    def select_edition_relative(self, delta: int) -> bool:
        """Move to the next/previous edition. Returns True if changed."""
        current = self.edition_variable.get()
        try:
            idx = self.edition_options.index(current)
        except ValueError:
            idx = 0
        new_idx = max(0, min(len(self.edition_options) - 1, idx + delta))
        if new_idx != idx:
            self.edition_variable.set(self.edition_options[new_idx])
            return True
        return False

    # ---------------------------------------------------------------- private

    def _all_cards(self) -> list:
        return sorted(self.mtg_object.data[self.edition_variable.get()].data.keys())

    def _rebuild_card_menu(self, cards: list):
        menu = self.card_option_menu['menu']
        menu.delete(0, 'end')
        for card in cards:
            menu.add_command(label=card,
                             command=lambda c=card: self.card_variable.set(c))
        self.card_variable.set(cards[0] if cards else '')

    def _on_edition_changed(self, *_):
        self._filter_var.set('')
        self._rebuild_card_menu(self._all_cards())

    def _apply_filter(self, *_):
        query    = self._filter_var.get().lower()
        filtered = [c for c in self._all_cards() if query in c.lower()] if query \
                   else self._all_cards()
        self._rebuild_card_menu(filtered)

    def _clear_filter(self):
        self._filter_var.set('')
