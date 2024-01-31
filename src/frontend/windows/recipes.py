import customtkinter as ctk

import frontend.colors as Colors
from frontend.components import Button
from frontend.windows.window import WindowFrame

class RecipesFrame(WindowFrame):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        self.columnconfigure(0, weight = 0)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 0)

        self.rowconfigure(0, weight = 0)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 0)

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
        self.btn_right.configure(True, width=128, height=128)

        self.frames = [
            TypeFrame(master=self),
            BeverageFrame(master=self),
            RecipeFrame(master=self)
        ]
        for frame in self.frames:
            frame.grid(row=1, column=1, sticky='nsew')
        
        self.set_page(0)

    def btn_left_clicked(self):
        if self.index > 0:
            self.set_page(self.index - 1)
        else:
            self.set_page(len(self.frames) - 1)
        
    def btn_right_clicked(self):
        if self.index < len(self.frames) - 1:
            self.set_page(self.index + 1)
            self.master.show_keyboard(lambda text: print("Keys" + text), lambda: print("cancel"), 'test')
        else:
            self.set_page(0)

    def set_page(self, index):
        self.index = index
        self.frames[index].tkraise()

class TypeFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class BeverageFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class RecipeFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)