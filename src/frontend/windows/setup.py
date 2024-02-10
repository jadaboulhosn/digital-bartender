import customtkinter as ctk

from backend.bar import Beverage
from backend.barista import Beverages

from hal.system import System
from hal.pump import Pump

import frontend.colors as Colors
from frontend.settings import Settings
from frontend.fonts import Fonts
from frontend.windows.window import WindowFrame
from frontend.components import ScrollableFrame, UpDownFrame, Button

class SetupFrame(WindowFrame):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        self.btn_left = Button(
            master = self, 
            text = "←", 
            command = self.scroll_left, 
            fg_color = Colors.BUTTON_GRAY, 
            corner_radius=8
            )
        self.btn_left.grid(row=1, column=0, sticky='w')
        self.btn_left.configure(True, width=64, height=64, corner_radius=8)

        self.scrollarea = ctk.CTkScrollableFrame(self, orientation='horizontal', fg_color=self._fg_color)
        self.scrollarea.grid(row=0, column=1, rowspan=3, sticky='nsew')
        self.scrollarea._scrollbar.grid_forget()

        self.btn_right = Button(
            master = self, 
            text = "→", 
            command = self.scroll_right, 
            fg_color = Colors.BUTTON_GRAY
            )
        self.btn_right.grid(row=1, column=2, sticky='e')
        self.btn_right.configure(True, width=64, height=64, corner_radius=8)

        index = 0
        for pump in System.instance().data:
            self.scrollarea.columnconfigure(index, weight=0)
            frame = PumpFrame(pump, master=self.scrollarea, fg_color=self._fg_color)
            frame.grid(row=0, column=index, padx=(4, 4), sticky='ns')
            index += 1
    
    def scroll_left(self):
        self.scrollarea._parent_canvas.xview("scroll", -100, "units")

    def scroll_right(self):
        self.scrollarea._parent_canvas.xview("scroll", 100, "units")

class PumpFrame(ctk.CTkFrame):
    def __init__(self, pump: 'Pump', **kwargs):
        super().__init__(**kwargs)

        self.ignore_initial_set = True

        self.pump = pump

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            self, 
            fg_color=self.master.master.master._fg_color, 
            text=pump.name, 
            font=Fonts.instance().get("title")
            )
        self.title.grid(row=0, column=0, sticky='ew')

        self.scrollview = ScrollableFrame(
            master=self, 
            fg_color=self.title._fg_color, 
            callback=self.on_beverage_selected,
            font=Fonts.instance().get("body")
            )
        self.scrollview.grid(row=1, column=0, sticky='nsew')

        self.up_down = UpDownFrame(
            master=self, 
            on_up=self.btn_up_clicked, 
            on_down=self.btn_down_clicked
            )
        self.up_down.grid(row=2, column=0, sticky='ew')

        self.btn_pour = ctk.CTkButton(
            self, 
            text="Purge", 
            font=Fonts.instance().get("title"), 
            fg_color=Colors.BUTTON_GREEN,
            hover_color=Colors.BUTTON_GREEN,
            corner_radius=0,
            border_width=0,
            height=92,
            command=self.on_pour_clicked
            )
        self.btn_pour.grid(row=3, column=0, sticky='nsew')

        self.btn_abort = ctk.CTkButton(
            self, 
            text="Stop", 
            font=Fonts.instance().get("title"), 
            fg_color=Colors.BUTTON_RED,
            hover_color=Colors.BUTTON_RED,
            corner_radius=0,
            border_width=0,
            height=92,
            command=self.on_abort_clicked
            )
        self.btn_abort.grid(row=3, column=0, sticky='nsew')
        self.btn_abort.grid_remove()

        self.load()

    def load(self):
        self.scrollview.clear()

        select = None
        for beverage in Beverages.instance():
            self.scrollview.append(str(beverage), beverage)
            
            if self.pump.id != -1:
                if hash(beverage) == self.pump.id:
                    select = str(beverage)
        
        if select is not None:
            self.scrollview.select_item(select)

    def btn_up_clicked(self):
        self.scrollview.scroll_up()

    def btn_down_clicked(self):
        self.scrollview.scroll_down()

    def on_beverage_selected(self, beverage: 'Beverage'):
        if self.ignore_initial_set:
            self.ignore_initial_set = False
        else:
            self.pump.id = hash(beverage)

    def on_pour_clicked(self):
        self.btn_abort.grid()
        self.btn_pour.grid_remove()
        
        self.pump.activate()

    def on_abort_clicked(self):
        self.btn_pour.grid()
        self.btn_abort.grid_remove()

        self.pump.deactivate()