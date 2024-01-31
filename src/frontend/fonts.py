import customtkinter as ctk
import logging

from shared.singleton import Singleton

@Singleton
class Fonts():
    def __init__(self):
        self.fonts = {}

    def add(self, name: str, font: ctk.CTkFont):
        if name not in self.fonts:
            self.fonts[name] = font
            logging.info(f"Registered font with name {name}@{font}.")
        else:
            logging.error(f"Unable to register font with name {name}@{font} because it already exists!")

    def get(self, name) -> ctk.CTkFont:
        if name in self.fonts:
            return self.fonts[name]
        else:
            logging.error(f"No font with name {name} exists in the registry!")
            return None
