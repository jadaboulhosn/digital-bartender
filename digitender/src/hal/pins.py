import sys
sys.path.append("./")

import logging

from shared.singleton import Singleton

@Singleton
class Pins():
    def __init__(self):
        # RPi Pinout
        self.PIN_NAMES = \
        {
            1: "3.3V",
            3: "GPIO02",
            5: "GPIO03",
            7: "GPIO04",
            9: "GND",
            11: "GPIO17",
            13: "GPIO27",
            15: "GPIO22",
            17: "3.3V",
            19: "GPIO10",
            21: "GPIO09",
            23: "GPIO11",
            25: "GND",
            27: "ID_SC",
            29: "GPIO05",
            31: "GPIO06",
            33: "GPIO13",
            35: "GPIO19",
            37: "GPIO26",
            39: "GND",

            2: "5V",
            4: "5V",
            6: "GND",
            8: "GPIO14",
            10: "GPIO15",
            12: "GPIO18",
            14: "GND",
            16: "GPIO23",
            18: "GPIO24",
            20: "GND",
            22: "GPIO25",
            24: "GPIO08",
            26: "GPIO07",
            28: "ID_SC",
            30: "GND",
            32: "GPIO12",
            34: "GND",
            36: "GPIO16",
            38: "GPIO20",
            40: "GPIO21"
        }

        # Flip Pinout to get Pins
        self.PIN_NUMBERS = {}
        for pin, name in self.PIN_NAMES.items():
            if name in self.PIN_NUMBERS:
                self.PIN_NUMBERS[name].append(pin)
            else:
                self.PIN_NUMBERS[name] = [pin]

    def get_pin_name(self, pin_number):
        if pin_number in self.PIN_NAMES:
            return self.PIN_NAMES[pin_number]
        else:
            logging.error(f"There is no pin name associated with pin {pin_number}! Invalid lookup.")
    
    def get_pin_number(self, pin_name):
        if pin_name in self.PIN_NUMBERS:
            return self.PIN_NUMBERS[pin_name]
        else:
            logging.error(f"There is no pin number associated with {pin_name}! Invalid lookup.")

    def is_pin_permitted(self, pin_name = None, pin_number = None):
        if pin_name is not None:
            if pin_name in self.PIN_NUMBERS:
                return "GPIO" in pin_name
            else:
                logging.error(f"{pin_name} is not a valid pin name!")
                return False
            
        if pin_number is not None:
            if pin_number in self.PIN_NAMES:
                return "GPIO" in self.PIN_NAMES[pin_number]
            else:
                logging.error(f"Pin {pin_number} is not a valid pin number!")
                return False
