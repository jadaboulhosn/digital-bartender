import sys
import inspect
import os
import shutil
import customtkinter
import jsonpickle
import time
import threading

sys.path.append("./lib")
from database import Database
from cookbook import Cookbook
from type import Type
from step import Step
from beverage import Beverage
from recipe import Recipe
from components import OnScreenKeyboard, CustomPanel

if sys.platform == "linux" or sys.platform == "linux2":
    import RPi.GPIO as GPIO
else:
    import gpio as GPIO

COOKBOOK_DB_TEMPLATE="../data/cookbook-template.json"
COOKBOOK_DB_PATH="../data/cookbook.json"
SETTINGS_PATH="../data/settings.json"

class Pump(object):
    def __init__(self, name: str, addr: int, beverage: str):
        self.name = name
        self.addr = addr
        self.beverage = beverage

class Settings(object):
    def __init__(self):
        self.width = 800
        self.height = 480
        self.milliliters_per_second = 5
        self.pumps = [ Pump("Pump", 0, ""), Pump("Pump 2", 1, "") ]

        try:
            self.load_settings()
        except Exception as error:
            print("An error occurred while trying to load the saved settings: \n" + str(error))
            self.save_settings()

    def load_settings(self):
        with open(SETTINGS_PATH, 'r') as file:
            obj = jsonpickle.decode(file.read())
            self.width = obj.width
            self.height = obj.height
            self.pumps = obj.pumps
            self.milliliters_per_second = obj.milliliters_per_second

    def save_settings(self):
        with open(SETTINGS_PATH, 'w') as file:
            file.write(jsonpickle.encode(self))

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.settings = Settings()

        if Cookbook.instance().get_type_count() == 0:
            vodka = Type("Vodka")
            Cookbook.instance().add_type(vodka)    
            gin = Type("Gin")
            Cookbook.instance().add_type(gin)
            whiskey = Type("Whiskey")
            Cookbook.instance().add_type(whiskey)
            tequila = Type("Tequila")
            Cookbook.instance().add_type(tequila)
            mixer = Type("Mixer")
            Cookbook.instance().add_type(mixer)

            johnny = Beverage("Johnny Walker", whiskey)
            Cookbook.instance().add_beverage(johnny)
            sky = Beverage("Sky", vodka)
            Cookbook.instance().add_beverage(sky)
            beef = Beverage("Beefeater", gin)
            Cookbook.instance().add_beverage(beef)
            jose = Beverage("Jose Cuervo", tequila)
            Cookbook.instance().add_beverage(jose)
            tonic = Beverage("Tonic Water", mixer)
            Cookbook.instance().add_beverage(tonic)
            oj = Beverage("Orange Juice", mixer)
            Cookbook.instance().add_beverage(oj)
            redbull = Beverage("Redbull", mixer)
            Cookbook.instance().add_beverage(redbull)

            neat = Recipe("Whiskey Neat")
            neat.add_step(Step(johnny, 50))
            Cookbook.instance().add_recipe(neat)
            vodka_rb = Recipe("Vodka Redbull")
            vodka_rb.add_step(Step(sky, 50))
            vodka_rb.add_step(Step(redbull, 200))
            Cookbook.instance().add_recipe(vodka_rb)
            gin_tonic = Recipe("Gin and Tonic")
            gin_tonic.add_step(Step(beef, 50))
            gin_tonic.add_step(Step(tonic, 200))
            Cookbook.instance().add_recipe(gin_tonic)
            tequila_oj = Recipe("Tequila OJ")
            tequila_oj.add_step(Step(jose, 50))
            tequila_oj.add_step(Step(oj, 200))


        self.geometry(f"{self.settings.width}x{self.settings.height}")
        #self.overrideredirect(True)

        # Configure the weights of the rows
        self.grid_columnconfigure(0, weight=1)  # Horizontal space
        self.grid_rowconfigure(0, weight=8)  # 80%
        self.grid_rowconfigure(1, weight=2)  # 20%

        # Fonts
        self.button_font = customtkinter.CTkFont("Stencil Std", 30, "bold")
        self.title_font = customtkinter.CTkFont("Stencil Std", 48, "bold")
        self.body_font = customtkinter.CTkFont("Stencil Std", 24)
        self.minor_font = customtkinter.CTkFont("Stencil Std", 18)
        
        # Panels
        self.bartender_panel = customtkinter.CTkFrame(self)
        self.bartender_panel.grid(row=0, column=0, sticky="nsew")
        
        self.settings_panel = customtkinter.CTkFrame(self)
        self.settings_panel.grid(row=0, column=0, sticky="nsew")

        self.maintenance_panel = customtkinter.CTkFrame(self)
        self.maintenance_panel.grid(row=0, column=0, sticky="nsew")
  
        self.tool_panel = customtkinter.CTkFrame(self)
        self.tool_panel.grid(row=1, column=0, sticky="nsew")

        # Add buttons to the lower panel with stretching horizontally
        self.btn_settings = customtkinter.CTkButton(self.tool_panel, text="Settings", font=self.button_font, command=self.settings_clicked, corner_radius=0, width=self.settings.width * 0.30)
        self.btn_settings.pack(side="left", fill="y")

        self.btn_bartender = customtkinter.CTkButton(self.tool_panel, text="Bartender", font=self.button_font, command=self.bartender_clicked, corner_radius=0)
        self.btn_bartender.pack(side="left", fill="both", expand=True, padx=2)

        self.btn_setup = customtkinter.CTkButton(self.tool_panel, text="Setup", font=self.button_font, command=self.maintenance_clicked, corner_radius=0, width=self.settings.width * 0.30)
        self.btn_setup.pack(side="left", fill="y")

        self.ml_poured = 0
        self.ml_expected = 0
        self.drink_index = 0
        self.setup_bartender_panel()
        self.setup_settings_panel()
        self.setup_setup_panel()

        self.bartender_clicked()

    def bind_keyboard(self, widget):
        widget.bind("<Button-1>", self.show_keyboard)

    def show_keyboard(self, event):
        keyboard = OnScreenKeyboard(self, event.widget)
        keyboard.mainloop()

    def settings_clicked(self):
        self.btn_bartender.configure(False, fg_color="#1F6AA5")
        self.btn_setup.configure(False, fg_color="#1F6AA5")
        self.btn_settings.configure(True, fg_color="#144870")

        self.settings_panel.tkraise()

    def bartender_clicked(self):
        self.btn_bartender.configure(False, fg_color="#144870")
        self.btn_setup.configure(False, fg_color="#1F6AA5")
        self.btn_settings.configure(True, fg_color="#1F6AA5")

        self.bartender_panel.tkraise()

        self.main_load_drink()

    def maintenance_clicked(self):
        self.btn_bartender.configure(False, fg_color="#1F6AA5")
        self.btn_setup.configure(False, fg_color="#144870")
        self.btn_settings.configure(True, fg_color="#1F6AA5")

        self.maintenance_panel.tkraise()

    def disable_menu(self):
        self.btn_settings.configure(False, state='disabled')
        self.btn_bartender.configure(False, state='disabled')
        self.btn_setup.configure(True, state='disabled')

    def enable_menu(self):
        self.btn_settings.configure(False, state='normal')
        self.btn_bartender.configure(False, state='normal')
        self.btn_setup.configure(True, state='normal')

    def setup_bartender_panel(self):
        # Create a label in the main panel
        button_color = "gray20"

        self.left_arrow_button = customtkinter.CTkButton(self.bartender_panel, text="←", command=self.main_left_arrow_action, font=self.button_font, corner_radius=0, fg_color=button_color, height=self.settings.height * 0.20)
        self.left_arrow_button.pack(side="left")

        # Create the center text
        self.center_text_frame = customtkinter.CTkFrame(self.bartender_panel)
        self.center_text_frame.configure(False, fg_color=self.bartender_panel._fg_color)
        self.center_text_frame.pack(side="left", fill="x", expand=True)

        self.drink_title = customtkinter.CTkLabel(self.center_text_frame, text="Top Text", font=self.body_font)
        self.drink_title.pack(side="top")

        # Create a frame for the side-by-side buttons
        self.button_frame = customtkinter.CTkFrame(self.center_text_frame)
        self.button_frame.configure(True, fg_color=self.bartender_panel._fg_color)
        self.button_frame.pack(side="bottom", pady=(10, 10))  # Add padding above the button frame

        self.main_show_preview_screen()

        # Create the right arrow button
        self.right_arrow_button = customtkinter.CTkButton(self.bartender_panel, text="→", command=self.main_right_arrow_action, font=self.button_font, corner_radius=0, fg_color=button_color, height=self.settings.height * 0.20)
        self.right_arrow_button.pack(side="right")
   
    def main_left_arrow_action(self):
        if self.drink_index > 0:
            self.drink_index -= 1
        else:
            self.drink_index = Cookbook.instance().get_recipe_count() - 1

        self.main_load_drink()

    def main_right_arrow_action(self):
        if self.drink_index < Cookbook.instance().get_recipe_count() - 1:
            self.drink_index += 1
        else:
            self.drink_index = 0

        self.main_load_drink()

    def main_show_pour_screen(self):
        if hasattr(self, 'drink_recipe'):
            self.drink_recipe.destroy()
        
        if hasattr(self, 'pour_button'):
            self.pour_button.destroy()

        self.progressbar = customtkinter.CTkProgressBar(self.center_text_frame, mode="determinate")
        self.progressbar.pack(side="top", anchor="center", pady=(60, 60))

        self.abort_button = customtkinter.CTkButton(self.button_frame, text="Abort", command=self.main_abort, font=self.body_font, corner_radius=0, height=self.settings.height * 0.20)
        self.abort_button.configure(True, fg_color="#a52f2f")
        self.abort_button.pack(side="left")  # Add padding between the buttons

        self.disable_menu()

        recipe = Cookbook.instance().get_recipe(self.drink_index)
        self.ml_poured = 0
        self.ml_expected = recipe.get_volume()
        self.progressbar.set(0)

        index = 0
        for step in recipe.get_steps():
            for pump in self.settings.pumps:
                if pump.beverage == step.beverage.get_id():
                    self.do_tap(pump, step.volume)

            index += 1

    def main_show_preview_screen(self):
        if hasattr(self, 'progressbar'):
            self.progressbar.destroy()

        if hasattr(self, 'abort_button'):
            self.abort_button.destroy()

        self.drink_recipe = customtkinter.CTkLabel(self.center_text_frame, text="Bottom Text", font=self.minor_font, height=self.settings.height / 4)
        self.drink_recipe.pack(side="top")

        # Create the buttons within the button frame
        self.pour_button = customtkinter.CTkButton(self.button_frame, text="Pour", command=self.main_pour, font=self.body_font, corner_radius=0, height=self.settings.height * 0.20)
        self.pour_button.configure(True, fg_color="#2FA572")
        self.pour_button.pack(side="left")  # Add padding between the buttons

        self.main_load_drink()
        self.enable_menu()
        
    def main_pour(self):
        self.left_arrow_button.configure(False, state="disabled")
        self.right_arrow_button.configure(True, state="disabled")

        self.main_show_pour_screen ()

    def main_abort(self):
        self.left_arrow_button.configure(False, state="normal")
        self.right_arrow_button.configure(True, state="normal")

        self.main_show_preview_screen()  
        self.shutdown_all_pumps()
    
    def main_load_drink(self):
        recipe = Cookbook.instance().get_recipe(self.drink_index)
        if recipe is None:
            self.drink_title.configure(False, text="No drink is available.")
            self.pour_button.configure(False, state="disabled")
            self.drink_recipe.configure(True, text="Try creating one in the Setup menu :)")
        else:
            self.drink_title.configure(False, text=recipe.get_name() + " - " + str(recipe.get_volume()) + " mL")
            
            (matches, missing) = self.main_get_pouring_solution(recipe)

            text = ""
            for step in matches:
                text += str(step) + "\n"

            for step in missing:
                text += "[Missing] " + str(step) + "\n"

            if len(missing) == 0:
                self.pour_button.configure(False, state="normal")
            else:
                self.pour_button.configure(False, state="disabled")
                
            self.drink_recipe.configure(True, text=text)
    
    def main_get_pouring_solution(self, recipe: 'Recipe'):
        matches = []
        missing = []

        for step in recipe.get_steps():
            found_match = False
            for pump in self.settings.pumps:
                id = pump.beverage
                if pump.beverage is None or pump.beverage == 0:
                    continue
                if id == step.get_beverage().get_id():
                    found_match = True
                    break
            
            if not found_match:
                missing.append(step)
            else:
                matches.append(step)

        return (matches, missing)

    def setup_settings_panel(self):
        bev_list = []
        for beverage in Cookbook.instance().get_beverages():
            bev_list.append(beverage.get_name())

        self.maintenance_buttons = {}
        for pump in self.settings.pumps:
            section_frame = customtkinter.CTkFrame(self.maintenance_panel, width=self.settings.width)
            section_frame.pack(side="left", fill="both", expand=True)

            # Title
            title_label = customtkinter.CTkLabel(section_frame, text=pump.name, font=self.minor_font)
            title_label.pack(pady=(80,10))

            # Dropdown
            pump_var = customtkinter.StringVar()
            pump_dropdown = customtkinter.CTkComboBox(section_frame, variable=pump_var, values=bev_list, command=lambda event, pump=pump, value=pump_var: self.setup_set_beverage(event, value.get(), pump))
            beverage = Cookbook.instance().get_beverage_by_id(pump.beverage)
            if beverage != None:
                pump_dropdown.set(beverage.name)
            else:
                pump_dropdown.set("Select Beverage")

            pump_dropdown.pack(pady=10)

            # Purge button
            purge_button = customtkinter.CTkButton(section_frame, text="Purge", command=lambda pump=pump: self.setup_purge_action(pump), font=self.body_font, corner_radius=0, height=self.settings.height * 0.20)
            purge_button.pack()

            # Abort button
            abort_button = customtkinter.CTkButton(section_frame, text="Abort", command=lambda pump=pump: self.setup_abort_action(pump), font=self.body_font, corner_radius=0, height=self.settings.height * 0.20)
            abort_button.pack()

            self.maintenance_buttons[pump] = {"purge": purge_button, "abort": abort_button, "state": False}

            self.setup_abort_action(pump)

    def setup_purge_action(self, pump):
        self.run_pump(pump)

        self.maintenance_buttons[pump]['purge'].pack_forget()
        self.maintenance_buttons[pump]['abort'].pack()
        self.maintenance_buttons[pump]['state'] = True

        self.disable_menu()

    def setup_abort_action(self, pump):
        self.shutdown_pump(pump)

        self.maintenance_buttons[pump]['state'] = False
        self.maintenance_buttons[pump]['purge'].pack()
        self.maintenance_buttons[pump]['abort'].pack_forget()

        is_aborting = False
        for pump in self.maintenance_buttons.values():
            if pump['state']:
                is_aborting = True
                break

        if not is_aborting:
            self.enable_menu()

    def setup_set_beverage(self, event, value, key):
        key.beverage = Cookbook.instance().get_beverage_by_name(value).get_id()
        self.settings.save_settings()

    def setup_setup_panel(self):
        items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]

        # Create three CustomPanel instances side by side
        panel1 = CustomPanel(self.settings_panel, "Beverage Types", items, self.body_font, self.minor_font, self.body_font)
        panel1.grid(row=0, column=0, sticky="nsew")

        panel2 = CustomPanel(self.settings_panel, "Beverages", items, self.body_font, self.minor_font, self.body_font)
        panel2.grid(row=0, column=1, sticky="nsew")

        panel3 = CustomPanel(self.settings_panel, "Recipes", items, self.body_font, self.minor_font, self.body_font)
        panel3.grid(row=0, column=2, sticky="nsew")

        # Configure row and column weights to make them expandable
        self.settings_panel.grid_rowconfigure(0, weight=1)
        self.settings_panel.grid_columnconfigure(0, weight=1)
        self.settings_panel.grid_columnconfigure(1, weight=1)
        self.settings_panel.grid_columnconfigure(2, weight=1)

    def do_tap(self, pump: Pump, mls: int):
        seconds = float(mls) / float(self.settings.milliliters_per_second)

        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(pump.addr, GPIO.OUT)
        except:
            pass

        print("Pouring from " + pump.name + " " + str(mls) + " mL (" + str(seconds) + ") seconds.")

        self.run_pump(pump)
        timer = threading.Timer(seconds, self.on_tap_complete, [pump, mls])
        timer.start()
        
    def on_tap_complete(self, pump, mls):
        self.shutdown_pump(pump)
        self.ml_poured += mls

        percent = (self.ml_poured / self.ml_expected)
        self.progressbar.set(percent)
        if percent > 0.99:
            self.main_abort()

    def run_pump(self, pump):
        GPIO.output(pump.addr, GPIO.HIGH)

    def shutdown_all_pumps(self):
        for pump in self.settings.pumps:
            self.shutdown_pump(pump)

    def shutdown_pump(self, pump):
        GPIO.output(pump.addr, GPIO.LOW)


def initialize():
    if not check_config_exists():
        copy_config_template()

    database = Database(COOKBOOK_DB_PATH)
    database.load_data()

def check_config_exists():
    return os.path.exists(COOKBOOK_DB_PATH)

def copy_config_template():
    shutil.copyfile(COOKBOOK_DB_TEMPLATE, COOKBOOK_DB_PATH)

if __name__ == "__main__":
    initialize()

    customtkinter.set_appearance_mode('dark')
    app = App()
    app.mainloop()