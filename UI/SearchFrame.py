from tkinter import Frame, StringVar, OptionMenu, Button, Entry, Label


class SearchFrame(Frame):
    """
    Edition/card selectors with real-time text filters for both.

    Layout:
      Row 0: [Edition dropdown]   [Card dropdown]    [Enter button]
      Row 1: [Filter label]       [Filter entry]     [Clear button]
      Row 2: [Set filter label]   [Set filter entry] [Clear button]

    Auto-load: selecting a card or edition from the dropdowns triggers
    update_ui() after a 300 ms debounce.  A _programmatic flag suppresses
    this during filter rebuilds and keyboard-nav calls (which call
    update_ui() directly).

    Public helpers for keyboard navigation (used by MTGApp):
      select_relative(delta)         — move ±1 within filtered card list
      select_edition_relative(delta) — move ±1 in edition list
      get_visible_cards()            — current filtered card list
    """

    def __init__(self, root):
        super().__init__(root)
        self.grid(row=0, column=0)

        self._root      = root
        self.mtg_object = root.mtg_object

        # _programmatic is True during any programmatic variable write so that
        # auto-load traces don't fire during filter rebuilds or keyboard nav.
        self._programmatic   = False
        self._auto_load_job  = None

        self._all_edition_options = sorted(self.mtg_object.data.keys())
        self.edition_options      = list(self._all_edition_options)

        self.edition_variable    = StringVar()
        self.card_variable       = StringVar()
        self._filter_var         = StringVar()
        self._edition_filter_var = StringVar()

        self.edition_variable.trace('w', self._on_edition_changed)
        self._filter_var.trace('w', self._apply_filter)
        self._edition_filter_var.trace('w', self._apply_edition_filter)
        self.card_variable.trace('w', self._on_card_changed)

        self.edition_option_menu = OptionMenu(self, self.edition_variable,
                                              *self.edition_options)
        self.card_option_menu    = OptionMenu(self, self.card_variable, '')

        self.edition_variable.set(self.edition_options[0])

        # Row 0: edition | card | Enter
        self.edition_option_menu.grid(row=0, column=0, sticky='W')
        self.card_option_menu.grid(   row=0, column=1, sticky='W')
        Button(self, text='Enter', command=root.update_ui).grid(
            row=0, column=2, padx=(4, 0))

        # Row 1: card name filter
        Label(self, text='Filter:').grid(row=1, column=0, sticky='E', pady=(2, 0))
        Entry(self, textvariable=self._filter_var, width=24).grid(
            row=1, column=1, sticky='W', pady=(2, 0))
        Button(self, text='Clear', command=self._clear_filter).grid(
            row=1, column=2, padx=(4, 0), pady=(2, 0))

        # Row 2: set / edition filter
        Label(self, text='Set filter:').grid(row=2, column=0, sticky='E', pady=(2, 0))
        Entry(self, textvariable=self._edition_filter_var, width=24).grid(
            row=2, column=1, sticky='W', pady=(2, 0))
        Button(self, text='Clear', command=self._clear_edition_filter).grid(
            row=2, column=2, padx=(4, 0), pady=(2, 0))

    # ---------------------------------------------------------------- public

    def get_visible_cards(self) -> list:
        """Cards currently shown in the dropdown (after filter is applied)."""
        query     = self._filter_var.get().lower()
        all_cards = self._all_cards()
        return [c for c in all_cards if query in c.lower()] if query else all_cards

    def select_relative(self, delta: int) -> bool:
        """Move card selection by delta within visible cards.
        Suppresses auto-load (caller calls update_ui directly)."""
        cards   = self.get_visible_cards()
        current = self.card_variable.get()
        try:
            idx = cards.index(current)
        except ValueError:
            idx = 0
        new_idx = max(0, min(len(cards) - 1, idx + delta))
        if new_idx != idx:
            prev = self._programmatic
            self._programmatic = True
            try:
                self.card_variable.set(cards[new_idx])
            finally:
                self._programmatic = prev
            return True
        return False

    def select_edition_relative(self, delta: int) -> bool:
        """Move to the next/previous edition.
        Suppresses auto-load (caller calls update_ui directly)."""
        current = self.edition_variable.get()
        try:
            idx = self.edition_options.index(current)
        except ValueError:
            idx = 0
        new_idx = max(0, min(len(self.edition_options) - 1, idx + delta))
        if new_idx != idx:
            prev = self._programmatic
            self._programmatic = True
            try:
                self.edition_variable.set(self.edition_options[new_idx])
            finally:
                self._programmatic = prev
            return True
        return False

    # ---------------------------------------------------------------- private

    def _all_cards(self) -> list:
        edition = self.edition_variable.get()
        if edition not in self.mtg_object.data:
            return []
        return sorted(self.mtg_object.data[edition].data.keys())

    def _rebuild_card_menu(self, cards: list):
        """Rebuild the card OptionMenu. Sets _programmatic for the duration."""
        prev = self._programmatic
        self._programmatic = True
        try:
            menu = self.card_option_menu['menu']
            menu.delete(0, 'end')
            for card in cards:
                menu.add_command(label=card,
                                 command=lambda c=card: self.card_variable.set(c))
            self.card_variable.set(cards[0] if cards else '')
        finally:
            self._programmatic = prev

    def _rebuild_edition_menu(self, editions: list):
        """Rebuild the edition OptionMenu and refresh the card menu."""
        prev = self._programmatic
        self._programmatic = True
        try:
            menu = self.edition_option_menu['menu']
            menu.delete(0, 'end')
            self.edition_options = editions
            for ed in editions:
                menu.add_command(label=ed,
                                 command=lambda e=ed: self.edition_variable.set(e))
            if editions and self.edition_variable.get() not in editions:
                self.edition_variable.set(editions[0])
            self._rebuild_card_menu(self._all_cards())
        finally:
            self._programmatic = prev

    def _on_edition_changed(self, *_):
        if self._programmatic:
            return
        # Clear card filter; _apply_filter trace rebuilds the card menu
        self._filter_var.set('')
        self._schedule_auto_load()

    def _apply_filter(self, *_):
        query    = self._filter_var.get().lower()
        filtered = [c for c in self._all_cards() if query in c.lower()] if query \
                   else self._all_cards()
        self._rebuild_card_menu(filtered)

    def _apply_edition_filter(self, *_):
        query    = self._edition_filter_var.get().lower()
        filtered = [e for e in self._all_edition_options if query in e.lower()] if query \
                   else list(self._all_edition_options)
        self._rebuild_edition_menu(filtered)

    def _on_card_changed(self, *_):
        if self._programmatic:
            return
        self._schedule_auto_load()

    def _schedule_auto_load(self):
        """Debounce: cancel any pending auto-load, schedule a new one."""
        if self._auto_load_job is not None:
            self.after_cancel(self._auto_load_job)
        self._auto_load_job = self.after(300, self._do_auto_load)

    def _do_auto_load(self):
        self._auto_load_job = None
        self._root.update_ui()

    def _clear_filter(self):
        self._filter_var.set('')

    def _clear_edition_filter(self):
        self._edition_filter_var.set('')
