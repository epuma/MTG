try:
	from Tkinter import *
except ImportError:
	from tkinter import *
from PIL import Image, ImageTk

class SplashScreen(Toplevel):
	def __init__(self, root):
		Toplevel.__init__(self)
		pil_image = Image.open('UI/SplashScreen.jpg')
		w,h = pil_image.size
		pil_image = pil_image.resize((w/2, h/2), Image.ANTIALIAS)
		splash_image = ImageTk.PhotoImage(pil_image)

		self.overrideredirect(1)
		self.attributes('-topmost', 1)

		scrnWt = root.winfo_screenwidth()
		scrnHt = root.winfo_screenheight()

		imgXPos = (scrnWt / 2) - (w / 4)
		imgYPos = (scrnHt / 2) - (h / 4)

		self.geometry('+%d+%d' % (imgXPos, imgYPos))
		splash_label = Label(self, image=splash_image, text='Loading...', compound='center', cursor = "watch", fg='white', font=('Helvetica',90,'bold'))
		splash_label.focus_set()
		splash_label.pack()

		self.update()