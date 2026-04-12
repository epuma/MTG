import threading
from tkinter import Frame, Label, CENTER, RIDGE
from PIL import ImageTk

import scryfall


class ImageFrame(Frame):
    """Displays the card artwork, fetched asynchronously from Scryfall."""

    def __init__(self, root):
        super().__init__(root)
        self.img_wt = root.img_wt
        self.img_ht = root.img_ht
        self.mtg_object = root.mtg_object
        self.configure(
            width=self.img_wt + 10,
            height=self.img_ht + 10,
            bd=10,
            relief=RIDGE,
        )
        self.grid(row=2, column=0, padx=10, pady=10, sticky='N')

        self._tk_image = None  # keep a reference to prevent GC
        self.card_image = Label(self, text='Loading...')
        self.card_image.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Load the default card in the background
        default_edition = 'Limited Edition Alpha'
        default_card = 'Black Lotus'
        set_code = self._set_code(default_edition)
        self._fetch_async(default_card, set_code)

    # ---------------------------------------------------------------- public

    def update_image(self, card_obj, edition):
        """Start an async fetch for card_obj's artwork."""
        self.card_image.config(image='', text='Loading...')
        self._tk_image = None
        set_code = self._set_code(edition)
        self._fetch_async(card_obj.name, set_code)

    # -------------------------------------------------------------- private

    def _set_code(self, edition_name):
        edition = self.mtg_object.data.get(edition_name)
        return getattr(edition, 'code', '') if edition else ''

    def _fetch_async(self, card_name, set_code):
        t = threading.Thread(
            target=self._worker,
            args=(card_name, set_code),
            daemon=True,
        )
        t.start()

    def _worker(self, card_name, set_code):
        pil_image = scryfall.fetch_card_image(
            card_name, set_code, self.img_wt, self.img_ht
        )
        # Schedule the UI update on the main thread
        self.after(0, self._apply_image, pil_image)

    def _apply_image(self, pil_image):
        if pil_image is None:
            self.card_image.config(image='', text='Image not found')
            self._tk_image = None
        else:
            self._tk_image = ImageTk.PhotoImage(pil_image)
            self.card_image.config(image=self._tk_image, text='')
