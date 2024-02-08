import sys
sys.path.insert(0, './')

from os.path import isfile
from pathlib import Path
import shutil
import jsonpickle
import logging

from backend.barista import Recipes, Beverages, Types
from hal.system import System

class Storage(object):
    def __init__(self, reference, path):
        self.reference = reference
        self.path = path

class Database(object):
    def __init__(self, path = "../data/"):
        self.path = path

        Path(path).mkdir(parents=True, exist_ok=True)
        self.archive = [
            Storage(Types.instance(), self.path + "types.json"),
            Storage(Beverages.instance(), self.path + "beverages.json"),
            Storage(Recipes.instance(), self.path + "recipes.json"),
            Storage(System.instance(), self.path + "system.json")
        ]
        
        self.last_write = {}
 
    def load(self):
        if self.path == None:
            logging.error("Attempted to load from database before initialization!")
            return
        
        try:
            for datum in self.archive:
                if isfile(datum.path):
                    with open(datum.path, 'r') as file:
                        datum.reference.data = jsonpickle.decode(file.read())

                    if isinstance(datum.reference, System):
                        for pump in System.instance().data:
                            pump.active = False
                            pump.is_setup = False
                            pump.setup()

                    if isinstance(datum.reference, Types) or isinstance(datum.reference, Beverages) or isinstance(datum.reference, Recipes):
                        logging.info(f"Successfully read {datum.path}. Restoring object references...")

                        for ser_rec in Recipes.instance():
                            logging.info(f"Checking Recipe: {ser_rec}")

                            for step in ser_rec.steps:
                                relinked_beverage = False
                                for ser_bev in Beverages.instance():
                                    if hash(step.beverage) == hash(ser_bev):
                                        logging.info(f"\tRelinking Beverage: {ser_bev}")
                                        step.beverage = ser_bev
                                        relinked_beverage = True

                                        relinked_type = False
                                        for ser_type in Types.instance():
                                            if hash(step.beverage.type) == hash(ser_type):
                                                logging.info(f"\tRelinking Type: {ser_type}")
                                                step.beverage.type = ser_type
                                                relinked_type = True
                                                break
                                        
                                        if not relinked_type:
                                            logging.error(f"\tUnable to relink Type: {step.beverage.type}")

                                        break
                                if not relinked_beverage:
                                    logging.error(f"\tUnable to relink Beverage: {step.beverage}")
                    else:
                        logging.info(f"Successfully read {datum.path}.")
                else:
                    logging.warning(f"Unable to read archival data at {datum.path}.")

            return True
        except Exception as e:
            logging.critical(f"Unable to read archival data:\n\t{e}", exc_info=True)
            return False
    
    def save(self):
        if self.path == None:
            logging.error("Attempted to save to database before initialization!")
            return
        
        try:
            for datum in self.archive:
                data = jsonpickle.encode(datum.reference.data)

                needs_write = False
                if datum.path not in self.last_write:
                    needs_write = True

                if datum.path in self.last_write and self.last_write[datum.path] != data:
                    needs_write = True

                if needs_write:
                    with open(datum.path, 'w') as file:
                        self.last_write[datum.path] = data
                        file.write(data)
                        logging.info(f"Detected change. Writing {len(datum.reference.data)} objects to {datum.path}.")
            return True
        except Exception as e:
            logging.critical(f"Unable to write archival data:\n\t{e}", exc_info=True)
            return False
        
    def destroy(self):
        if self.path == None:
            logging.error("Attempted to destroy database before initialization!")
            return
        
        shutil.rmtree(self.path)