try:
	from Tkinter import *
except ImportError:
	from tkinter import *

class ScrollFrame(Frame):
	def __init__(self, root):
		Frame.__init__(self, root)
		self.img_wt = root.img_wt
		self.img_ht = root.img_ht
		self.configure(width = self.img_wt, height = self.img_ht)
		self.grid(row=2, column=1, padx=10, pady=10, sticky=N)

		#scrollbar!
		self.canvas = Canvas(self)
		self.info_frame = Frame(self.canvas)
		self.info_scrollbar = AutoScrollbar(self)
		self.info_scrollbar.config(command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.info_scrollbar.set)

		self.info_scrollbar.grid(row=0, column=1, sticky=N+S)
		self.canvas.grid(row=0, column=0)
		self.canvas.create_window((0,0), window=self.info_frame, anchor='nw')
		self.info_frame.bind("<Configure>", self.scroll_function)
		self.info_frame.bind("<MouseWheel>", self.on_mouse_wheel)


		self.default_edition = 'Limited Edition Alpha'
		self.default_card = 'Black Lotus'
		self.card_object = root.mtg_object.data[self.default_edition].data[self.default_card]
		self.initialize()

	def initialize(self):
		self.info_attributes = [
						   'name',
						   'manaCost',
						   'type',
						   'rarity',
						   'text',
						   'flavor',
						   'power',
						   'toughness',
						   'loyalty',
						   'printings',
						   'artist',
						   'number',
						   'multiverseid',
						   'border',
						   'timeshifted',
						   'hand',
						   'life',
						   'rulings',
						   'legalities',
						   'originalText',
						   'originalType'
						   ]

		self.info_attribute_labels = [
								 Label(self.info_frame, text = self.card_object.name),
								 Label(self.info_frame, text = self.card_object.manaCost),
								 Label(self.info_frame, text = self.card_object.type),
								 Label(self.info_frame, text = self.card_object.rarity),
								 Label(self.info_frame, text = self.card_object.text),
								 Label(self.info_frame, text = self.card_object.flavor),
								 Label(self.info_frame, text = self.card_object.power),
								 Label(self.info_frame, text = self.card_object.toughness),
								 Label(self.info_frame, text = self.card_object.loyalty),
								 Label(self.info_frame, text = self.card_object.printings),
								 Label(self.info_frame, text = self.card_object.artist),
								 Label(self.info_frame, text = self.card_object.number),
								 Label(self.info_frame, text = self.card_object.multiverseid),
								 Label(self.info_frame, text = self.card_object.border),
								 Label(self.info_frame, text = self.card_object.timeshifted),
								 Label(self.info_frame, text = self.card_object.hand),
								 Label(self.info_frame, text = self.card_object.life),
								 Label(self.info_frame, text = self.card_object.rulings),
								 Label(self.info_frame, text = self.card_object.legalities),
								 Label(self.info_frame, text = self.card_object.originalText),
								 Label(self.info_frame, text = self.card_object.originalType)
								 ]



		self.info_labels = [
					   Label(self.info_frame, text = 'Name:'),
					   Label(self.info_frame, text = 'Casting Cost:'),
					   Label(self.info_frame, text = 'Type:'),
					   Label(self.info_frame, text = 'Rarity:'),
					   Label(self.info_frame, text = 'Text:'),
					   Label(self.info_frame, text = 'Flavor Text:'),
					   Label(self.info_frame, text = 'Power:'),
					   Label(self.info_frame, text = 'Toughness:'),
					   Label(self.info_frame, text = 'Loyalty Counters:'),
					   Label(self.info_frame, text = 'Set Printings:'),
					   Label(self.info_frame, text = 'Artist:'),
					   Label(self.info_frame, text = 'Card Number:'),
					   Label(self.info_frame, text = 'MultiVerse ID:'),
					   Label(self.info_frame, text = 'Border Color:'),
					   Label(self.info_frame, text = 'Timeshifted:'),
					   Label(self.info_frame, text = 'Max Hand Modifier:'),
					   Label(self.info_frame, text = 'Max Life Modifier:'),
					   Label(self.info_frame, text = 'Rulings:'),
					   Label(self.info_frame, text = 'Legality:'),
					   Label(self.info_frame, text = 'Original Text:'),
					   Label(self.info_frame, text = 'Original Type:')
					   ]

		i = 0
		for n in range(len(self.info_attributes)):
			if getattr(self.card_object, self.info_attributes[n]) is not None:
				self.info_labels[n].grid(row=i, column=0, sticky=NW)
				self.info_attribute_labels[n].config(wraplength=350, justify=LEFT)
				self.info_attribute_labels[n].grid(row=i, column=1, sticky=W)
				i += 1

	def scroll_function(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=self.img_wt,height=self.img_ht)
	def on_mouse_wheel(self, event):
		if platform.system() == 'Darwin':
			self.scroll_frame.canvas.yview_scroll(-1*(event.delta), "units")
		else:
			self.scroll_frame.canvas.yview_scroll(-1*(event.delta)/120, "units")

	def update_info(self, card_obj):
		print 'Updating Info!'
		i = 0
		for n in range(len(self.info_attributes)):
			self.info_labels[n].grid_forget()
			self.info_attribute_labels[n].grid_forget()
		
		for n in range(len(self.info_attributes)):
			if getattr(card_obj, self.info_attributes[n]) is not None:
				self.info_labels[n].grid(row=i, column=0, sticky=NW)
				self.info_attribute_labels[n].config(text=getattr(card_obj, self.info_attributes[n]), wraplength=350, justify=LEFT)
				self.info_attribute_labels[n].grid(row=i, column=1, sticky=W)
				i += 1


class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError, "cannot use pack with this widget"
    def place(self, **kw):
        raise TclError, "cannot use place with this widget"