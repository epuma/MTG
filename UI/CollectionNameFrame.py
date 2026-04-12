from tkinter import Frame, Label


class CollectionNameFrame(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.grid(row=0, column=2, padx=10, pady=10, sticky='NW')

        Label(self, text='Collection:').grid(row=0, column=0, sticky='W')
        self.name_label = Label(self, text='')
        self.name_label.grid(row=0, column=1, sticky='W')

    def update_name(self, name):
        self.name_label.config(text=name)
