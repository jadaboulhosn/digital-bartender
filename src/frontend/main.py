import os
import sys
sys.path.insert(0, './')
import customtkinter as ctk
import logging

from frontend.toolbar import ToolbarFrame
from frontend.windows.input import InputFrame
from frontend.settings import Settings
from frontend.fonts import Fonts

from frontend.windows.bartender import BartenderFrame
from frontend.windows.recipes import RecipesFrame
from frontend.windows.setup import SetupFrame

from shared.singleton import Singleton

from backend.util import get_hostname

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        #self.withdraw()
    
        self.register_fonts()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (Settings.instance().width / 2)
        y = (screen_height / 2) - (Settings.instance().height / 2)
        self.geometry('%dx%d+%d+%d' % (Settings.instance().width, Settings.instance().height, x, y))
        self.minsize(Settings.instance().width, Settings.instance().height)

        self.rowconfigure(0, weight=85)
        self.rowconfigure(1, weight=15)
        self.columnconfigure(0, weight=1)

        self.resizable(False, False)

        self.windows = [
            SetupFrame("Setup", master=self, fg_color=self._fg_color),
            BartenderFrame("Bartender", master=self, fg_color=self._fg_color),
            RecipesFrame("Recipes", master=self, fg_color=self._fg_color)
        ]

        for window in self.windows:
            window.grid(row=0, column=0, sticky='nsew', pady=(8, 8), padx=(8, 8))

        self.toolbar = ToolbarFrame(
            windows=self.windows, 
            state_changed=self.toolbar_changed, 
            default=2, 
            master=self
            )
        self.toolbar.grid(row=1, column=0, sticky='nsew', pady=(0, 0))

        self.keyboard = InputFrame(master=self, fg_color=self._fg_color)
        self.keyboard.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.hide_keyboard()

        self.wm_title("digitender")
        #self.deiconify()

    def show_keyboard(self, on_submit, on_cancel, text=""):
        for window in self.windows:
            window.grid_remove()
        
        self.toolbar.grid_remove()

        self.keyboard.grid()

        self.keyboard.setup(
            lambda text: [self.hide_keyboard(), on_submit(text)], 
            lambda: [self.hide_keyboard(), on_cancel()],
            text
            )
    
    def hide_keyboard(self):
        for window in self.windows:
            window.grid()
        
        self.toolbar.grid()

        self.keyboard.grid_remove()

    def register_fonts(self):
        Fonts.instance().add("button", ctk.CTkFont(family="Stencil Std", size=30, weight="bold"))
        Fonts.instance().add("textfield", ctk.CTkFont(family="Stencil Std", size=24, weight="bold"))
        
    def toolbar_changed(self, window):
        window.tkraise()

if __name__ == "__main__":
    if get_hostname() == "digitender":
        os.environ["DISPLAY"] = ':0' 
    else:
        os.environ["DISPLAY"] = ''

    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    ctk.set_appearance_mode('dark')

    app = App()
    app.mainloop()