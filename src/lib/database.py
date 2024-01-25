from singleton import Singleton
from cookbook import Cookbook
import jsonpickle

class Database(object):
    def __init__(self, path: str):
        self.path = path
        self.cookbook = Cookbook.instance()
    
    def load_data(self):
        try:
            with open(self.path, 'r') as file:
                self.cookbook.set_data(jsonpickle.decode(file.read()))
                return True
        except:
            return False
    
    def save_data(self):
        try:
            with open(self.path, 'w') as file:
                file.write(jsonpickle.encode(self.cookbook.get_data()))
                return True
        except:
            return False