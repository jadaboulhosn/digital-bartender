import frontend.colors as Colors
from frontend.fonts import Fonts
import customtkinter as ctk

class Button(ctk.CTkButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  

        self.configure(True, font=Fonts.instance().get("button"), corner_radius=0)

class ToggleButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.default_color = self._fg_color
        self.on = False
        self.command = kwargs['command']
        self._command = self.btn_clicked

    def btn_clicked(self):
        if not self.on:
            self.configure(True, fg_color=Colors.BUTTON_HIGHTLIGHT)
            self.command()

    def untoggle(self):
        self.configure(True, fg_color=self.default_color)

    def enable(self):
        self.configure(False, state = 'normal')
    
    def disable(self):
        self.configure(False, state = 'disabled')