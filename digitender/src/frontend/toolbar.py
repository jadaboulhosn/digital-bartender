import customtkinter as ctk

from frontend.components import ToggleButton

class ToolbarFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)

        self.btn_setup = ToggleButton(master = self, command = self.btn_setup_click, text = "Setup")
        self.btn_setup.grid(row = 0, column = 0, sticky="nsew")

        self.btn_main = ToggleButton(master = self, command = self.btn_main_click, text = "Bartender")
        self.btn_main.grid(row = 0, column = 1, sticky="nsew")

        self.btn_recipes = ToggleButton(master = self, command = self.btn_recipes_click, text = "Recipes")
        self.btn_recipes.grid(row = 0, column = 2, sticky="nsew")

    def btn_main_click(self):
        pass

    def btn_setup_click(self):
        pass

    def btn_recipes_click(self):
        pass