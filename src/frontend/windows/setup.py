import customtkinter as ctk

from frontend.windows.window import WindowFrame

class SetupFrame(WindowFrame):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        label = ctk.CTkLabel(self, text="Setup")
        label.pack()