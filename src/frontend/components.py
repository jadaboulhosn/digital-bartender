import logging
import frontend.colors as Colors
from frontend.fonts import Fonts
import customtkinter as ctk

from frontend.settings import Settings

class PopupFrame(ctk.CTkFrame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=1)
        
        self.title = None
        self.label = None
        self.okay_cancel = None
        
    def show(self, title: str, message: str, on_okay = None, on_cancel = None):
        if self.title is not None:
            self.title.destroy()
        self.title = ctk.CTkLabel(self, text=title, font=Fonts.instance().get("title"), fg_color=self._fg_color)
        self.title.grid(row=1, column=0, pady=(0, 16))
    
        if self.label is not None:
            self.label.destroy()
        self.label = ctk.CTkLabel(self, text=message, font=Fonts.instance().get("body"), fg_color=self._fg_color)
        self.label.grid(row=2, column=0, pady=(0, 8))

        if self.okay_cancel is not None:
            self.okay_cancel.destroy()
        self.okay_cancel = OkayCancelGroup(
            on_okay=lambda: [self.master.hide_popup(), on_okay()], 
            on_cancel=lambda: [self.master.hide_popup(), on_cancel()], 
            master=self,
            fg_color=self._fg_color
            )
        self.okay_cancel.grid(row=3, column=0)

class OkayCancelGroup(ctk.CTkFrame):
    def __init__(self, on_okay, on_cancel = None, **kwargs):
        super().__init__(**kwargs)  

        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=1)

        self.okay_button = Button(master=self, command=on_okay, text="Okay", fg_color=Colors.BUTTON_GRAY)
        self.okay_button.grid(row=0, column=0, sticky='ew')

        if on_cancel is not None:
            self.columnconfigure(1, weight=1)
            self.cancel_button = Button(master=self, command=on_cancel, text="Cancel", fg_color=Colors.BUTTON_GRAY)
            self.cancel_button.grid(row=0, column=1, sticky='ew')

class Button(ctk.CTkButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  

        self.configure(
            True, 
            font=Fonts.instance().get("button"),
            corner_radius=0,
            border_width=0,
            hover_color=self._fg_color
            )

class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, fg_color, callback, font=None, invert_colors=False):
        super().__init__(master=master, fg_color=fg_color)
        
        if font == None:
            self.font = Fonts.instance().get("button")
        else:
            self.font = font

        self.invert_colors = invert_colors
        self.callback = callback
        self._scrollbar.grid_forget()
        self.scrollview_objs = {}
        self.selected_text = ""
        self.selected_obj = None
        self.columnconfigure(0, weight=1)

    def scroll_up(self):
        self._parent_canvas.yview("scroll", -50, "units")

    def scroll_down(self):
        self._parent_canvas.yview("scroll", 50, "units")

    def on_list_item_toggled(self, label):
        for list_label, list_obj in self.scrollview_objs.items():
            if label == list_label:
                list_label.set_selected(True)
                
                self.selected_text = label._text
                self.selected_obj = list_obj

                self.callback(self.selected_obj)
            else:
                list_label.set_selected(False)
    
    def select_item(self, text):
        for list_label, _ in self.scrollview_objs.items():
            if text == list_label._text:
                list_label.set_selected(True)
            else:
                list_label.set_selected(False)

    def append(self, text, obj):
        self.rowconfigure(len(self.scrollview_objs), weight=0)
        label = ToggleListButton(
            master=self, 
            text=text, 
            fg_color=Colors.BUTTON_GRAY,
            font=self.font,
            command=lambda label: self.on_list_item_toggled(label),
            invert_colors=self.invert_colors
        )
        label.grid(row=len(self.scrollview_objs), column=0, padx=(0, 6), sticky='ew')
        self.scrollview_objs[label] = obj

        if len(self.scrollview_objs) == 1:
            self.on_list_item_toggled(label)

    def clear(self):
        for obj in self.scrollview_objs.keys():
            obj.destroy()
        self.scrollview_objs = {}
        self.selected_text = ""
        self.selected_obj = None
    
    def get_selected(self) -> (str, object):
        return self.selected_text, self.selected_obj

