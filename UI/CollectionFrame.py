from tkinter import Frame, Label, Text, Button, END


class CollectionFrame(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.grid(row=2, column=2, padx=10, pady=10, sticky='N')

        Label(self, text='Quantity Owned:').grid(row=0, column=0, sticky='NW')
        Label(self, text='Price:').grid(row=1, column=0, sticky='NW')
        Label(self, text='Price Last Updated:').grid(row=2, column=0, sticky='NW')
        Label(self, text='Notes:').grid(row=3, column=0, sticky='NW')

        self.quant = Label(self, text='0')
        self.price = Label(self,
                           text='Market: N/A\nFoil: N/A\nMTGO: N/A',
                           justify='left')
        self.date = Label(self, text='')
        self.notes = Text(self, height=30, width=30, bd=10)
        self.notes.config(state='disabled')

        self.quant.grid(row=0, column=1, sticky='W')
        self.price.grid(row=1, column=1, sticky='W')
        self.date.grid(row=2, column=1, sticky='W')
        self.notes.grid(row=3, column=1, sticky='W')

        self.save_button = Button(self, text='Save Notes',
                                  command=root.update_notes, state='disabled')
        self.save_button.grid(row=4, column=1, sticky='E')

    def update_collection_info(self, root, edition, card):
        if root.collection.data is None:
            self.quant.config(text='0')
            self.price.config(text='Market: N/A\nFoil: N/A\nMTGO: N/A')
            self.date.config(text='')
            self.notes.config(state='normal')
            self.notes.delete('1.0', END)
            self.notes.config(state='disabled')
            self.save_button.config(state='disabled')
        else:
            p = root.collection.getPrice(edition, card)
            self.quant.config(text=root.collection.getQuantity(edition, card))
            self.price.config(
                text=f"Market: {p[0]}\nFoil: {p[1]}\nMTGO: {p[2]}",
                justify='left'
            )
            self.date.config(text=root.collection.getDateUpdated(edition, card))
            self.notes.config(state='normal')
            self.notes.delete('1.0', END)
            self.notes.insert('1.0', root.collection.getNotes(edition, card))
            self.notes.focus_set()
            self.save_button.config(state='normal')
