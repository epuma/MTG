from tkinter import Frame, Label, RIDGE, W, E


class StatsFrame(Frame):
    """
    Footer bar showing collection-wide statistics:
      Total cards owned  |  Unique cards  |  Est. value (market USD)

    Call update_stats(collection) whenever the collection changes.
    """

    def __init__(self, root):
        super().__init__(root, bd=1, relief=RIDGE, padx=8, pady=4)
        self.grid(row=3, column=0, columnspan=3, sticky='EW', padx=10, pady=(0, 6))

        # Three evenly-spaced stat blocks
        self._make_stat(0, 'Total Cards')
        self._make_stat(1, 'Unique Cards')
        self._make_stat(2, 'Est. Value (Market)')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self._show_empty()

    # ---------------------------------------------------------------- private

    def _make_stat(self, col, title):
        """Create a label pair (title + value) in the given column."""
        inner = Frame(self)
        inner.grid(row=0, column=col, padx=20)
        Label(inner, text=title, font=('Helvetica', 9)).grid(row=0, column=0)
        value_label = Label(inner, text='—', font=('Helvetica', 11, 'bold'))
        value_label.grid(row=1, column=0)
        # Store a reference so update_stats can reach it
        setattr(self, f'_val_{col}', value_label)

    def _set(self, col, text):
        getattr(self, f'_val_{col}').config(text=text)

    def _show_empty(self):
        self._set(0, '—')
        self._set(1, '—')
        self._set(2, '—')

    # ---------------------------------------------------------------- public

    def update_stats(self, collection):
        """Refresh the stats from the given Collection object."""
        if collection.data is None:
            self._show_empty()
            return

        total_qty    = collection.getTotalQuantity()
        unique_owned = collection.getUniqueOwned()
        prices       = collection.getTotalPrice()
        market_value = prices[0]

        self._set(0, f'{total_qty:,}')
        self._set(1, f'{unique_owned:,}')
        self._set(2, f'${market_value:,.2f}')
