from tkinter import Menu


class CreateMenu(Menu):
    def __init__(self, root):
        super().__init__(root)

        filemenu = Menu(self, tearoff=0)
        filemenu.add_command(label='New',              command=root.new_file)
        filemenu.add_command(label='Open',             command=root.open_file)
        filemenu.add_command(label='Save',             command=root.save_file)
        filemenu.add_command(label='Save as...',       command=root.save_file)
        filemenu.add_command(label='Save and Close',   command=root.save_close_file)
        filemenu.add_separator()
        filemenu.add_command(label='Export as CSV...', command=root.export_collection)
        filemenu.add_separator()
        filemenu.add_command(label='Exit',             command=root.quit)
        self.add_cascade(label='File', menu=filemenu)

        helpmenu = Menu(self, tearoff=0)
        helpmenu.add_command(label='About...', command=root.show_about)
        self.add_cascade(label='Help', menu=helpmenu)
