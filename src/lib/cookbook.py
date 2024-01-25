from typing import List

from type import Type
from beverage import Beverage
from recipe import Recipe
from singleton import Singleton

@Singleton
class Cookbook():
    def __init__(self):
        self.types = []
        self.beverages = []
        self.recipes = []

    def get_data(self):
        return { 
            'types': self.types,
            'beverages': self.beverages,
            'recipes': self.recipes
        }

    def set_data(self, data):
        self.types = data['types']
        self.beverages = data['beverages']
        self.recipes = data['recipes']

    # Recipes
    def add_recipe(self, recipe: 'Recipe'):
        self.recipes.append(recipe)

    def remove_recipe(self, recipe: 'Recipe'):
        self.recipes.remove(recipe)

    def has_recipe(self, recipe: 'Recipe') -> bool:
        return recipe in self.recipes

    def get_recipe(self, index: int) -> Recipe:
        if index >= 0 and index < len(self.recipes):
            return self.recipes[index]
        return None

    def get_recipes(self) -> List[Recipe]:
        return self.recipes
    
    def get_recipe_count(self) -> int:
        return len(self.recipes)

    # Beverages
    def add_beverage(self, beverage: 'Beverage'):
        self.beverages.append(beverage)

    def remove_beverage(self, beverage: 'Beverage') -> bool:
        if beverage in self.beverages:
            self.beverages.remove(beverage)

            purge_recipes = []
            for recipe in self.recipes:
                if recipe.has_beverage(beverage):
                    purge_recipes.append(recipe)
            
            for recipe in purge_recipes:
                self.recipes.remove(purge_recipes)
        return False

    def has_beverage(self, beverage: 'Beverage') -> bool:
        return beverage in self.beverages

    def get_beverage_by_name(self, name: str) -> Beverage:
        for beverage in self.beverages:
            if beverage.name == name:
                return beverage
        return None
     
    def get_beverage_by_id(self, id: int) -> Beverage:
        for beverage in self.beverages:
            if beverage.get_id() == id:
                return beverage
        return None 

    def get_beverage(self, index: int) -> Beverage:
        if index >= 0 and index < len(self.beverages):
            return self.beverages[index]
        return None
    
    def get_beverages(self) -> List[Beverage]:
        return self.beverages
    
    def get_beverage_count(self) -> int:
        return len(self.beverages)

    # Types
    def add_type(self, type: 'Type'):
        self.types.append(type)
    
    def remove_type(self, type: 'Type') -> bool:
        if type in self.types:
            self.types.remove(type)

            purge_beverages = []
            for beverage in self.beverages:
                if beverage.get_type() == type and beverage not in purge_beverages:
                    purge_beverages.append(beverage)

            if len(purge_beverages) > 0:
                for beverage in purge_beverages:
                    self.beverages.remove(beverage)

                    purge_recipes = []
                    for recipe in self.recipes:
                        if recipe.has_beverage(beverage) and recipe not in purge_recipes:
                            purge_recipes.append(recipe)
                    
                    for recipe in purge_recipes:
                        self.recipes.remove(recipe)

            return True
        return False
    
    def get_types(self) -> List[Type]:
        return self.types

    def has_type(self, type: 'Type') -> bool:
        return type in self.types

    def get_type(self, index: int) -> Type:
        if index >= 0 and index < len(self.types):
            return self.types[index]
        return None
     
    def get_type_count(self) -> int:
        return len(self.types)