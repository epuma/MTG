try:
	from Tkinter import *
except ImportError:
	from tkinter import *

from Menu import createMenu
from ConnectionRequired import is_internet_on, get_image, download_json
from Classes import Magic


def change_image(event=None):
	global tk_image
	tk_image = get_image(card_name.get())
	if isinstance(tk_image, basestring):
		card_image.config(image="", text=tk_image)
	else:
		card_image.config(image=tk_image)


#initialize the app window
root = Tk()
root.wm_title("Eric's Magic App")
#root.wm_iconbitmap('mtgicon.ico')

menubar = createMenu(root)
root.config(menu = menubar)

json_file = 'JSON Files/AllSets-x.json'
mtg_object = Magic(json_file)

#Create a frame to place the card image in
image_frame = Frame(root, width = 240, height = 340)
image_frame.pack()

card_name = StringVar()
card_name.set('Black Lotus')

card_name_entry = Entry(root, textvariable=card_name)
card_name_entry.pack()

enter_button = Button(root, text='Enter', command=change_image)
enter_button.pack()

root.bind('<Return>', change_image)


if is_internet_on():
	tk_image = get_image('Black Lotus')
	card_image = Label(image_frame, image=tk_image)

	#Places the image in the frame
	card_image.place(relx=0.5, rely=0.5, anchor=CENTER)
else:
	no_internet = Label(root, text = 'No Internet! Please Check Your Internet Connection!')
	no_internet.pack()



#This makes the window appear on the top
root.call('wm', 'attributes', '.', '-topmost', '1')
#Sets the minimum size of the window to exactly fit all widgets
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
root.mainloop()