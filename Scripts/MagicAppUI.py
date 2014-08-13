from Tkinter import *
from Menu import createMenu

root = Tk()
root.wm_title("Eric's Magic App")
#root.wm_iconbitmap('mtgicon.ico')

menubar = createMenu(root)
root.config(menu = menubar)

#Create a frame to place the card image in
image_frame = Frame(root, width = 240, height = 340)
image_frame.pack_propagate(0)
image_frame.pack(anchor = W)

#Creating the Image Label, will move this out later
from PIL import Image, ImageTk
from urllib2 import urlopen
import io

def get_image(name):
	url = 'http://mtgimage.com/card/' + name + '.jpg'
	image_bytes = urlopen(url).read()
	data_stream = io.BytesIO(image_bytes)
	pil_image = Image.open(data_stream)
	pil_image = pil_image.resize((240, 340), Image.ANTIALIAS)
	tk_image = ImageTk.PhotoImage(pil_image)
	return tk_image

def change_image(event=None):
	global tk_image
	tk_image = get_image(card_name.get())
	card_image.config(image=tk_image)


card_name = StringVar()
card_name.set('Card Name Here')

card_name_entry = Entry(root, textvariable=card_name)
card_name_entry.pack()

enter_button = Button(root, text='Enter', command=change_image)
enter_button.pack()

root.bind('<Return>', change_image)

tk_image = get_image('Black Lotus')
card_image = Label(image_frame, image=tk_image)






#Places the image in the frame
card_image.place(relx=0.5, rely=0.5, anchor=CENTER)

#This makes the window appear on the top
root.call('wm', 'attributes', '.', '-topmost', '1')
root.mainloop()