import logging

import sys
sys.path.insert(0, './')
try:
    logging.info("Importing RPi GPIO Libary...")
    import RPi.GPIO as GPIO
except Exception as e:
    logging.warning("RPi GPIO Library is missing, will use emulator instead.")
    import hal.gpio as GPIO

from hal.pins import Pins
from shared.entity import Entity

class Pump(Entity):
    def __init__(self, name = "", pin_number = -1):
        self.name = name
        self.id = -1
        self.pin_number = -1
        self.is_setup = False
        self.active = False

        self.set_pin_number(pin_number)
    
    def setup(self):
        if not self.is_setup:
            if Pins.instance().is_pin_permitted(pin_number = self.pin_number):
                GPIO.setup(self.pin_number, GPIO.OUT)
                self.is_setup = True
                logging.info(f"{self} is now ready.")
            else:
                self.is_setup = False
                logging.error(f"Unable to setup {self} because the pin number is invalid!")
        else:
            logging.error(f"Unable to setup {self} because this device is already setup!")

    def teardown(self):
        if self.is_setup:
            logging.info(f"Tearing down {self}.")
            if self.is_active:
                self.deactivate()

            self.is_setup = False

    def activate(self) -> bool:
        if self.is_setup:
            if Pins.instance().is_pin_permitted(pin_number = self.pin_number):
                if not self.active:
                    logging.info(f"Activating {self}.")
                    GPIO.output(self.pin_number, GPIO.HIGH)
                    self.active = True

                    return True
                else:
                    logging.info(f"Skipping activation of {self} because it is already active.")
            else:
                logging.error(f"Unable to activate GPIO@{self.pin_number}. The address is invalid.")
        else:
            logging.error(f"Unable to activate {self} because it is not setup!")

        return False

    def deactivate(self) -> bool:
        if self.is_setup:
            if Pins.instance().is_pin_permitted(pin_number = self.pin_number):
                if self.active:
                    logging.info(f"Deactivating {self}.")
                    GPIO.output(self.pin_number, GPIO.LOW)
                    self.active = False

                    return True
                else:
                    logging.info(f"Skipping deactivation of {self} because it is already inactive.")
            else:
                logging.error(f"Unable to deactivate GPIO@{self.pin_number}. The address is invalid.")
        else:
            logging.error(f"Unable to deactivate {self} because it is not setup!")
            
        return False

    def set_pin_number(self, pin_number):
        if Pins.instance().is_pin_permitted(pin_number = pin_number):
            logging.info(f"Setting {self.name} to {Pins.instance().get_pin_name(pin_number)}")
            
            if self.is_setup:
                self.teardown()

            self.pin_number = pin_number
            self.setup()
        else:
            logging.error(f"Unable to set {self.name} to {pin_number} because the pin number is invalid.")        

    def is_valid(self) -> bool:
        return self.is_setup

    def is_active(self) -> bool:
        return self.active and self.is_setup

    def __str__(self) -> str:
        return f"{self.name}@{Pins.instance().get_pin_name(self.pin_number)}"