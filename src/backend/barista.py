import sys
sys.path.insert(0, './')

from typing import List
import logging

from backend.bar import Beverage, Recipe, Type
from shared.singleton import Singleton

@Singleton
class Types():
    def __init__(self):
        self.data = []

    def append(self, type: 'Type'):
        logging.info(f"Adding {type} to Types.")
        self.data.append(type)

    def check_references(self, type: 'Type') -> bool:
        if type in self.data:
            for beverage in Beverages.instance():
                if beverage.type == type:
                    return True

        return False

    def remove(self, type: 'Type') -> bool:
        logging.info(f"Removing {type} from Types.")
        if type in self.data:
            purge_beverages = []
            for beverage in Beverages.instance():
                if beverage.type == type:
                    purge_beverages.append(beverage)

            if len(purge_beverages) > 0:
                logging.warning(f"This Type has {len(purge_beverages)} associated beverages that will be purged.")
                for beverage in purge_beverages:
                    logging.warning(f"Removing {beverage} from Beverages.")
                    Beverages.instance().remove(beverage)
            
            self.data.remove(type)
            logging.info(f"Removed {type} from Types.")
            return True
        else:
            logging.error(f"Unable to remove {type} from Types as it does not exist!")
            return False

    def clear(self):
        self.data = []

    def contains(self, type: 'Type') -> bool:
        return type in self.data

    def __iter__(self):
        return iter(self.data)
    
    def __next__(self):
        if self.current == None:
            self.current = 0
        
        if self.current >= len(self):
            raise StopIteration
        
        self.current += 1
        return self.current

    def __getitem__(self, index: int) -> Type:
        if index >= 0 and index < len(self.data):
            return self.data[index]
        return None
     
    def __len__(self) -> int:
        return len(self.data)


@Singleton
class Beverages():
    def __init__(self):
        self.data = []

    def append(self, beverage: 'Beverage'):
        logging.info(f"Adding {beverage} to Beverages.")
        self.data.append(beverage)

    def check_references(self, beverage: 'Beverage') -> bool:
        if beverage in self.data:
            for recipe in Recipes.instance():
                if recipe.contains(beverage):
                    return True
        
        return False

    def remove(self, beverage: 'Beverage') -> bool:
        logging.info(f"Removing {beverage} from Beverages.")
        if beverage in self.data:
            purge_recipes = []
            for recipe in Recipes.instance():
                if recipe.contains(beverage):
                    purge_recipes.append(recipe)

            if len(purge_recipes) > 0:
                logging.warning(f"This Beverage has {len(purge_recipes)} associated recipes that will be purged.")
                for recipe in purge_recipes:
                    logging.warning(f"Removing {recipe} from Recipes.")
                    Recipes.instance().remove(recipe)
        
            self.data.remove(beverage)
            logging.info(f"Removed {beverage} from Beverages.")
            return True
        else:
            logging.error(f"Unable to remove {beverage} from Beverages as it does not exist!")
            return False
        
    def clear(self):
        self.data = []

    def contains(self, beverage: 'Beverage') -> bool:
        return beverage in self.data

    def __iter__(self):
        return iter(self.data)
    
    def __next__(self):
        if self.current == None:
            self.current = 0
        
        if self.current >= len(self):
            raise StopIteration
        
        self.current += 1
        return self.current

    def __getitem__(self, index: int) -> Beverage:
        if index >= 0 and index < len(self.data):
            return self.data[index]
        return None
 
    def __len__(self) -> int:
        return len(self.data)
    
@Singleton
class Recipes():
    def __init__(self):
        self.data = []

    def append(self, recipe: 'Recipe'):
        logging.info(f"Adding {recipe} to Recipes.")
        self.data.append(recipe)

    def remove(self, recipe: 'Recipe'):
        logging.info(f"Removing {recipe} from Recipes.")
        if recipe in self:
            self.data.remove(recipe)
            return True
        
        return False

    def clear(self):
        self.data = []

    def contains(self, recipe: 'Recipe') -> bool:
        return recipe in self.data

    def __iter__(self):
        return iter(self.data)
    
    def __next__(self):
        if self.current == None:
            self.current = 0
        
        if self.current >= len(self):
            raise StopIteration
        
        self.current += 1
        return self.current

    def __getitem__(self, index: int) -> Recipe:
        if index >= 0 and index < len(self.data):
            return self.data[index]
        return None

    def __len__(self) -> int:
        return len(self.data)