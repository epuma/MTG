try:
	from Tkinter import *
except ImportError:
	from tkinter import *

class CollectionNameFrame(Frame):
	def __init__(self, root):
		Frame.__init__(self, root)
		self.grid(row=0, column=2, padx=10, pady=10, sticky=NW)

		self.collection_name_label = Label(self, text = 'Collection Name:')
		self.collection_name_label.grid(row=0, column=0, sticky=W)
		self.collection_name = Label(self, text = '')
		self.collection_name.grid(row=0, column=1, sticky=W)

	def update_name(self, name):
		self.collection_name.config(text=name)

