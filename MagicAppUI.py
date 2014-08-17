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

scrnWt = root.winfo_screenwidth()
scrnHt = root.winfo_screenheight()
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
print 'DONE!'
splash_screen.destroy()

root.deiconify()
###################################################



menubar = createMenu(root)
root.config(menu = menubar)

#Create a frame to place the card image in
image_frame = Frame(root, width = 240, height = 340)
image_frame.pack()

card_name = StringVar()

card_name_entry = Entry(root, textvariable=card_name)
card_name_entry.focus()
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