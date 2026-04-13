"""
Scryfall full-text search window.

Opened via View → Search Scryfall…  as a non-modal Toplevel.
When the user clicks a result the on_select callback receives the raw
Scryfall card dict; MTGApp converts it and updates the main panels.
"""
import threading
from tkinter import (
    Toplevel, Frame, Label, Entry, Button, Listbox, Scrollbar,
    StringVar, END,
)

import scryfall


class ScryfallSearchFrame(Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title('Search Scryfall')
        self.geometry('420x380')
        self.resizable(True, True)

        self._on_select = None
        self._results: list = []
        self._page      = 1
        self._has_more  = False
        self._query     = ''

        self._build_ui()

    # ---------------------------------------------------------------- setup

    def _build_ui(self):
        Label(self, text='Scryfall Search',
              font=('Helvetica', 11, 'bold')).pack(pady=(8, 2))

        # ── search bar ────────────────────────────────────────────────────
        bar = Frame(self)
        bar.pack(fill='x', padx=10, pady=4)

        self._query_var = StringVar()
        self._entry = Entry(bar, textvariable=self._query_var, font=('Helvetica', 10))
        self._entry.pack(side='left', fill='x', expand=True)
        self._entry.bind('<Return>', lambda _: self._start_search())
        self._entry.focus_set()

        Button(bar, text='Search', command=self._start_search).pack(side='left', padx=(4, 0))

        # ── status ────────────────────────────────────────────────────────
        self._status = Label(self, text='Type a query and press Search.',
                             fg='grey', font=('Helvetica', 8), anchor='w')
        self._status.pack(fill='x', padx=12)

        # ── results listbox ───────────────────────────────────────────────
        list_frame = Frame(self)
        list_frame.pack(fill='both', expand=True, padx=10, pady=4)

        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')

        self._listbox = Listbox(list_frame, font=('Helvetica', 9),
                                yscrollcommand=scrollbar.set, activestyle='dotbox')
        self._listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self._listbox.yview)
        self._listbox.bind('<<ListboxSelect>>', self._on_listbox_select)

        # ── load-more button ──────────────────────────────────────────────
        self._more_btn = Button(self, text='Load more results…',
                                command=self._load_more, state='disabled')
        self._more_btn.pack(pady=(0, 8))

        Label(self, text='Tip: use Scryfall syntax, e.g.  type:creature cmc<=2  or  set:lea',
              font=('Helvetica', 7), fg='grey').pack(pady=(0, 4))

    # ---------------------------------------------------------------- callbacks

    def set_on_select(self, callback):
        """callback(scryfall_card_dict) — called on the main thread."""
        self._on_select = callback

    # ---------------------------------------------------------------- search

    def _start_search(self, page: int = 1):
        query = self._query_var.get().strip()
        if not query:
            return
        if page == 1:
            self._query = query
            self._results.clear()
            self._listbox.delete(0, END)

        self._page = page
        self._status.config(text='Searching…')
        self._more_btn.config(state='disabled')

        threading.Thread(
            target=self._search_worker,
            args=(query, page),
            daemon=True,
        ).start()

    def _search_worker(self, query: str, page: int):
        cards, has_more, total = scryfall.search_cards(query, page)
        self.after(0, self._show_results, cards, has_more, total)

    def _show_results(self, cards: list, has_more: bool, total: int):
        self._has_more = has_more
        self._results.extend(cards)

        for card in cards:
            set_label = card.get('set_name') or card.get('set', '').upper()
            self._listbox.insert(END, f"  {card['name']}  [{set_label}]")

        shown = len(self._results)
        if self._page == 1:
            self._status.config(
                text=f'{total} result(s) found.' if total else 'No results found.'
            )
        else:
            self._status.config(text=f'Showing {shown} of {total}.')

        self._more_btn.config(state='normal' if has_more else 'disabled')

    def _load_more(self):
        self._start_search(page=self._page + 1)

    def _on_listbox_select(self, _event):
        sel = self._listbox.curselection()
        if not sel or self._on_select is None:
            return
        idx = sel[0]
        if idx < len(self._results):
            self._on_select(self._results[idx])
