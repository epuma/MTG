from tkinter import Toplevel, Frame, Label, Scrollbar, Text, END, N, S


class CollectionValueHistory(Toplevel):
    """Toplevel window showing total collection value over time."""

    def __init__(self, root, collection):
        super().__init__(root)
        self.title('Collection Value History')
        self.resizable(True, True)
        self.geometry('520x400')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        Label(self, text='Collection Value Over Time',
              font=('TkDefaultFont', 12, 'bold')).grid(
            row=0, column=0, padx=12, pady=(10, 4), sticky='W')

        frame = Frame(self)
        frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='NSEW')
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        sb = Scrollbar(frame)
        sb.grid(row=0, column=1, sticky=N + S)
        self._text = Text(frame, font=('Courier', 9), state='disabled',
                          yscrollcommand=sb.set, width=60, height=20, bd=1)
        self._text.grid(row=0, column=0, sticky='NSEW')
        sb.config(command=self._text.yview)

        self._populate(collection.get_value_history())

    def _populate(self, history: list):
        self._text.config(state='normal')
        self._text.delete('1.0', END)
        if history:
            self._text.insert(END, f"{'Date':<12} {'Market':>10} {'Foil':>10} {'TIX':>10}\n")
            self._text.insert(END, '-' * 46 + '\n')
            for entry in history:
                mkt = f"${entry['market']:.2f}"
                foi = f"${entry['foil']:.2f}"
                tix = f"{entry['tix']:.2f}"
                self._text.insert(
                    END, f"{entry['date']:<12} {mkt:>10} {foi:>10} {tix:>10}\n")
        else:
            self._text.insert(
                END,
                'No value history recorded yet.\n\n'
                'Browse cards with a collection open to start\n'
                'recording daily value snapshots.',
            )
        self._text.config(state='disabled')
