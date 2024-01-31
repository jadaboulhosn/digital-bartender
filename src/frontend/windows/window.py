import customtkinter as ctk

class WindowFrame(ctk.CTkFrame):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name