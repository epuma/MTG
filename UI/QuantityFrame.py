from tkinter import Frame, Label, Entry, Button, IntVar


class QuantityFrame(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.grid(row=1, column=2, padx=10, pady=10, sticky='N')

        Label(self, text='New Quantity:').grid(row=0, column=0, sticky='NW')

        self.new_quant = IntVar(value=0)
        self.quantity_entry = Entry(self, textvariable=self.new_quant,
                                   state='disabled')
        self.quantity_entry.grid(row=0, column=1, sticky='NW')

        self.update_button = Button(self, text='Update Quantity',
                                    command=root.update_quantity,
                                    state='disabled')
        self.update_button.grid(row=0, column=2, sticky='NE')

    def change_state(self, root):
        state = 'normal' if root.collection.data is not None else 'disabled'
        self.quantity_entry.config(state=state)
        self.update_button.config(state=state)
