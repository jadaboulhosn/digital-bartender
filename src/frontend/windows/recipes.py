import customtkinter as ctk

import logging

import frontend.colors as Colors
from frontend.components import Button, ToggleListButton, UpDownFrame, AddEditDeleteFrame, ScrollableFrame, CloseHeader
from frontend.fonts import Fonts
from frontend.windows.window import WindowFrame

from backend.bar import Type, Beverage, Step, Recipe
from backend.barista import Types, Beverages, Recipes

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
            fg_color = Colors.BUTTON_GRAY,
            corner_radius=8
            )
        self.btn_left.grid(row=1, column=0, sticky='w')
        self.btn_left.configure(True, width=128, height=128)

        self.btn_right = Button(
            master = self, 
            text = "→", 
            command = self.btn_right_clicked, 
            fg_color = Colors.BUTTON_GRAY,
            corner_radius=8
            )
        self.btn_right.grid(row=1, column=2, sticky='e')
        self.btn_right.configure(True, width=128, height=128)

        self.selected_type = None
        self.selected_beverage = None
        self.selected_recipe = None

        self.recipe_frame = RecipeFrame(self.on_recipe_selected, master=self)
        self.beverage_frame = BeverageFrame(self.on_beverage_selected, master=self)
        self.type_frame = TypeFrame(self.on_type_selected, master=self)

        self.recipe_editor = RecipeEditorFrame(self.on_recipe_edit_complete, master=self)
        self.recipe_editor.grid(row=0, column=0, rowspan=3, columnspan=3, sticky='nsew')
        self.recipe_editor.grid_remove()

        self.frames = [self.type_frame, self.beverage_frame, self.recipe_frame]
        for frame in self.frames:
            frame.grid(row=1, column=1, sticky='nsew', padx=8)
        
        self.set_page(0)

    def on_type_selected(self, type: 'Type'):
        self.selected_type = type
        self.beverage_frame.set_selected_type(type)

    def on_beverage_selected(self, beverage: 'Beverage'):
        self.selected_beverage = beverage

    def on_recipe_selected(self, recipe: 'Recipe'):
        self.selected_recipe = recipe

    def show_recipe_editor(self):
        self.recipe_editor.load(self.selected_recipe)
        self.recipe_editor.grid()
        self.recipe_editor.tkraise()
        self.master.toolbar.disable()

    def on_recipe_edit_complete(self):
        self.recipe_editor.grid_remove()
        self.recipe_frame.tkraise()
        self.recipe_frame.load()
        self.master.toolbar.enable()

    def btn_left_clicked(self):
        if self.index > 0:
            self.set_page(self.index - 1)
        
    def btn_right_clicked(self):
        if self.index < len(self.frames) - 1:
            self.set_page(self.index + 1)

    def set_page(self, index):
        self.index = index
        self.frames[index].tkraise()

        if index == 0:
            self.btn_left.configure(True, state='disabled')
        else:
            self.btn_left.configure(True, state='normal')

        if index == len(self.frames) - 1:
            self.btn_right.configure(True, state='disabled')
        else:
            self.btn_right.configure(True, state='normal')

class TypeFrame(ctk.CTkFrame):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.columnconfigure(0, weight = 1)
        self.rowconfigure((0, 1, 3), weight = 0)
        self.rowconfigure(2, weight = 1)

        self.label = ctk.CTkLabel(master=self, text="Beverage Types", font=Fonts.instance().get("title"))
        self.label.grid(row=0, column=0, sticky='ew', pady=(8, 8))

        self.add_edit_delete = AddEditDeleteFrame(
            master=self, 
            on_add=self.btn_add_clicked,
            on_edit=None,
            on_delete=self.btn_delete_clicked
            )
        self.add_edit_delete.grid(row=1, column=0, sticky='ew')

        self.scrollview = ScrollableFrame(master=self, fg_color=self.label._fg_color, callback=callback)
        self.scrollview.grid(row=2, column=0, sticky='nsew')

        self.up_down = UpDownFrame(
            master=self, 
            on_up=self.btn_up_clicked, 
            on_down=self.btn_down_clicked
            )
        self.up_down.grid(row=3, column=0, sticky='ew')

        self.load()

    def load(self):
        self.scrollview.clear()

        for type in Types.instance():
            self.scrollview.append(str(type), type)

    def btn_up_clicked(self):
        self.scrollview.scroll_up()

    def btn_down_clicked(self):
        self.scrollview.scroll_down()

    def btn_delete_clicked(self):
        if self.scrollview.selected_obj is not None:
            if Types.instance().check_references(self.scrollview.selected_obj):
                self.master.master.show_popup(
                    title="Warning", 
                    message="The beverage type you are trying to delete is used by other beverages and recipes.\nYou can still delete this type, but this will automatically delete associated beverages and recipes.\nDo you still want to proceed?", 
                    on_okay=lambda: [Types.instance().remove(self.scrollview.selected_obj), self.load()],
                    on_cancel=lambda: logging.info("User aborted type removal due to recipe collision.")
                )
            else:
                Types.instance().remove(self.scrollview.selected_obj)
                self.load()

    def btn_add_clicked(self):
        self.master.master.show_keyboard(
            lambda text: [Types.instance().append(Type(text)), self.load()],
            lambda: logging.info("No Type added due to user cancellation.")
            )

