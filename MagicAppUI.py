try:
	from Tkinter import *
except ImportError:
	from tkinter import *

from Menu import createMenu
import urllib2

root = Tk()
root.wm_title("Eric's Magic App")
#root.wm_iconbitmap('mtgicon.ico')

menubar = createMenu(root)
root.config(menu = menubar)

def internet_on():
    try:
        response=urllib2.urlopen('http://74.125.228.100',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

if internet_on():
	#Create a frame to place the card image in
	image_frame = Frame(root, width = 240, height = 340)
	image_frame.pack()

	#Creating the Image Label, will move this out later
	from PIL import Image, ImageTk
	import io

	def get_image(name):
		try:
			url = 'http://mtgimage.com/card/' + name + '.jpg'
			image_bytes = urllib2.urlopen(url).read()
			data_stream = io.BytesIO(image_bytes)
			pil_image = Image.open(data_stream)
			w,h = pil_image.size
			pil_image = pil_image.resize((240, 340), Image.ANTIALIAS)
			tk_image = ImageTk.PhotoImage(pil_image)
		except:
			tk_image = 'Card not found'
		return tk_image

	def change_image(event=None):
		global tk_image
		tk_image = get_image(card_name.get())
		if isinstance(tk_image, basestring):
			card_image.config(image="", text=tk_image)
		else:
			card_image.config(image=tk_image)


	card_name = StringVar()
	card_name.set('Black Lotus')

	card_name_entry = Entry(root, textvariable=card_name)
	card_name_entry.pack()

	enter_button = Button(root, text='Enter', command=change_image)
	enter_button.pack()

	root.bind('<Return>', change_image)

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