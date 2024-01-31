import frontend.colors as Colors
import customtkinter as ctk

class ToggleButton(ctk.CTkButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.on = False
        self.command = kwargs['command']
        self._command = self.btn_clicked

    def btn_clicked(self):
        if self._state == 'normal':
            self.toggle()
            if self.on:
                self.command()

    def enable(self):
        self.configure(False, state = 'normal')
    
    def disable(self):
        self.configure(False, state = 'disabled')

    def toggle(self):
        self.on = not self.on

        if self.on:
            self.configure(True, fg_color=Colors.BUTTON_HIGHTLIGHT)
        else:
            self.configure(True, fg_color=Colors.BUTTON_NORMAL)
