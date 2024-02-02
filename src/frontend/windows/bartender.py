import random

import customtkinter as ctk

from backend.bar import Recipe
from backend.barista import Recipes

from frontend.fonts import Fonts
from frontend.windows.window import WindowFrame
from frontend.components import Button
import frontend.colors as Colors

from hal.system import System

class BartenderFrame(WindowFrame):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.frm_pour = PourFrame(master=self, fg_color=self._fg_color)
        self.frm_pour.grid(row=0, column=0, sticky='nsew')

        self.frm_display = DisplayFrame(master=self, fg_color=self._fg_color)
        self.frm_display.grid(row=0, column=0, sticky='nsew')

        self.show_display_frame()
        self.phrases = [
            "Whipping up a $!",
            "Here comes the $!",
            "Pouring a $ now :)",
            "Making a $ special, just for you!"
        ]

    def show_pour_frame(self, recipe: 'Recipe'):
        self.frm_display.grid_remove()
        
        self.frm_pour.grid()
        self.frm_pour.tkraise()

        self.frm_pour.update(random.choice(self.phrases).replace("$", recipe.name), 0)
        self.after(50, self.update_pour_status)
        System.instance().pour(recipe)
    
    def update_pour_status(self):
        self.frm_pour.update(progress=System.instance().pour_progress)
        self.after(50, self.update_pour_status)

        if System.instance().pour_progress > 0.99:
            self.show_display_frame()

    def show_display_frame(self):
        self.frm_pour.grid_remove()

        self.frm_display.grid()
        self.frm_display.tkraise()
    
    def on_pour_abort(self):
        self.show_display_frame()

class PourFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)

        self.title = ctk.CTkLabel(self, text="Title", font=Fonts.instance().get("title"))
        self.title.grid(row=1, column=1, sticky='ew', pady=(0,8))

        self.progressbar = ctk.CTkProgressBar(self, mode="determinate")
        self.progressbar.grid(row=2, column=1, sticky='ew', pady=(0, 64))

        self.btn_abort = ctk.CTkButton(
            self, 
            text="Cancel", 
            font=Fonts.instance().get("title"), 
            width=156, 
            height=92,
            fg_color=Colors.BUTTON_RED,
            corner_radius=0,
            command=self.master.on_pour_abort
            )
        self.btn_abort.grid(row=3, column=1)

    def update(self, title = None, progress = None):
        if title is not None:
            self.title.configure(True, text=title)

        if progress is not None:
            self.progressbar.set(progress)

class DisplayFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

        self.btn_left = Button(
            master = self, 
            text = "←", 
            command = self.btn_left_clicked, 
            fg_color = Colors.BUTTON_GRAY, 
            corner_radius=8
            )
        self.btn_left.grid(row=1, column=0, sticky='w')
        self.btn_left.configure(True, width=128, height=128, corner_radius=8)

        self.frm_summary = SummaryFrame(master=self, fg_color=self._fg_color)
        self.frm_summary.grid(row=0, column=1, rowspan=3, sticky='nsew')

        self.btn_right = Button(
            master = self, 
            text = "→", 
            command = self.btn_right_clicked, 
            fg_color = Colors.BUTTON_GRAY
            )
        self.btn_right.grid(row=1, column=2, sticky='e')
        self.btn_right.configure(True, width=128, height=128, corner_radius=8)

        self.recipe_index = 0
        self.frm_summary.load(self.recipe_index)

    def btn_left_clicked(self):
        if self.recipe_index > 0:
            self.recipe_index -= 1
        else:
            self.recipe_index = len(Recipes.instance()) - 1

        self.frm_summary.load(self.recipe_index)

    def btn_right_clicked(self):
        if self.recipe_index < len(Recipes.instance()) - 1:
            self.recipe_index += 1
        else:
            self.recipe_index = 0

        self.frm_summary.load(self.recipe_index)

class SummaryFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=1)

        self.title = ctk.CTkLabel(self, text="Title", font=Fonts.instance().get("title"))
        self.title.grid(row=1, column=0, sticky='ew', pady=(0,8))

        self.description = ctk.CTkLabel(self, text="Description", font=Fonts.instance().get("body"))
        self.description.grid(row=2, column=0, sticky='new', pady=(0,8))

        self.btn_pour = ctk.CTkButton(
            self, 
            text="Pour", 
            font=Fonts.instance().get("title"), 
            width=156, 
            height=92,
            fg_color=Colors.BUTTON_GREEN,
            corner_radius=0,
            command=self.on_pour_clicked
            )
        self.btn_pour.grid(row=3, column=0, sticky='n')

        self.recipe = None

    def on_pour_clicked(self):
        self.master.master.show_pour_frame(self.recipe)

    def load(self, index: int):
        recipe = Recipes.instance()[index]

        if recipe is not None:
            self.recipe = recipe
            self.title.configure(True, text=recipe.name)
            
            if len(recipe.steps) > 0:
                summary = f"{len(recipe.steps)} Steps ({recipe.volume()} mL)\n\n"
                for step in recipe.steps:
                    summary += str(step) + "\n"

                if not System.instance().can_pour(recipe):   
                    self.btn_pour.configure(state="disabled")
                    
                    summary += "\nMissing: "
                    summary += ', '.join(str(bev) for bev in System.instance().get_missing(recipe))
                else:
                    self.btn_pour.configure(state="enabled")
                    
                self.description.configure(True, text=summary)
            else:
                self.description.configure(True, text="0 Steps")
                self.btn_pour.configure(state="disabled")

        else:
            self.title.configure(text="No Recipes are Loaded")
            self.description.configure(text="Try adding some in the Recipes tab :)")
            self.btn_pour.configure(state='disabled')
