import platform
from tkinter import Frame, Canvas, Scrollbar, Label, NW, W, N, S, TclError


class ScrollFrame(Frame):
    """Scrollable panel that shows detailed attributes for the selected card."""

    # Pairs of (attribute name on Card, display label)
    CARD_FIELDS = [
        ('name',         'Name'),
        ('manaCost',     'Casting Cost'),
        ('type',         'Type'),
        ('rarity',       'Rarity'),
        ('text',         'Text'),
        ('flavor',       'Flavor Text'),
        ('power',        'Power'),
        ('toughness',    'Toughness'),
        ('loyalty',      'Loyalty'),
        ('printings',    'Set Printings'),
        ('artist',       'Artist'),
        ('number',       'Card Number'),
        ('multiverseid', 'Multiverse ID'),
        ('border',       'Border'),
        ('timeshifted',  'Timeshifted'),
        ('hand',         'Max Hand Modifier'),
        ('life',         'Max Life Modifier'),
        ('rulings',      'Rulings'),
        ('legalities',   'Legalities'),
        ('originalText', 'Original Text'),
        ('originalType', 'Original Type'),
    ]

    def __init__(self, root):
        super().__init__(root)
        self.img_wt = root.img_wt
        self.img_ht = root.img_ht
        self.configure(width=self.img_wt, height=self.img_ht)
        self.grid(row=2, column=1, padx=10, pady=10, sticky=N)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvas = Canvas(self)
        self.info_frame = Frame(self.canvas)
        self.scrollbar = _AutoScrollbar(self)
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.grid(row=0, column=1, sticky=N + S)
        self.canvas.grid(row=0, column=0, sticky='NSEW')
        self.canvas.create_window((0, 0), window=self.info_frame, anchor='nw')

        self.info_frame.bind('<Configure>', self._on_frame_configure)
        self.canvas.bind('<Enter>', self._bind_mousewheel)
        self.canvas.bind('<Leave>', self._unbind_mousewheel)

        # Build static label widgets once; show/hide them on each update
        self._key_labels = []
        self._val_labels = []
        for _attr, display in self.CARD_FIELDS:
            self._key_labels.append(Label(self.info_frame, text=f'{display}:'))
            self._val_labels.append(
                Label(self.info_frame, wraplength=350, justify='left')
            )

        # Show the default card on startup
        default_edition = 'Limited Edition Alpha'
        default_card = 'Black Lotus'
        card_obj = root.mtg_object.data[default_edition].data[default_card]
        self.update_info(card_obj)

    # -------------------------------------------------------------- helpers

    def _on_frame_configure(self, _event):
        self.canvas.configure(
            scrollregion=self.canvas.bbox('all'),
            width=self.img_wt,
            height=self.img_ht,
        )

    def _bind_mousewheel(self, _event):
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)

    def _unbind_mousewheel(self, _event):
        self.canvas.unbind_all('<MouseWheel>')

    def _on_mousewheel(self, event):
        if platform.system() == 'Darwin':
            self.canvas.yview_scroll(-1 * event.delta, 'units')
        else:
            self.canvas.yview_scroll(int(-1 * event.delta / 120), 'units')

    # -------------------------------------------------------------- public

    def update_info(self, card_obj):
        row = 0
        for n, (attr, _display) in enumerate(self.CARD_FIELDS):
            value = getattr(card_obj, attr, None)
            self._key_labels[n].grid_forget()
            self._val_labels[n].grid_forget()
            if value is not None:
                self._key_labels[n].grid(row=row, column=0, sticky=NW)
                self._val_labels[n].config(text=str(value))
                self._val_labels[n].grid(row=row, column=1, sticky=W)
                row += 1


class _AutoScrollbar(Scrollbar):
    """A scrollbar that hides itself when not needed (grid geometry only)."""

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call('grid', 'remove', self)
        else:
            self.grid()
        super().set(lo, hi)

    def pack(self, **kw):
        raise TclError('cannot use pack with this widget')

    def place(self, **kw):
        raise TclError('cannot use place with this widget')
