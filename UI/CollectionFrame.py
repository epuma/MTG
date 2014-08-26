try:
	from Tkinter import *
except ImportError:
	from tkinter import *

class CollectionFrame(Frame):
	def __init__(self, root):
		Frame.__init__(self, root)
		self.grid(row=2, column=2, padx=10, pady=10, sticky=N)

		self.quant_label = Label(self, text = 'Quantity Owned:')
		self.price_label = Label(self, text = 'Price:')
		self.date_label = Label(self, text = 'Price Last Updated On:')
		self.notes_label = Label(self, text = 'Notes:')

		self.quant_label.grid(row=0, column=0, sticky=NW)
		self.price_label.grid(row=1, column=0, sticky=NW)
		self.date_label.grid(row=2, column=0, sticky=NW)
		self.notes_label.grid(row=3, column=0, sticky=NW)

		self.quant = Label(self, text = '0')
		self.price = Label(self, text = 'High: N/A' + '\n' + 'Medium: N/A' + '\n' + 'Low: N/A', justify=LEFT)
		self.date = Label(self, text = '')
		self.notes = Text(self, height=30, width=30, bd=10)
		self.notes.config(state=DISABLED)

		self.quant.grid(row=0, column=1, sticky=W)
		self.price.grid(row=1, column=1, sticky=W)
		self.date.grid(row=2, column=1, sticky=W)
		self.notes.grid(row=3, column=1, sticky=W)

		self.save_button = Button(self, text = 'Save Notes', command=root.update_notes, state=DISABLED)
		self.save_button.grid(row=4, column=1, sticky=E)

	def update_collection_info(self, root, edition, card):
		if root.collection.data == None:
			self.quant.config(text = '0')
			self.price.config(text = 'High: N/A' + '\n' + 'Medium: N/A' + '\n' + 'Low: N/A', justify=LEFT)
			self.date.config(text = '')
			self.notes.delete(0.0, END)
			self.save_button.config(state=DISABLED)
			self.notes.config(state=DISABLED)
		else:
			price = root.collection.getPrice(edition, card)

			self.save_button.config(state=NORMAL)
			self.notes.config(state=NORMAL)
			self.quant.config(text = root.collection.getQuantity(edition, card))
			self.price.config(text = 'High: ' + price[0] + '\n' + 'Medium: ' + price[1] + '\n' + 'Low: ' + price[2], justify=LEFT)
			self.date.config(text = root.collection.getDateUpdated(edition, card))
			self.notes.delete(0.0, END)
			self.notes.insert(0.0, root.collection.getNotes(edition, card))
			self.notes.focus_set()