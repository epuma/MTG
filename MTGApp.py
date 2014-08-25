#! /usr/bin/env python

try:
	from Tkinter import *
except ImportError:
	from tkinter import *

import os
import platform
from UI import CreateMenu, SplashScreen, SearchFrame, PriceFrame, ImageFrame, ScrollFrame
from Classes import Magic, Collection
from ConnectionRequired import is_internet_on, download_json
from tkFileDialog import askopenfilename, asksaveasfilename

class magic_app(Tk):
	def __init__(self, parent):
		Tk.__init__(self, parent)
		self.parent = parent
		self.initialize()

	def initialize(self):
		self.grid()
		wt_ratio = self.winfo_screenwidth()/1440
		ht_ratio = self.winfo_screenheight()/900
		self.img_wt = int(wt_ratio * 480)
		self.img_ht = int(ht_ratio * 680)

		#forces Python to the front
		os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

		#SplashScreen
		self.withdraw()
		splash_screen = SplashScreen(self)
		
		#Download any Updates
		print 'Downloading Updates...'
		if is_internet_on():
			download_json()
		else:
			print 'Download Failed, lack of Internet Connection'
		
		#Initialize MTG Object and Collection Object
		print 'Loading...'
		json_file = 'JSON Files/AllSets-x.json'
		self.mtg_object = Magic(json_file)
		self.collection = Collection()
		print 'DONE!'

		splash_screen.destroy()
		self.deiconify()

		#Initiate Menu
		menubar = CreateMenu(self)
		self.config(menu = menubar)
		
		#Search Frame
		self.search_frame = SearchFrame(self)
		self.bind('<Return>', self.update_ui)
		
		#Price Frame
		self.price_frame = PriceFrame(self)
			
		#Image Frame
		self.image_frame = ImageFrame(self)
		
		#Scroll Frame
		self.scroll_frame = ScrollFrame(self)
		self.bind_all("<MouseWheel>", self.on_mouse_wheel)
		
		#Implement Collections Here

		#Sets size of window to exactly fit all widgets
		self.update()
		self.winWt = self.winfo_width()
		self.winHt = self.winfo_height()
		self.geometry('%dx%d+%d+%d' % (self.winWt, self.winHt, 0, 0))
		self.minsize(self.winWt, self.winHt)
		self.maxsize(self.winWt, self.winHt)

	#This Method does nothing
	def donothing(self):
		filewin = Toplevel()
		button = Button(filewin, text = "Do nothing button")
		button.pack()
	
	#Methods for File Management
	def new_file(self):
		filePath = asksaveasfilename(defaultextension = '.json')
		self.collection.newCollection(self.mtg_object, filePath)
		self.collection.load(filePath)
	def open_file(self):
		filePath = askopenfilename()
		self.collection.load(filePath)
		print self.collection
	def save_file(self):
		filePath = asksaveasfilename(defaultextension = '.json')
		self.collection.save(filePath)
	
	#Methods to handle Events
	def update_ui(self, event=None):
		edition = self.search_frame.edition_variable.get()
		card = self.search_frame.card_variable.get()
		card_obj = self.mtg_object.data[edition].data[card]
		self.price_frame.update_prices(card_obj, edition)
		self.image_frame.update_image(card_obj, edition)
		self.scroll_frame.update_info(card_obj)
	def on_mouse_wheel(self, event):
		if platform.system() == 'Darwin':
			self.scroll_frame.canvas.yview_scroll(-1*(event.delta), "units")
		else:
			self.scroll_frame.canvas.yview_scroll(-1*(event.delta)/120, "units")

if __name__ == "__main__":
    app = magic_app(None)
    app.wm_title("Eric's Magic App")
    app.mainloop()


