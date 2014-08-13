import sys
from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename

def donothing():
	filewin = Toplevel()
	button = Button(filewin, text = "Do nothing button")
	button.pack()

def get_file_name():
	filePath = askopenfilename()
	return filePath

def open_file():
	filePath = get_file_name()
	#do something to handle the file you have (display it)

def get_save_name():
	filePath = asksaveasfilename(defaultextension = '.json')
	print filePath

def save_file():
    filePath = get_save_name()
	#do something with filename, use it to save the json file

################################ Commands are above #############################################

def createMenu(root):
	
	menubar = Menu(root)

	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="New", command=donothing)
	filemenu.add_command(label="Open", command=open_file)
	filemenu.add_command(label="Save", command=save_file)
	filemenu.add_command(label="Save as...", command=save_file)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=root.quit)

	menubar.add_cascade(label="File", menu=filemenu)

	helpmenu = Menu(menubar, tearoff=0)
	helpmenu.add_command(label="Help Index", command=donothing)
	helpmenu.add_command(label="About...", command=donothing)

	menubar.add_cascade(label="Help", menu=helpmenu)

	return menubar