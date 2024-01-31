import customtkinter as ctk

from frontend.components import ToggleButton

class ToolbarFrame(ctk.CTkFrame):
    def __init__(self, windows: list, state_changed, default: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
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

            self.buttons[window] = ToggleButton(
                master=self, 
                command=lambda window=window: state_click(window), 
                text=window.name
                )
            self.buttons[window].grid(row=0, column=i, sticky="nsew")

        self.buttons[self.windows[default]].invoke()

    def enable(self):
        for _, button in self.buttons.items():
            button.enable()

    def disable(self):
        for _, button in self.buttons.items():
            button.disable()

    def get_state(self) -> str:
        return self.window