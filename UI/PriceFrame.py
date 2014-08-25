try:
	from Tkinter import *
except ImportError:
	from tkinter import *

from Prices import get_prices

class PriceFrame(Frame):
	def __init__(self, root):
		Frame.__init__(self, root)
		self.grid(row=1, column=0)

		self.high_label = Label(self, text='TCG Price High')
		self.medium_label = Label(self, text='TCG Price Medium')
		self.low_label = Label(self, text='TCG Price Low')

		self.high_price = Label(self, text='N/A')
		self.medium_price = Label(self, text='N/A')
		self.low_price = Label(self, text='N/A')


		self.high_label.grid(row=0, column=0, sticky=W)
		self.medium_label.grid(row=1, column=0, sticky=W)
		self.low_label.grid(row=2, column=0, sticky=W)

		self.high_price.grid(row=0, column=1, sticky=E)
		self.medium_price.grid(row=1, column=1, sticky=E)
		self.low_price.grid(row=2, column=1, sticky=E)

	def update_prices(self, card_obj, edition):
		new_card = check_split_card(card_obj)
		prices = get_prices(new_card, edition)
		if 'N/A' in prices:
			self.high_price.config(text= prices[0])
			self.medium_price.config(text= prices[1])
			self.low_price.config(text= prices[2])
		else:
			self.high_price.config(text='$'+ prices[0])
			self.medium_price.config(text='$'+ prices[1])
			self.low_price.config(text='$'+ prices[2])

#Changes the name to fit the URL from TCGPlayer if the card is a split card
def check_split_card(card_obj):
	new_card_name = ''
	if card_obj.layout == 'split':
		new_card_name = card_obj.names[0] + ' // ' + card_obj.names[1]
	else:
		new_card_name = card_obj.name
	return new_card_name