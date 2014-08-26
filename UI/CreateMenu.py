import sys

try:
	from Tkinter import *
except ImportError:
	from tkinter import *

class CreateMenu(Menu):
	def __init__(self, root):
		Menu.__init__(self, root)
		self.filemenu = Menu(self, tearoff=0)
		self.filemenu.add_command(label="New", command=root.new_file)
		self.filemenu.add_command(label="Open", command=root.open_file)
		self.filemenu.add_command(label="Save", command=root.save_file)
		self.filemenu.add_command(label="Save as...", command=root.save_file)
		self.filemenu.add_command(label="Save and Close", command=root.save_close_file)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit", command=root.quit)
		
		self.add_cascade(label="File", menu=self.filemenu)
		
		self.helpmenu = Menu(self, tearoff=0)
		self.helpmenu.add_command(label="Help Index", command=root.donothing)
		self.helpmenu.add_command(label="About...", command=root.donothing)
		
		self.add_cascade(label="Help", menu=self.helpmenu)