class ToggleListButton(ctk.CTkButton):
    def __init__(self, invert_colors=False,**kwargs):
        super().__init__(**kwargs)  

        self.configure(
            True, 
            corner_radius=0,
            border_width=0
            )
        
        if invert_colors:
            self.active_color = Colors.BUTTON_GRAY
            self.inactive_color = Colors.BUTTON_DARK_GRAY
        else:
            self.active_color = Colors.BUTTON_DARK_GRAY
            self.inactive_color = Colors.BUTTON_GRAY

        self.on = False
        self.command = kwargs['command']
        self._command = self.label_clicked
        self.set_selected(False)
        
    def label_clicked(self):
        self.on = True
        self.command(self)

    def set_selected(self, state):
        if state:
            self.configure(True, fg_color=self.active_color, hover_color=self.active_color)
        else:
            self.configure(True, fg_color=self.inactive_color, hover_color=self.inactive_color)

class ToggleToolbarButton(Button):
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
        self.configure(True, state = 'normal')
    
    def disable(self):
        self.configure(True, state = 'disabled')

class UpDownFrame(ctk.CTkFrame):
    def __init__(self, on_up, on_down, **kwargs):
        super().__init__(**kwargs)  

        self.columnconfigure((0, 1), weight = 1)
        self.rowconfigure(0, weight=0)

        self.up_button = Button(master=self, text='▲', command=on_up, fg_color=Colors.BUTTON_GRAY)
        self.up_button.grid(row=0, column=1, sticky='ew')

        self.down_button = Button(master=self, text='▼', command=on_down, fg_color=Colors.BUTTON_GRAY)
        self.down_button.grid(row=0, column=0, sticky='ew')

class AddEditDeleteFrame(ctk.CTkFrame):
    def __init__(self, on_add, on_edit, on_delete, **kwargs):
        super().__init__(**kwargs)  

        col_index = 0
        actions = [on_add, on_edit, on_delete]
        for action in actions:
            if action is not None:
                self.columnconfigure(col_index, weight = 1)
                col_index += 1
        self.rowconfigure(0, weight=0)

        col_index = 0
        if on_add is not None:
            self.add_button = Button(master=self, text='+', command=on_add, fg_color=Colors.BUTTON_GRAY)
            self.add_button.grid(row=0, column=col_index, sticky='ew')
            
            col_index += 1

        if on_edit is not None:
            self.edit_button = Button(master=self, text='✎', command=on_edit, fg_color=Colors.BUTTON_GRAY)
            self.edit_button.grid(row=0, column=col_index, sticky='ew')

            col_index += 1

        if on_delete is not None:
            self.delete_button = Button(master=self, text='🗑', command=on_delete, fg_color=Colors.BUTTON_GRAY)
            self.delete_button.grid(row=0, column=col_index, sticky='ew')

            col_index += 1

class CloseHeader(ctk.CTkFrame):
    def __init__(self, text: str, on_close, **kwargs):
        super().__init__(**kwargs)  
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        self.configure(True, fg_color=self.master._fg_color)

        self.label = ctk.CTkLabel(self, text=text, font=Fonts.instance().get("title"))
        self.label.grid(row=0, column=0, sticky='nsew')

        self.button = ctk.CTkButton(
            self, 
            text='✖', 
            command=on_close, 
            width=32, 
            height=32, 
            fg_color=Colors.BUTTON_GRAY
            )
        self.button.grid(row=0, column=1, sticky='ns')
        
class ToolbarFrame(ctk.CTkFrame):
    def __init__(self, windows: list, state_changed, default: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.state = True

        self.grid_rowconfigure(0, weight=1)

        def state_click(target_window):
            for window, button in self.buttons.items():
                if target_window != window:
                    button.untoggle()
            self.window = target_window
            state_changed(self.window)

        self.buttons = {}    
        self.windows = windows
        for i in range(0, len(self.windows)):
            window = self.windows[i]
            self.grid_columnconfigure(i, weight=1)

            self.buttons[window] = ToggleToolbarButton(
                master=self, 
                command=lambda window=window: state_click(window), 
                text=window.name
                )
            self.buttons[window].grid(row=0, column=i, sticky="nsew")

        self.buttons[self.windows[default]].invoke()

    def enable(self):
        if not self.state:
            for _, button in self.buttons.items():
                button.enable()
            self.state = True

    def disable(self):
        if self.state:
            for _, button in self.buttons.items():
                button.disable()
            self.state = False

    def get_state(self) -> str:
        return self.window