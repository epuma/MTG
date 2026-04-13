#!/usr/bin/env python3
"""MTG Collection Manager — main application entry point."""

import os
import tkinter as tk
from tkinter import Entry, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

import scryfall
from Classes import Magic, Collection, Database
from UI import (
    CreateMenu, SplashScreen, SearchFrame, PriceFrame,
    ImageFrame, ScrollFrame, CollectionFrame, CollectionNameFrame,
    QuantityFrame, StatsFrame, ScryfallSearchFrame, CollectionGridView,
)

DB_JSON   = 'JSON Files/AllSets-x.json'
DB_SQLITE = 'cards.db'


# ──────────────────────────────────────────────── startup helpers

def _download_json(path: str) -> None:
    import urllib.request
    print('Downloading card database from MTGJson…')
    urllib.request.urlretrieve('https://mtgjson.com/api/v5/AllSets.json', path)
    print('Download complete.')


def _ensure_sqlite() -> None:
    """Build cards.db from AllSets-x.json on first run (or if missing)."""
    if os.path.exists(DB_SQLITE):
        return
    if not os.path.exists(DB_JSON):
        _download_json(DB_JSON)
    print('Building card database — first run only, please wait…')
    import build_db
    build_db.build(DB_JSON, DB_SQLITE)


def _load_database():
    """Return a Database (SQLite) instance, falling back to Magic (JSON)."""
    try:
        _ensure_sqlite()
        return Database(DB_SQLITE)
    except Exception as exc:
        print(f'SQLite unavailable ({exc}), loading from JSON…')
        if not os.path.exists(DB_JSON):
            _download_json(DB_JSON)
        return Magic(DB_JSON)


# ──────────────────────────────────────────────── main app

class MagicApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self._scryfall_win = None   # singleton search window
        self._grid_win     = None   # singleton grid window
        self._init_ui()

    # ────────────────────────────────────────── setup

    def _init_ui(self):
        self.grid()
        wt_ratio    = self.winfo_screenwidth()  / 1440
        ht_ratio    = self.winfo_screenheight() / 900
        self.img_wt = int(wt_ratio * 480)
        self.img_ht = int(ht_ratio * 680)

        self.withdraw()
        splash = SplashScreen(self)

        print('Loading card database…')
        self.mtg_object = _load_database()
        self.collection = Collection()
        print('Ready.')

        splash.destroy()
        self.deiconify()

        self.config(menu=CreateMenu(self))

        self.search_frame          = SearchFrame(self)
        self.price_frame           = PriceFrame(self)
        self.image_frame           = ImageFrame(self)
        self.scroll_frame          = ScrollFrame(self)
        self.collection_frame      = CollectionFrame(self)
        self.collection_name_frame = CollectionNameFrame(self)
        self.quantity_frame        = QuantityFrame(self)
        self.stats_frame           = StatsFrame(self)

        self._bind_keys()
        self.bind('<Return>', self.update_ui)

        self.update()
        self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_height()}+0+0')
        self.minsize(self.winfo_screenwidth(), self.winfo_height())

    def _bind_keys(self):
        # File operations
        self.bind('<Control-n>', lambda _: self.new_file())
        self.bind('<Control-o>', lambda _: self.open_file())
        self.bind('<Control-s>', lambda _: self.save_file())
        self.bind('<Control-e>', lambda _: self.export_collection())

        # Card navigation (Alt+arrows to avoid clashing with text-entry shortcuts)
        self.bind('<Alt-Left>',  self._prev_card)
        self.bind('<Alt-Right>', self._next_card)
        self.bind('<Alt-Up>',    self._prev_edition)
        self.bind('<Alt-Down>',  self._next_edition)

    # ────────────────────────────────────────── keyboard navigation

    def _prev_card(self, _event=None):
        if self.search_frame.select_relative(-1):
            self.update_ui()

    def _next_card(self, _event=None):
        if self.search_frame.select_relative(1):
            self.update_ui()

    def _prev_edition(self, _event=None):
        if self.search_frame.select_edition_relative(-1):
            self.update_ui()

    def _next_edition(self, _event=None):
        if self.search_frame.select_edition_relative(1):
            self.update_ui()

    # ────────────────────────────────────────── file actions

    def new_file(self):
        path = asksaveasfilename(defaultextension='.json')
        if not path:
            return
        self.collection.newCollection(self.mtg_object, path)
        self.collection.load(path)
        self._refresh_collection_ui(path)

    def open_file(self):
        path = askopenfilename()
        if not path:
            return
        self.collection.load(path)
        self.collection.updateCollection(self.mtg_object)
        self._refresh_collection_ui(path)

    def save_file(self):
        path = asksaveasfilename(defaultextension='.json')
        if path:
            self.collection.save(path)

    def save_close_file(self):
        path = asksaveasfilename(defaultextension='.json')
        if not path:
            return
        self.collection.save_close(path)
        self.collection_name_frame.update_name('')
        self.collection_frame.update_collection_info(self, self.edition, self.card)
        self.quantity_frame.change_state(self)
        self.stats_frame.update_stats(self.collection)

    def export_collection(self):
        if self.collection.data is None:
            messagebox.showwarning('No collection open',
                                   'Please open a collection before exporting.')
            return
        path = asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
        )
        if path:
            self.collection.export_csv(path)
            messagebox.showinfo('Export complete', f'Owned cards exported to:\n{path}')

    def _refresh_collection_ui(self, path: str):
        self.collection_name_frame.update_name(os.path.basename(path))
        self.collection_frame.update_collection_info(self, self.edition, self.card)
        self.quantity_frame.change_state(self)
        self.stats_frame.update_stats(self.collection)

    # ────────────────────────────────────────── view actions

    def open_scryfall_search(self):
        if self._scryfall_win and self._scryfall_win.winfo_exists():
            self._scryfall_win.lift()
            return
        self._scryfall_win = ScryfallSearchFrame(self)
        self._scryfall_win.set_on_select(self._on_scryfall_card_selected)

    def open_collection_grid(self):
        if self.collection.data is None:
            messagebox.showwarning('No collection open',
                                   'Please open a collection first.')
            return
        if self._grid_win and self._grid_win.winfo_exists():
            self._grid_win.lift()
            return
        self._grid_win = CollectionGridView(
            self, self.collection, self.mtg_object,
            on_card_select=self._on_grid_card_selected,
        )

    # ────────────────────────────────────────── callbacks from child windows

    def _on_scryfall_card_selected(self, scryfall_card: dict):
        """Display a card from Scryfall search without touching the dropdowns."""
        card_obj = scryfall.scryfall_to_card(scryfall_card)
        set_code = scryfall_card.get('set', '')

        self.scroll_frame.update_info(card_obj)
        self.image_frame.update_image_from_code(card_obj.name, set_code)

        # Prices are already in the search result — no extra API call needed
        p = scryfall_card.get('prices', {})
        self.price_frame.set_prices_direct([
            p.get('usd')      or 'N/A',
            p.get('usd_foil') or 'N/A',
            p.get('tix')      or 'N/A',
        ])

    def _on_grid_card_selected(self, edition_name: str, card_name: str):
        """Update dropdowns + main panels when a card is clicked in the grid."""
        if edition_name in self.mtg_object.data:
            if card_name in self.mtg_object.data[edition_name].data:
                self.search_frame.edition_variable.set(edition_name)
                self.search_frame.card_variable.set(card_name)
                self.update_ui()

    # ────────────────────────────────────────── help

    def show_about(self):
        messagebox.showinfo(
            'About',
            'MTG Collection Manager\n\n'
            'Tracks your Magic: The Gathering card collection.\n'
            'Card data, images and prices provided by Scryfall (scryfall.com).',
        )

    def show_shortcuts(self):
        messagebox.showinfo(
            'Keyboard Shortcuts',
            'Ctrl+N       New collection\n'
            'Ctrl+O       Open collection\n'
            'Ctrl+S       Save collection\n'
            'Ctrl+E       Export as CSV\n'
            '\n'
            'Alt+Left     Previous card\n'
            'Alt+Right    Next card\n'
            'Alt+Up       Previous edition\n'
            'Alt+Down     Next edition\n'
            '\n'
            'Enter        Load selected card\n'
        )

    # ────────────────────────────────────────── main event handlers

    def update_ui(self, _event=None):
        self.edition = self.search_frame.edition_variable.get()
        self.card    = self.search_frame.card_variable.get()
        if not self.edition or not self.card:
            return
        card_obj = self.mtg_object.data[self.edition].data[self.card]

        edition, card = self.edition, self.card   # capture for async closure

        def on_prices_ready(prices):
            if self.collection.data is not None:
                self.collection.updatePrice(edition, card, prices)
                self.stats_frame.update_stats(self.collection)

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
        self.stats_frame.update_stats(self.collection)


if __name__ == '__main__':
    app = MagicApp()
    app.wm_title("Eric's Magic App")
    app.mainloop()
