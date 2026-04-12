#!/usr/bin/env python3
"""MTG Collection Manager — main application entry point."""

import os
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

from Classes import Magic, Collection
from UI import (
    CreateMenu, SplashScreen, SearchFrame, PriceFrame,
    ImageFrame, ScrollFrame, CollectionFrame, CollectionNameFrame,
    QuantityFrame,
)


DB_PATH = 'JSON Files/AllSets-x.json'


def _ensure_database():
    """Download the card database if it is not present locally."""
    if os.path.exists(DB_PATH):
        return
    print('Card database not found. Attempting download from MTGJson…')
    import urllib.request
    url = 'https://mtgjson.com/api/v5/AllSets.json'
    try:
        urllib.request.urlretrieve(url, DB_PATH)
        print('Download complete.')
    except Exception as exc:
        raise FileNotFoundError(
            f'Cannot find or download {DB_PATH}.\n'
            'Please place AllSets-x.json in the "JSON Files" directory.'
        ) from exc


class MagicApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self._init_ui()

    # ---------------------------------------------------------------- setup

    def _init_ui(self):
        self.grid()
        wt_ratio = self.winfo_screenwidth()  / 1440
        ht_ratio = self.winfo_screenheight() / 900
        self.img_wt = int(wt_ratio * 480)
        self.img_ht = int(ht_ratio * 680)

        # Hide the main window while the splash is up
        self.withdraw()
        splash = SplashScreen(self)

        print('Checking database…')
        _ensure_database()

        print('Loading card database…')
        self.mtg_object = Magic(DB_PATH)
        self.collection = Collection()
        print('Done.')

        splash.destroy()
        self.deiconify()

        # Menu
        self.config(menu=CreateMenu(self))

        # Frames
        self.search_frame          = SearchFrame(self)
        self.price_frame           = PriceFrame(self)
        self.image_frame           = ImageFrame(self)
        self.scroll_frame          = ScrollFrame(self)
        self.collection_frame      = CollectionFrame(self)
        self.collection_name_frame = CollectionNameFrame(self)
        self.quantity_frame        = QuantityFrame(self)

        self.bind('<Return>', self.update_ui)

        # Size the window to fit all widgets exactly
        self.update()
        self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_height()}+0+0')
        self.minsize(self.winfo_screenwidth(), self.winfo_height())

    # ---------------------------------------------------------- file actions

    def new_file(self):
        path = asksaveasfilename(defaultextension='.json')
        if not path:
            return
        self.collection.newCollection(self.mtg_object, path)
        self.collection.load(path)
        self.collection_name_frame.update_name(os.path.basename(path))
        self.collection_frame.update_collection_info(self, self.edition, self.card)
        self.quantity_frame.change_state(self)

    def open_file(self):
        path = askopenfilename()
        if not path:
            return
        self.collection.load(path)
        self.collection.updateCollection(self.mtg_object)
        self.collection_name_frame.update_name(os.path.basename(path))
        self.collection_frame.update_collection_info(self, self.edition, self.card)
        self.quantity_frame.change_state(self)

    def save_file(self):
        path = asksaveasfilename(defaultextension='.json')
        if not path:
            return
        self.collection.save(path)

    def save_close_file(self):
        path = asksaveasfilename(defaultextension='.json')
        if not path:
            return
        self.collection.save_close(path)
        self.collection_name_frame.update_name('')
        self.collection_frame.update_collection_info(self, self.edition, self.card)
        self.quantity_frame.change_state(self)

    # ---------------------------------------------------------- UI helpers

    def show_about(self):
        messagebox.showinfo(
            'About',
            'MTG Collection Manager\n\nTracks your Magic: The Gathering card collection.\n'
            'Prices and card images provided by Scryfall (scryfall.com).',
        )

    # ---------------------------------------------------------- event handlers

    def update_ui(self, _event=None):
        self.edition = self.search_frame.edition_variable.get()
        self.card    = self.search_frame.card_variable.get()
        card_obj = self.mtg_object.data[self.edition].data[self.card]

        # Capture edition/card now so the async callback uses the right values
        edition, card = self.edition, self.card

        def on_prices_ready(prices):
            if self.collection.data is not None:
                self.collection.updatePrice(edition, card, prices)

        self.price_frame.update_prices(card_obj, self.edition,
                                       on_complete=on_prices_ready)
        self.image_frame.update_image(card_obj, self.edition)
        self.scroll_frame.update_info(card_obj)
        self.collection_frame.update_collection_info(self, self.edition, self.card)
        self.quantity_frame.change_state(self)

    def update_notes(self, _event=None):
        self.collection.updateNotes(
            self.edition, self.card,
            self.collection_frame.notes.get('1.0', tk.END),
        )

    def update_quantity(self, _event=None):
        self.collection.updateQuantity(
            self.edition, self.card,
            self.quantity_frame.new_quant.get(),
        )
        self.quantity_frame.new_quant.set(0)
        self.collection_frame.update_collection_info(self, self.edition, self.card)


if __name__ == '__main__':
    app = MagicApp()
    app.wm_title("Eric's Magic App")
    app.mainloop()
