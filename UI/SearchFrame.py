from tkinter import Frame, StringVar, OptionMenu, Button, Entry, Label


class SearchFrame(Frame):
    """
    Edition/card selectors with a real-time text filter for card names.

    Layout:
      Row 0: [Edition dropdown]  [Card dropdown]  [Enter button]
      Row 1: [Filter label]      [Filter entry]   [Clear button]
    """

    def __init__(self, root):
        super().__init__(root)
        self.grid(row=0, column=0)

        self.mtg_object = root.mtg_object

        self.edition_options = sorted(self.mtg_object.data.keys())
        self.edition_variable = StringVar()
        self.card_variable    = StringVar()
        self._filter_var      = StringVar()

        # Watch for edition changes and filter-text changes
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

        # Filter row
        Label(self, text='Filter:').grid(row=1, column=0, sticky='E', pady=(2, 0))
        Entry(self, textvariable=self._filter_var, width=24).grid(
            row=1, column=1, sticky='W', pady=(2, 0))
        Button(self, text='Clear', command=self._clear_filter).grid(
            row=1, column=2, padx=(4, 0), pady=(2, 0))

    # ---------------------------------------------------------------- private

    def _current_cards(self):
        """All card names for the selected edition, sorted."""
        return sorted(self.mtg_object.data[self.edition_variable.get()].data.keys())

    def _rebuild_card_menu(self, cards):
        """Replace card dropdown contents with the given list."""
        menu = self.card_option_menu['menu']
        menu.delete(0, 'end')
        for card in cards:
            menu.add_command(label=card,
                             command=lambda c=card: self.card_variable.set(c))
        self.card_variable.set(cards[0] if cards else '')

    def _on_edition_changed(self, *_):
        self._filter_var.set('')          # Clear filter when edition changes
        self._rebuild_card_menu(self._current_cards())

    def _apply_filter(self, *_):
        query = self._filter_var.get().lower()
        all_cards = self._current_cards()
        filtered = [c for c in all_cards if query in c.lower()] if query else all_cards
        self._rebuild_card_menu(filtered)

    def _clear_filter(self):
        self._filter_var.set('')
