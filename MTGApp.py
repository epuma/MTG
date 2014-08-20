#! /usr/bin/env python

try:
	from Tkinter import *
except ImportError:
	from tkinter import *

from Menu import create_menu
from ConnectionRequired import is_internet_on, get_image, download_json
from Classes import Magic
import time
import os
from Prices import get_prices

def change_image(event=None):
	global tk_image
	edition = edition_variable.get()
	card = card_variable.get()
	card_name = mtg_object.data[edition].data[card].imageName
	tk_image = get_image(edition, card_name, img_wt, img_ht)
	if isinstance(tk_image, basestring):
		card_image.config(image="", text=tk_image)
		high_price.config(text='N/A')
		medium_price.config(text='N/A')
		low_price.config(text='N/A')
	else:
		card_image.config(image=tk_image)
		update_prices(card, edition)

def update_prices(card, edition):
	prices = get_prices(card, edition)
	high_price.config(text='$'+ prices[0])
	medium_price.config(text='$'+ prices[1])
	low_price.config(text='$'+ prices[2])

#initialize the app window
root = Tk()
root.wm_title("Eric's Magic App")
#root.wm_iconbitmap('mtgicon.ico')
scrnWt = root.winfo_screenwidth()
scrnHt = root.winfo_screenheight()
wt_ratio = scrnWt/1440
ht_ratio = scrnHt/900
img_wt = int(wt_ratio * 480)
img_ht = int(ht_ratio * 680)

#forces the Python to the front
os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

#####################################################
import io
from PIL import Image, ImageTk
pil_image = Image.open('SplashScreen.jpg')
w,h = pil_image.size
pil_image = pil_image.resize((w/2, h/2), Image.ANTIALIAS)
splash_image = ImageTk.PhotoImage(pil_image)

#splash screen???
root.withdraw()
splash_screen = Toplevel()
splash_screen.overrideredirect(1)
splash_screen.attributes('-topmost', 1)

imgXPos = (scrnWt / 2) - (w / 4)
imgYPos = (scrnHt / 2) - (h / 4)

splash_screen.geometry('+%d+%d' % (imgXPos, imgYPos))
text_label = Label(splash_screen, image=splash_image, text='Loading...', compound='center', cursor = "watch", fg='white', font=('Helvetica',90,'bold'))
text_label.focus_set()
text_label.pack()
splash_screen.update()

print 'Downloading Updates...'
if is_internet_on():
	download_json()
else:
	print 'Download Failed, lack of Internet Connection'

print 'loading...'
json_file = 'JSON Files/AllSets-x.json'
mtg_object = Magic(json_file)
#time.sleep(5)
print 'DONE!'
splash_screen.destroy()

root.deiconify()
###################################################

menubar = create_menu(root)
root.config(menu = menubar)
search_frame = Frame(root)
search_frame.grid(row=0, column=0)

#See if I can do optionMenus
def update_options(*args):
	cards = sorted(mtg_object.data[edition_variable.get()].data.keys())
	card_variable.set(cards[0])
	menu = card_option_menu['menu']
	menu.delete(0, 'end')
	for card in cards:
		menu.add_command(label = card, command=lambda card=card: card_variable.set(card))


edition_options = sorted(mtg_object.data.keys())

edition_variable = StringVar()
card_variable = StringVar()
edition_variable.trace('w', update_options)
edition_option_menu = OptionMenu(search_frame, edition_variable, *edition_options)
card_option_menu = OptionMenu(search_frame, card_variable, '')
edition_variable.set(edition_options[0])
edition_option_menu.grid(row=0, column=0)
card_option_menu.grid(row=0, column=1)



#card_name = StringVar()
#
#card_name_entry = Entry(root, textvariable=card_name)
#card_name_entry.focus()
#card_name_entry.pack()

enter_button = Button(search_frame, text='Enter', command=change_image)
enter_button.grid(row=0, column=2)

root.bind('<Return>', change_image)

#Create a frame to place the card image in
image_frame = Frame(root, width = img_wt, height = img_ht)
image_frame.grid(row=2,column=0)

if is_internet_on():
	tk_image = get_image('Limited Edition Alpha', 'Black Lotus', img_wt, img_ht)
	card_image = Label(image_frame, image=tk_image)

	#Places the image in the frame
	card_image.place(relx=0.5, rely=0.5, anchor=CENTER)
else:
	no_internet = Label(root, text = 'No Internet!')
	no_internet.pack()

price_frame = Frame(root)
price_frame.grid(row=1, column=0)

high_label = Label(price_frame, text='TCG Price High')
medium_label = Label(price_frame, text='TCG Price Medium')
low_label = Label(price_frame, text='TCG Price Low')

high_price = Label(price_frame, text='N/A')
medium_price = Label(price_frame, text='N/A')
low_price = Label(price_frame, text='N/A')


high_label.grid(row=0, column=0)
medium_label.grid(row=1, column=0)
low_label.grid(row=2, column=0)

high_price.grid(row=0, column=1)
medium_price.grid(row=1, column=1)
low_price.grid(row=2, column=1)

#Sets the minimum size of the window to exactly fit all widgets
root.update()
winWt = root.winfo_width()
winHt = root.winfo_height()
winXPos = (scrnWt / 2) - (winWt / 2)
winYPos = (scrnHt / 2) - (winHt / 2)
root.geometry('+%d+%d' % (winXPos, winYPos))
root.minsize(winWt, winHt)

root.mainloop()