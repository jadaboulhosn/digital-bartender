import customtkinter as ctk

from frontend.windows.window import WindowFrame
from frontend.components import Button
import frontend.colors as Colors

class BartenderFrame(WindowFrame):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        self.btn_left = Button(
            master = self, 
            text = "←", 
            command = self.btn_left_clicked, 
            fg_color = Colors.BUTTON_GRAY
            )
        self.btn_left.grid(row=1, column=0, sticky='w')
        self.btn_left.configure(True, width=128, height=128)

        self.btn_right = Button(
            master = self, 
            text = "→", 
            command = self.btn_right_clicked, 
            fg_color = Colors.BUTTON_GRAY
            )
        self.btn_right.grid(row=1, column=2, sticky='e')
        self.btn_right.configure(True, width=128, height= 128)

        self.frm_pour = PourFrame(master=self)
        self.frm_pour.grid(row=1, column=1, sticky='nsew')

    def btn_left_clicked(self):
        pass

    def btn_right_clicked(self):
        pass

class PourFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class DisplayFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)