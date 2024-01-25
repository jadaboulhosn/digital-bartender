from typing import List

from beverage import Beverage
from step import Step
from hash import get_hash

class Recipe(object):
    def __init__(self, name: str):
        self.name = name
        self.steps = []

    def get_name(self) -> str:
        return self.name

    def add_step(self, step: 'Step'):
        self.steps.append(step)

    def remove_step(self, step: 'Step') -> bool:
        if step in self.steps:
            self.steps.remove(step)
            return True
        return False
    
    def get_step(self, index: int) -> Step:
        if index >= 0 and index < len(self.steps):
            return self.steps[index]
        return None
    
    def get_steps(self) -> List[Step]:
        return self.steps

    def get_step_count(self) -> int:
        return len(self.steps)
    
    def has_beverage(self, beverage: 'Beverage') -> bool:
        for step in self.steps:
            if step.get_beverage() == beverage:
                return True            
        return False
    
    def get_volume(self) -> int:
        volume = 0
        for step in self.steps:
            volume += step.get_volume()
        return volume
    
    def get_id(self) -> int:
        return get_hash(self.name)

    def __eq__(self, other):
        if other is None:
            return False
        
        if isinstance(other, Recipe):
            if other.name == self.name and len(other.steps) == len(self.steps):
                valid = True
                for i in range(0, len(self.steps)):
                    if self.get_step(i) != other.get_step(i):
                        valid = False
                        break
                if valid:
                    return True
            return False
        else:
            return self.__dict__ == other.__dict__