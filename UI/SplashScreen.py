from tkinter import Toplevel, Label
from PIL import Image, ImageTk


class SplashScreen(Toplevel):
    """Borderless splash shown while the app loads the card database."""

    def __init__(self, root):
        super().__init__()
        pil_image = Image.open('UI/SplashScreen.jpg')
        w, h = pil_image.size
        pil_image = pil_image.resize((w // 2, h // 2), Image.LANCZOS)
        self._splash_image = ImageTk.PhotoImage(pil_image)

        self.overrideredirect(True)
        self.attributes('-topmost', True)

        scrnWt = root.winfo_screenwidth()
        scrnHt = root.winfo_screenheight()
        img_x = (scrnWt // 2) - (w // 4)
        img_y = (scrnHt // 2) - (h // 4)
        self.geometry(f'+{img_x}+{img_y}')

        label = Label(
            self,
            image=self._splash_image,
            text='Loading...',
            compound='center',
            cursor='watch',
            fg='white',
            font=('Helvetica', 90, 'bold'),
        )
        label.pack()
        self.update()
