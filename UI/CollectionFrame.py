from tkinter import Frame, Label, Text, Button, END


class CollectionFrame(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.grid(row=2, column=2, padx=10, pady=10, sticky='N')

        Label(self, text='Quantity Owned:').grid(row=0, column=0, sticky='NW')
        Label(self, text='Price:').grid(         row=1, column=0, sticky='NW')
        Label(self, text='Last Updated:').grid(  row=2, column=0, sticky='NW')
        Label(self, text='Price History:').grid( row=3, column=0, sticky='NW')
        Label(self, text='Notes:').grid(         row=4, column=0, sticky='NW')

        self.quant = Label(self, text='0')
        self.price = Label(self,
                           text='Market: N/A\nFoil: N/A\nMTGO: N/A',
                           justify='left')
        self.date  = Label(self, text='')

        # Price history — compact read-only text box (Courier for alignment)
        self.history = Text(self, height=5, width=34,
                            font=('Courier', 8), state='disabled', bd=1)

        self.notes = Text(self, height=20, width=30, bd=10)
        self.notes.config(state='disabled')

        self.quant.grid(  row=0, column=1, sticky='W')
        self.price.grid(  row=1, column=1, sticky='W')
        self.date.grid(   row=2, column=1, sticky='W')
        self.history.grid(row=3, column=1, sticky='W')
        self.notes.grid(  row=4, column=1, sticky='W')

        self.save_button = Button(self, text='Save Notes',
                                  command=root.update_notes, state='disabled')
        self.save_button.grid(row=5, column=1, sticky='E')

    # ---------------------------------------------------------------- public

    def update_collection_info(self, root, edition, card):
        if root.collection.data is None:
            self._clear()
        else:
            p = root.collection.getPrice(edition, card)
            self.quant.config(text=root.collection.getQuantity(edition, card))
            self.price.config(
                text=f"Market: {p[0]}\nFoil: {p[1]}\nMTGO: {p[2]}",
                justify='left',
            )
            self.date.config(text=root.collection.getDateUpdated(edition, card))
            self._update_history(root.collection.getPriceHistory(edition, card))
            self.notes.config(state='normal')
            self.notes.delete('1.0', END)
            self.notes.insert('1.0', root.collection.getNotes(edition, card))
            self.notes.focus_set()
            self.save_button.config(state='normal')

    # ---------------------------------------------------------------- private

    def _clear(self):
        self.quant.config(text='0')
        self.price.config(text='Market: N/A\nFoil: N/A\nMTGO: N/A')
        self.date.config(text='')
        self._update_history([])
        self.notes.config(state='normal')
        self.notes.delete('1.0', END)
        self.notes.config(state='disabled')
        self.save_button.config(state='disabled')

    def _update_history(self, history: list):
        """Render recent price snapshots in the read-only history widget."""
        self.history.config(state='normal')
        self.history.delete('1.0', END)
        if history:
            self.history.insert(END, f"{'Date':<20} {'Mkt':>7} {'Foil':>7} {'TIX':>5}\n")
            self.history.insert(END, '-' * 43 + '\n')
            for entry in history[:5]:
                d  = entry.get('date', '')[:17]
                p  = entry.get('prices', ['N/A', 'N/A', 'N/A'])
                mkt  = f"${p[0]}" if p[0] != 'N/A' else 'N/A'
                foil = f"${p[1]}" if p[1] != 'N/A' else 'N/A'
                tix  = p[2] if p[2] != 'N/A' else 'N/A'
                self.history.insert(END, f"{d:<20} {mkt:>7} {foil:>7} {tix:>5}\n")
        else:
            self.history.insert(END, 'No history yet.')
        self.history.config(state='disabled')
