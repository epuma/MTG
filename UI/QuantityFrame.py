try:
	from Tkinter import *
except ImportError:
	from tkinter import *

class QuantityFrame(Frame):
	def __init__(self, root):
		Frame.__init__(self, root)
		self.grid(row=1, column=2, padx=10, pady=10, sticky=N)

		self.newq_label = Label(self, text = 'New Quantity:')
		self.newq_label.grid(row=0, column=0, sticky=NW)
		
		self.new_quant = IntVar()
		self.quantity_entry = Entry(self, textvariable=self.new_quant, state=DISABLED)
		self.quantity_entry.grid(row=0, column=1, stick=NW)
		self.new_quant.set(0)

		self.update_button = Button(self, text = 'Update Quantity', command=root.update_quantity, state=DISABLED)
		self.update_button.grid(row=0, column=2, sticky=NE)

	def change_state(self, root):
		if root.collection.data == None:
			self.quantity_entry.config(state=DISABLED)
			self.update_button.config(state=DISABLED)
		else:
			self.quantity_entry.config(state=NORMAL)
			self.update_button.config(state=NORMAL)

