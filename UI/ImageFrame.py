try:
	from Tkinter import *
except ImportError:
	from tkinter import *

from ConnectionRequired import is_internet_on, get_image

class ImageFrame(Frame):
	def __init__(self, root):
		Frame.__init__(self, root)
		self.img_wt = root.img_wt
		self.img_ht = root.img_ht
		self.configure(width = self.img_wt+10, height = self.img_ht+10, bd=10, relief=RIDGE)
		self.grid(row=2,column=0, padx=10, pady=10, sticky=N)

		if is_internet_on():
			self.tk_image = get_image('Limited Edition Alpha', 'Black Lotus', self.img_wt, self.img_ht)
			self.card_image = Label(self, image=self.tk_image)
		
			#Places the image in the frame
			self.card_image.place(relx=0.5, rely=0.5, anchor=CENTER)
		else:
			self.card_image = Label(self, text = 'No Internet!')
			self.card_image.place(relx=0.5, rely=0.5, anchor=CENTER)

	def update_image(self, card, edition, mtg_object):
		card_name = mtg_object.data[edition].data[card].imageName
		self.tk_image = get_image(edition, card_name, self.img_wt, self.img_ht)
		if self.tk_image is None:
			self.card_image.config(image="", text='Card not Found')
		else:
			self.card_image.config(image=self.tk_image)