class BeverageFrame(ctk.CTkFrame):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure((0, 1, 3), weight = 0)
        self.rowconfigure(2, weight = 1)

        self.label = ctk.CTkLabel(master=self, text="Beverages", font=Fonts.instance().get("title"))
        self.label.grid(row=0, column=0, sticky='ew', pady=(8, 8))

        self.add_edit_delete = AddEditDeleteFrame(
            master=self, 
            on_add=self.btn_add_clicked,
            on_edit=None,
            on_delete=self.btn_delete_clicked
            )
        self.add_edit_delete.grid(row=1, column=0, sticky='ew')

        self.scrollview = ScrollableFrame(master=self, fg_color=self.label._fg_color, callback=callback)
        self.scrollview.grid(row=2, column=0, sticky='nsew')

        self.up_down = UpDownFrame(
            master=self, 
            on_up=self.btn_up_clicked, 
            on_down=self.btn_down_clicked
            )
        self.up_down.grid(row=3, column=0, sticky='ew')

        self.load()

        self.selected_type = None

    def load(self):
        self.scrollview.clear()

        for beverage in Beverages.instance():
            self.scrollview.append(str(beverage), beverage)

    def set_selected_type(self, type: 'Type'):
        self.selected_type = type
        self.label.configure(True, text=f"Beverages (Type: {self.selected_type})")

    def btn_up_clicked(self):
        self.scrollview.scroll_up()

    def btn_down_clicked(self):
        self.scrollview.scroll_down()

    def btn_delete_clicked(self):
        if self.scrollview.selected_obj is not None:
            if Beverages.instance().check_references(self.scrollview.selected_obj):
                self.master.master.show_popup(
                    title="Warning", 
                    message="The beverage you are trying to delete is used by other recipes.\nYou can still delete this beverage, but this will automatically delete any associated recipes.\nDo you still want to proceed?", 
                    on_okay=lambda: [Beverages.instance().remove(self.scrollview.selected_obj), self.load()],
                    on_cancel=lambda: logging.info("User aborted beverage removal due to recipe collision."
                    )
                ) 
            else:
                Beverages.instance().remove(self.scrollview.selected_obj)
                self.load()

    def btn_add_clicked(self):
        if len(Types.instance()) > 0:
            self.master.master.show_keyboard(
                lambda text: [Beverages.instance().append(Beverage(text, self.selected_type)), self.load()],
                lambda: logging.info("No Beverage added due to user cancellation.")
                )
        
class RecipeFrame(ctk.CTkFrame):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure((0, 1, 3), weight = 0)
        self.rowconfigure(2, weight = 1)

        self.label = ctk.CTkLabel(master=self, text="Recipes", font=Fonts.instance().get("title"))
        self.label.grid(row=0, column=0, sticky='ew', pady=(8, 8))

        self.add_edit_delete = AddEditDeleteFrame(
            master=self, 
            on_add=self.btn_add_clicked,
            on_edit=self.btn_edit_clicked,
            on_delete=self.btn_delete_clicked
            )
        self.add_edit_delete.grid(row=1, column=0, sticky='ew')

        self.scrollview = ScrollableFrame(master=self, fg_color=self.label._fg_color, callback=callback)
        self.scrollview.grid(row=2, column=0, sticky='nsew')

        self.up_down = UpDownFrame(
            master=self, 
            on_up=self.btn_up_clicked, 
            on_down=self.btn_down_clicked
            )
        self.up_down.grid(row=3, column=0, sticky='ew')

        self.load()

        self.selected_type = None

    def load(self):
        self.scrollview.clear()

        for recipe in Recipes.instance():
            self.scrollview.append(f"{recipe.name} ({len(recipe.steps)} Steps)", recipe)
            
    def btn_up_clicked(self):
        self.scrollview.scroll_up()

    def btn_down_clicked(self):
        self.scrollview.scroll_down()

    def btn_delete_clicked(self):
        if self.scrollview.selected_obj is not None:
            Recipes.instance().remove(self.scrollview.selected_obj)
            self.load()
            
    def btn_edit_clicked(self):
        if self.scrollview.selected_obj is not None:
            self.master.show_recipe_editor()

    def btn_add_clicked(self):
        self.master.master.show_keyboard(
            lambda text: [Recipes.instance().append(Recipe(text)), self.load(), self.master.on_recipe_selected(Recipes.instance()[len(Recipes.instance())-1]), self.master.show_recipe_editor()],
            lambda: logging.info("No Recipe added due to user cancellation.")
            )
        
