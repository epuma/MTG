try:
	from Tkinter import *
except ImportError:
	from tkinter import *

class SearchFrame(Frame):
	def __init__(self, root):
		Frame.__init__(self, root)
		self.grid(row=0, column=0)
		
		self.mtg_object = root.mtg_object
		
		self.edition_options = sorted(self.mtg_object.data.keys())
		self.edition_variable = StringVar()
		self.card_variable = StringVar()
		self.edition_variable.trace('w', self.update_options)
		self.edition_option_menu = OptionMenu(self, self.edition_variable, *self.edition_options)
		self.card_option_menu = OptionMenu(self, self.card_variable, '')

		self.edition_variable.set(self.edition_options[0])

		self.edition_option_menu.grid(row=0, column=0)
		self.card_option_menu.grid(row=0, column=1)

		self.enter_button = Button(self, text='Enter', command=root.update_ui)
		self.enter_button.grid(row=0, column=2)

	#OptionMenus
	def update_options(self, *args):
		cards = sorted(self.mtg_object.data[self.edition_variable.get()].data.keys())
		self.card_variable.set(cards[0])
		menu = self.card_option_menu['menu']
		menu.delete(0, 'end')
		for card in cards:
			menu.add_command(label = card, command=lambda card=card: self.card_variable.set(card))
