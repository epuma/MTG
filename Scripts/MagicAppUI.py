from Tkinter import *
from Menu import createMenu

root = Tk()
root.wm_title("Eric's Magic App")
#root.wm_iconbitmap('mtgicon.ico')

menubar = createMenu(root)
root.config(menu=menubar)

root.mainloop()