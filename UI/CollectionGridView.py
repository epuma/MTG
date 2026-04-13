"""
Collection overview grid window.

Shows all owned cards (quantity > 0) as image thumbnails in a scrollable
grid.  Thumbnails are loaded asynchronously from the Scryfall cache.
Click a card to highlight it in the main window.
"""
import platform
import threading
from tkinter import (
    Toplevel, Frame, Canvas, Scrollbar, Label, Entry, Button, StringVar,
)

from PIL import ImageTk

import scryfall

THUMB_W = 100
THUMB_H = 140
TILE_W  = 116
TILE_H  = 174
COLS    = 5


class CollectionGridView(Toplevel):
    def __init__(self, root, collection, mtg_object, on_card_select=None):
        super().__init__(root)
        self.title('Collection Overview')
        self.geometry(f'{TILE_W * COLS + 40}x550')
        self.resizable(True, True)

        self._collection    = collection
        self._mtg_object    = mtg_object
        self._on_card_select = on_card_select
        self._tk_images: dict = {}   # (card_name, set_code) -> PhotoImage (prevents GC)
        self._all_cards: list = []   # (edition, card_name, set_code, qty)

        self._build_ui()
        self._load_card_list()

    # ---------------------------------------------------------------- setup

    def _build_ui(self):
        # ── toolbar ───────────────────────────────────────────────────────
        toolbar = Frame(self)
        toolbar.pack(fill='x', padx=6, pady=4)

        Label(toolbar, text='Filter:').pack(side='left')
        self._filter_var = StringVar()
        self._filter_var.trace('w', lambda *_: self._apply_filter())
        Entry(toolbar, textvariable=self._filter_var, width=22).pack(side='left', padx=4)
        Button(toolbar, text='Clear',
               command=lambda: self._filter_var.set('')).pack(side='left')

        self._count_lbl = Label(toolbar, text='', fg='grey')
        self._count_lbl.pack(side='right', padx=6)

        # ── scrollable canvas ─────────────────────────────────────────────
        container = Frame(self)
        container.pack(fill='both', expand=True)

        self._canvas = Canvas(container, bg='#f0f0f0')
        sb = Scrollbar(container, command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=sb.set)

        sb.pack(side='right', fill='y')
        self._canvas.pack(side='left', fill='both', expand=True)

        self._grid_frame = Frame(self._canvas, bg='#f0f0f0')
        self._win_id = self._canvas.create_window(
            (0, 0), window=self._grid_frame, anchor='nw'
        )

        self._grid_frame.bind('<Configure>', self._on_frame_cfg)
        self._canvas.bind('<Configure>', self._on_canvas_cfg)
        self._canvas.bind('<Enter>',
                          lambda _: self._canvas.bind_all('<MouseWheel>', self._scroll))
        self._canvas.bind('<Leave>',
                          lambda _: self._canvas.unbind_all('<MouseWheel>'))

    def _on_frame_cfg(self, _):
        self._canvas.configure(scrollregion=self._canvas.bbox('all'))

    def _on_canvas_cfg(self, event):
        self._canvas.itemconfig(self._win_id, width=event.width)

    def _scroll(self, event):
        if platform.system() == 'Darwin':
            self._canvas.yview_scroll(-1 * event.delta, 'units')
        else:
            self._canvas.yview_scroll(int(-1 * event.delta / 120), 'units')

    # ---------------------------------------------------------------- data

    def _load_card_list(self):
        for edition_name, cards in self._collection.data.items():
            edition  = self._mtg_object.data.get(edition_name)
            set_code = getattr(edition, 'code', '') if edition else ''
            for card_name, info in cards.items():
                if info['quantity'] > 0:
                    self._all_cards.append(
                        (edition_name, card_name, set_code, info['quantity'])
                    )
        self._all_cards.sort(key=lambda x: (x[0], x[1]))
        self._apply_filter()

    def _apply_filter(self):
        query    = self._filter_var.get().lower()
        filtered = [
            c for c in self._all_cards
            if not query or query in c[1].lower() or query in c[0].lower()
        ]
        self._render_grid(filtered)
        self._count_lbl.config(text=f'{len(filtered)} card(s)')

    # ---------------------------------------------------------------- grid

    def _render_grid(self, cards: list):
        # Destroy existing tile widgets and release image references
        for w in self._grid_frame.winfo_children():
            w.destroy()
        self._tk_images.clear()

        placeholder = scryfall.make_placeholder(THUMB_W, THUMB_H, '')

        for idx, (edition_name, card_name, set_code, qty) in enumerate(cards):
            row, col = divmod(idx, COLS)
            tile = Frame(self._grid_frame, width=TILE_W, height=TILE_H,
                         bd=1, relief='solid', bg='white')
            tile.grid(row=row, column=col, padx=3, pady=3)
            tile.grid_propagate(False)

            # Image label — starts with placeholder
            ph_tk = ImageTk.PhotoImage(placeholder)
            img_lbl = Label(tile, image=ph_tk, bg='white')
            img_lbl.image = ph_tk          # prevent GC
            img_lbl.pack()

            # Card name (truncated) + quantity badge
            short_name = (card_name[:15] + '…') if len(card_name) > 16 else card_name
            Label(tile, text=short_name, font=('Helvetica', 7),
                  wraplength=TILE_W - 4, bg='white').pack()
            Label(tile, text=f'×{qty}', font=('Helvetica', 7, 'bold'),
                  fg='navy', bg='white').pack()

            # Click binding on tile and all children
            key = (edition_name, card_name)
            for widget in (tile, img_lbl):
                widget.bind('<Button-1>', lambda _e, k=key: self._select(*k))

            # Async thumbnail load
            threading.Thread(
                target=self._load_thumb,
                args=(img_lbl, card_name, set_code),
                daemon=True,
            ).start()

    # ---------------------------------------------------------------- async

    def _load_thumb(self, label: Label, card_name: str, set_code: str):
        img = scryfall.fetch_card_image(
            card_name, set_code, THUMB_W, THUMB_H, scryfall_size='small'
        )
        if img is not None:
            self.after(0, self._set_thumb, label, card_name, set_code, img)

    def _set_thumb(self, label: Label, card_name: str, set_code: str, pil_img):
        if not label.winfo_exists():
            return
        tk_img = ImageTk.PhotoImage(pil_img)
        self._tk_images[(card_name, set_code)] = tk_img   # prevent GC
        label.config(image=tk_img)
        label.image = tk_img

    # ---------------------------------------------------------------- select

    def _select(self, edition_name: str, card_name: str):
        if self._on_card_select:
            self._on_card_select(edition_name, card_name)