class RecipeEditorFrame(ctk.CTkFrame):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=0)

        self.configure(True, fg_color=self.master._fg_color)

        self.beverage_label = ctk.CTkLabel(master=self, text="Beverages", font=Fonts.instance().get("title"))
        self.beverage_label.grid(row=0, column=0, padx=(0, 4), sticky='ew')

        self.beverage_up_down = UpDownFrame(
            master=self, 
            on_up=self.btn_bev_up_clicked, 
            on_down=self.btn_bev_down_clicked
            )
        self.beverage_up_down.grid(row=1, column=0, sticky='ew')

        self.beverage_view = ScrollableFrame(
            master=self, 
            fg_color=self.beverage_label._fg_color, 
            callback=self.on_beverage_selected,
            font=Fonts.instance().get("title"),
            invert_colors=True
            )
        self.beverage_view.grid(
            row=2, 
            column=0, 
            padx=(0, 4),
            sticky='nsew')

        self.add_button = Button(master=self, text='+', command=self.on_add_beverage, fg_color=Colors.BUTTON_GRAY)
        self.add_button.grid(row=3, column=0, padx=(0, 4),sticky='ew')
        
        self.step_header = CloseHeader(text="Steps", on_close=self.master.on_recipe_edit_complete, master=self)
        self.step_header.grid(row=0, column=1, padx=(4, 0), sticky='ew')

        self.step_up_down = UpDownFrame(
            master=self, 
            on_up=self.btn_step_up_clicked, 
            on_down=self.btn_step_down_clicked
            )
        self.step_up_down.grid(row=1, column=1, sticky='ew')

        self.step_view = ScrollableFrame(
            master=self, 
            fg_color=self.beverage_label._fg_color, 
            callback=self.on_step_selected,
            font=Fonts.instance().get("title"),
            invert_colors=True
            )
        self.step_view.grid(
            row=2, 
            column=1,
            padx=(4, 0), 
            sticky='nsew')

        self.edit_delete_frame = AddEditDeleteFrame(
            on_add=None,
            on_edit=self.on_step_edited,
            on_delete=self.on_step_deleted,
            master=self
        )
        self.edit_delete_frame.grid(
            row=3,
            column=1,
            padx=(4, 0),
            sticky='ew'
        )

        self.selected_beverage = None
        self.recipe = None

    def load(self, recipe: 'Recipe'):
        self.beverage_view.clear()
        for beverage in Beverages.instance():
            self.beverage_view.append(str(beverage), beverage)

        self.step_view.clear()
        for step in recipe.steps:
            self.step_view.append(str(step), step)

        self.recipe = recipe
     
    def btn_bev_up_clicked(self):
        self.beverage_view.scroll_up()

    def btn_bev_down_clicked(self):
        self.beverage_view.scroll_down()

    def btn_step_up_clicked(self):
        self.step_view.scroll_up()

    def btn_step_down_clicked(self):
        self.step_view.scroll_down()

    def on_beverage_selected(self, beverage: 'Beverage'):
        self.selected_beverage = beverage
    
    def on_step_selected(self, step: 'Step'):
        self.selected_step = step

    def on_step_edited(self):
        self.master.master.show_keyboard(
            lambda text: [self.selected_step.set_volume(max(int(text), 1)), self.load(self.recipe)],
            lambda: logging.info("Ignoring volume modification."),
            text=str(self.selected_step.volume),
            use_numeric=True
        )

    def on_step_deleted(self):
        self.recipe.steps.remove(self.selected_step)

        self.load(self.recipe)

    def on_add_beverage(self):
        self.recipe.steps.append(Step(self.selected_beverage, 44))
        
        self.load(self.recipe)