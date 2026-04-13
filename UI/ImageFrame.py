import threading
from tkinter import Frame, Label, CENTER, RIDGE

from PIL import ImageTk

import scryfall


class ImageFrame(Frame):
    """Displays the card artwork, fetched asynchronously from Scryfall."""

    PREFETCH_COUNT = 2   # number of adjacent cards to prefetch after selection

    def __init__(self, root):
        super().__init__(root)
        self.img_wt     = root.img_wt
        self.img_ht     = root.img_ht
        self.mtg_object = root.mtg_object
        self.configure(
            width=self.img_wt + 10, height=self.img_ht + 10,
            bd=10, relief=RIDGE,
        )
        self.grid(row=2, column=0, padx=10, pady=10, sticky='N')

        self._tk_image = None       # kept to prevent GC
        placeholder    = scryfall.make_placeholder(self.img_wt, self.img_ht)
        self._ph_tk    = ImageTk.PhotoImage(placeholder)

        self.card_image = Label(self, image=self._ph_tk)
        self.card_image.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Load default card
        default_edition = 'Limited Edition Alpha'
        set_code = self._set_code(default_edition)
        self._fetch_async('Black Lotus', set_code)

    # ---------------------------------------------------------------- public

    def update_image(self, card_obj, edition: str):
        """Start async fetch for the selected card (from local DB)."""
        self._show_loading()
        set_code = self._set_code(edition)
        self._fetch_async(card_obj.name, set_code)
        self._prefetch_adjacent(card_obj.name, edition, set_code)

    def update_image_from_code(self, card_name: str, set_code: str):
        """Start async fetch using an explicit Scryfall set code (e.g. from search)."""
        self._show_loading()
        self._fetch_async(card_name, set_code)

    # ---------------------------------------------------------------- private

    def _set_code(self, edition_name: str) -> str:
        edition = self.mtg_object.data.get(edition_name)
        return getattr(edition, 'code', '') if edition else ''

    def _show_loading(self):
        self._tk_image = None
        self.card_image.config(image=self._ph_tk)

    def _fetch_async(self, card_name: str, set_code: str):
        threading.Thread(
            target=self._worker,
            args=(card_name, set_code),
            daemon=True,
        ).start()

    def _worker(self, card_name: str, set_code: str):
        pil_image = scryfall.fetch_card_image(card_name, set_code,
                                              self.img_wt, self.img_ht)
        self.after(0, self._apply_image, pil_image)

    def _apply_image(self, pil_image):
        if pil_image is None:
            placeholder = scryfall.make_placeholder(self.img_wt, self.img_ht, 'Not Found')
            self._tk_image = ImageTk.PhotoImage(placeholder)
        else:
            self._tk_image = ImageTk.PhotoImage(pil_image)
        self.card_image.config(image=self._tk_image)

    def _prefetch_adjacent(self, card_name: str, edition: str, set_code: str):
        """Queue background downloads for the next few cards."""
        edition_obj = self.mtg_object.data.get(edition)
        if not edition_obj:
            return
        cards = sorted(edition_obj.data.keys())
        try:
            idx = cards.index(card_name)
        except ValueError:
            return
        for delta in range(1, self.PREFETCH_COUNT + 1):
            next_idx = idx + delta
            if next_idx < len(cards):
                scryfall.prefetch_image(cards[next_idx], set_code,
                                        self.img_wt, self.img_ht)
