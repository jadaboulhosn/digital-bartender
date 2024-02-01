import customtkinter as ctk

from frontend.components import Button, ToggleToolbarButton
from frontend.fonts import Fonts
import frontend.colors as Colors

class InputFrame(ctk.CTkFrame):
    def __init__(self, numeric_only=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caps_lock = False
        self.shift = False
        self.on_submit = None
        self.on_cancel = None
        self.numeric_only = numeric_only

        self.configure(fg_color=Colors.BUTTON_GRAY)

        # Define special key symbols
        self.shift_key = "⇧"
        self.caps_lock_key = "⇪"
        self.backspace_key = "⌫"
        
        # Define the keyboard layout
        self.keys = [
                ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
                ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                [self.caps_lock_key, 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
                [self.shift_key, 'z', 'x', 'c', 'v', 'b', 'n', 'm', self.backspace_key],
                ['Space']
            ]

        self.buttons = {}
     
        # Create the keyboard buttons
        for r, row in enumerate(self.keys):
            self.rowconfigure(r + 1, weight = 1)
            for c, key in enumerate(row):
                self.columnconfigure(c, weight = 1)
                
                fn = lambda k=key: self.on_key_press(k)

                btn = None
                if key == self.shift_key or key == self.caps_lock_key:
                    btn = ToggleToolbarButton(
                        master=self, 
                        text=key, 
                        command=fn,
                        fg_color=Colors.BUTTON_GRAY
                        )
                else:    
                    btn = Button(
                        master=self, 
                        text=key, 
                        command=fn,
                        fg_color=Colors.BUTTON_GRAY
                        )
                
                if numeric_only and not key.isdigit():
                    btn.configure(True, state="disabled")
                else:
                    btn.configure(True, state="enabled")

                if key == self.backspace_key:
                    btn.configure(True, state="enabled")

                self.buttons[key] = btn

                if key == 'Space':
                    btn.grid(row=r+1, column=c, columnspan=10, sticky='nsew')
                elif key == self.backspace_key:
                    btn.grid(row=r+1, column=c, columnspan=2, sticky='nsew')
                else:
                    btn.grid(row=r+1, column=c, sticky='nsew')
   
        self.text = ctk.CTkTextbox(self, wrap='word', height=10, width=40, font=Fonts.instance().get("textfield"))
        self.text.grid(row=0, column=2, columnspan=6, sticky='nsew')

        self.btn_cancel = Button(
            master=self,
            text="Cancel", 
            fg_color=Colors.BUTTON_RED,
            command=lambda: self.on_cancel()
            )
        self.btn_cancel.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.btn_submit = Button(
            master=self, 
            text="Done", 
            fg_color=Colors.BUTTON_GREEN,
            command=self.on_submitted
            )
        self.btn_submit.grid(row=0, column=8, columnspan=2, sticky='nsew')

    def on_submitted(self):
        text = self.text.get(1.0, "end-1c")
        if self.numeric_only and len(text) == 0:
            self.on_submit('0')
            return
        
        self.on_submit(text)

    def on_key_press(self, key):
        # Handle key presses
        if key == 'Space':
            self.text.insert(ctk.END, ' ')
        elif key == self.shift_key:
            if self.shift:
                self.buttons[key].untoggle()
                self.shift = False
            else:
                self.shift = True
        elif key == self.caps_lock_key:
            if self.caps_lock:
                self.buttons[key].untoggle()
                self.caps_lock = False
            else:
                self.caps_lock = True
        elif key == self.backspace_key:
            self.text.delete(index1='end-2c', index2='end-1c')
        else:
            if key.isalpha():
                if self.caps_lock or self.shift:
                    key = key.upper()
                if self.shift:
                    self.shift = False
                    self.buttons[self.shift_key].untoggle()
            self.text.insert(ctk.END, key)

    def setup(self, on_submit, on_cancel, text):
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        self.text.delete('1.0', 'end')
        self.text.insert('1.0', text)