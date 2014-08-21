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
	if tk_image is None:
		card_image.config(image="", text='Card not Found')
		high_price.config(text='N/A')
		medium_price.config(text='N/A')
		low_price.config(text='N/A')
	else:
		card_image.config(image=tk_image)
		update_prices(card, edition)
		update_info(card, edition)

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

#forces Python to the front
os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

#####################################################
#Splash Screen
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
splash_label = Label(splash_screen, image=splash_image, text='Loading...', compound='center', cursor = "watch", fg='white', font=('Helvetica',90,'bold'))
splash_label.focus_set()
splash_label.pack()
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
#Initiate Menu
menubar = create_menu(root)
root.config(menu = menubar)

#Search Frame with Option Menus and Enter Button
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


#Create Image Frame to place the card image in
image_frame = Frame(root, width = img_wt, height = img_ht)
image_frame.grid(row=2,column=0, padx=10, pady=10, sticky=N)

if is_internet_on():
	tk_image = get_image('Limited Edition Alpha', 'Black Lotus', img_wt, img_ht)
	card_image = Label(image_frame, image=tk_image)

	#Places the image in the frame
	card_image.place(relx=0.5, rely=0.5, anchor=CENTER)
else:
	no_internet = Label(image_frame, text = 'No Internet!')
	no_internet.pack()

#Price Frame to fit Labels
price_frame = Frame(root)
price_frame.grid(row=1, column=0)

high_label = Label(price_frame, text='TCG Price High')
medium_label = Label(price_frame, text='TCG Price Medium')
low_label = Label(price_frame, text='TCG Price Low')

high_price = Label(price_frame, text='N/A')
medium_price = Label(price_frame, text='N/A')
low_price = Label(price_frame, text='N/A')


high_label.grid(row=0, column=0, sticky=W)
medium_label.grid(row=1, column=0, sticky=W)
low_label.grid(row=2, column=0, sticky=W)

high_price.grid(row=0, column=1, sticky=E)
medium_price.grid(row=1, column=1, sticky=E)
low_price.grid(row=2, column=1, sticky=E)

#############################################################################
#Frame for Card Information

scroll_frame = Frame(root, width = img_wt, height = img_ht)
scroll_frame.grid(row=2, column=1, padx=10, pady=10, sticky=N)

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

def scroll_function(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=img_wt,height=img_ht)

#scrollbar!
canvas = Canvas(scroll_frame)
info_frame = Frame(canvas)
info_scrollbar = AutoScrollbar(scroll_frame)
info_scrollbar.config(command=canvas.yview)
canvas.configure(yscrollcommand=info_scrollbar.set)

info_scrollbar.grid(row=0, column=1, sticky=N+S)
canvas.grid(row=0, column=0)
canvas.create_window((0,0), window=info_frame, anchor='nw')
info_frame.bind("<Configure>", scroll_function)



default_edition = 'Limited Edition Alpha'
default_card = 'Black Lotus'

info_attributes = [
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

info_attribute_labels = [
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].name),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].manaCost),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].type),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].rarity),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].text),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].flavor),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].power),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].toughness),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].loyalty),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].printings),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].artist),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].number),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].multiverseid),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].border),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].timeshifted),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].hand),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].life),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].rulings),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].legalities),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].originalText),
			   Label(info_frame, text = mtg_object.data[default_edition].data[default_card].originalType)
			   ]



info_labels = [
			   Label(info_frame, text = 'Name:'),
			   Label(info_frame, text = 'Casting Cost:'),
			   Label(info_frame, text = 'Type:'),
			   Label(info_frame, text = 'Rarity:'),
			   Label(info_frame, text = 'Text:'),
			   Label(info_frame, text = 'Flavor Text:'),
			   Label(info_frame, text = 'Power:'),
			   Label(info_frame, text = 'Toughness:'),
			   Label(info_frame, text = 'Loyalty Counters:'),
			   Label(info_frame, text = 'Set Printings:'),
			   Label(info_frame, text = 'Artist:'),
			   Label(info_frame, text = 'Card Number:'),
			   Label(info_frame, text = 'MultiVerse ID:'),
			   Label(info_frame, text = 'Border Color:'),
			   Label(info_frame, text = 'Timeshifted:'),
			   Label(info_frame, text = 'Max Handsize Modifier (Vanguard):'),
			   Label(info_frame, text = 'Max Life Modifier (Vanguard):'),
			   Label(info_frame, text = 'Rulings:'),
			   Label(info_frame, text = 'Legality:'),
			   Label(info_frame, text = 'Original Text:'),
			   Label(info_frame, text = 'Original Type:')
			   ]

i = 0
for n in range(len(info_attributes)):
	if getattr(mtg_object.data[default_edition].data[default_card], info_attributes[n]) is not None:
		info_labels[n].grid(row=i, column=0, sticky=NW)
		info_attribute_labels[n].config(wraplength=350, justify=LEFT)
		info_attribute_labels[n].grid(row=i, column=1, sticky=W)
		i += 1

def update_info(card, edition):
	print 'Updating Info!'
	i = 0
	for n in range(len(info_attributes)):
		info_labels[n].grid_forget()
		info_attribute_labels[n].grid_forget()

	for n in range(len(info_attributes)):
		if getattr(mtg_object.data[edition].data[card], info_attributes[n]) is not None:
			info_labels[n].grid(row=i, column=0, sticky=NW)
			info_attribute_labels[n].config(text=getattr(mtg_object.data[edition].data[card], info_attributes[n]), wraplength=350, justify=LEFT)
			info_attribute_labels[n].grid(row=i, column=1, sticky=W)
			i += 1


#############################################################################



#Sets the minimum size of the window to exactly fit all widgets
root.update()
winWt = root.winfo_width()
winHt = root.winfo_height()
winXPos = (scrnWt / 2) - (winWt / 2)
winYPos = 0
root.geometry('%dx%d+%d+%d' % (winWt, winHt, winXPos, winYPos))
root.minsize(winWt, winHt)
root.maxsize(winWt, winHt)

root.mainloop()