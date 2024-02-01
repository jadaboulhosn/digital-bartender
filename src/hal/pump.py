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
    def __init__(self, name = "", vcc_pin = -1, gnd_pin = -1):
        self.name = name
        self.id = -1
        self.vcc_pin = vcc_pin
        self.gnd_pin = gnd_pin
        self.is_setup = False
        self.active = False

        self.set_pin_number(vcc_pin, gnd_pin)
    
    def setup(self):
        if not self.is_setup:
            if Pins.instance().is_pin_permitted(pin_number = self.vcc_pin):
                if Pins.instance().is_pin_permitted(pin_number = self.gnd_pin):
                    GPIO.setup(self.vcc_pin, GPIO.OUT)
                    self.is_setup = True
                    logging.info(f"{self} is now ready.")
                else:
                    self.is_setup = False
                    logging.error(f"Unable to setup {self} because the GND pin number is invalid!")
            else:
                self.is_setup = False
                logging.error(f"Unable to setup {self} because the VCC pin number is invalid!")
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
            if not self.active:
                logging.info(f"Activating {self}.")
                GPIO.output(self.vcc_pin, GPIO.HIGH)
                GPIO.output(self.gnd_pin, GPIO.LOW)
                self.active = True

                return True
            else:
                logging.info(f"Skipping activation of {self} because it is already active.")
        else:
            logging.error(f"Unable to activate {self} because it is not setup!")

        return False

    def deactivate(self) -> bool:
        if self.is_setup:
            if self.active:
                logging.info(f"Deactivating {self}.")
                GPIO.output(self.vcc_pin, GPIO.LOW)
                GPIO.output(self.gnd_pin, GPIO.LOW)
                self.active = False

                return True
            else:
                logging.info(f"Skipping deactivation of {self} because it is already inactive.")
        else:
            logging.error(f"Unable to deactivate {self} because it is not setup!")
            
        return False

    def set_pin_number(self, vcc_pin, gnd_pin):
        if Pins.instance().is_pin_permitted(pin_number = vcc_pin):
            if Pins.instance().is_pin_permitted(pin_number = gnd_pin):
                logging.info(f"Setting {self.name} to \
                    VCC@{Pins.instance().get_pin_name(vcc_pin)} and \
                    GND@{Pins.instance().get_pin_name(vcc_pin)}")
                if self.is_setup:
                    self.teardown()

                self.vcc_pin = vcc_pin
                self.gnd_pin = gnd_pin
                self.setup()
            else:
                 logging.error(f"Unable to set GND@{self.name} to {vcc_pin} because the pin number is invalid.")      
        else:
            logging.error(f"Unable to set VCC@{self.name} to {vcc_pin} because the pin number is invalid.")        

    def is_valid(self) -> bool:
        return self.is_setup

    def is_active(self) -> bool:
        return self.active and self.is_setup

    def __str__(self) -> str:
        return f"{self.name}: VCC@{Pins.instance().get_pin_name(self.vcc_pin)} GND@{Pins.instance().get_pin_name(self.gnd_pin)}"