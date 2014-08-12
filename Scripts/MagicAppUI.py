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

card_name = 'Ancestral Recall'
url = 'http://mtgimage.com/card/' + card_name + '.jpg'
try:
	image_bytes = urlopen(url).read()
	data_stream = io.BytesIO(image_bytes)
	pil_image = Image.open(data_stream)
#	w, h = pil_image.size
	pil_image = pil_image.resize((240, 340), Image.ANTIALIAS)
	tk_image = ImageTk.PhotoImage(pil_image)
	card_image = Label(image_frame, image=tk_image)
except:
	card_image = Label(image_frame, text='Error: Card Not Found')

#Places the image in the frame
card_image.place(relx=0.5, rely=0.5, anchor=CENTER)

root.mainloop()