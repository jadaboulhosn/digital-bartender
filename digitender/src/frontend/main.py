import sys
sys.path.insert(0, './')
import customtkinter as ctk

from frontend.toolbar import ToolbarFrame
from frontend.settings import Settings

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.withdraw()
    
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (Settings.instance().width / 2)
        y = (screen_height / 2) - (Settings.instance().height / 2)
        self.geometry('%dx%d+%d+%d' % (Settings.instance().width, Settings.instance().height, x, y))
        self.minsize(Settings.instance().width, Settings.instance().height)

        self.rowconfigure(0, weight = 8)
        self.rowconfigure(1, weight = 2)
        self.columnconfigure(0, weight = 1)

        self.toolbar = ToolbarFrame(self)
        self.toolbar.grid(row = 1, column = 0)

        self.wm_title("digitender")
        self.deiconify()

    
if __name__ == "__main__":
    if sys.platform == "linux" or sys.platform == "linux2":
        os.environ["DISPLAY"] = ':0' 

    ctk.set_appearance_mode('dark')
    app = App()
    app.mainloop()