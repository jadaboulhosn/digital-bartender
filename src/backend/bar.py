import sys
sys.path.insert(0, './')

from shared.entity import Entity

class Type(Entity):
    def __init__(self, name: str):
        self.name = name

        super().__init__()
        
    def __str__(self):
        return self.name

class Beverage(Entity):
    def __init__(self, name: str, type: Type):
        self.name = name
        self.type = type

        super().__init__()

    def __str__(self):
        return self.name + " (" + str(self.type) + ")"

class Step(Entity):
    def __init__(self, beverage: 'Beverage', volume: int):
        self.beverage = beverage
        self.volume = volume

        super().__init__()

    def set_volume(self, volume: int):
        self.volume = volume

    def __str__(self) -> str:
        return str(self.beverage) + " [" + str(self.volume) + " mL]"

class Recipe(Entity):
    def __init__(self, name: str):
        self.name = name
        self.steps = []

        super().__init__()

    def append(self, step: 'Step'):
        self.steps.append(step)

    def remove(self, step: 'Step') -> bool:
        if step in self.steps:
            self.steps.remove(step)
            return True
        return False
    
    def contains(self, beverage: 'Beverage') -> bool:
        for step in self.steps:
            if step.beverage == beverage:
                return True            
        return False
    
    def volume(self) -> int:
        volume = 0
        for step in self.steps:
            volume += step.volume
        return volume
    
    def __str__(self) -> str:
        desc = f"{self.name}"
        if (len(self.steps) > 0):
            desc += " ("
            for step in self.steps:
                desc += f"{str(step)}, "
            desc = desc[0:len(desc) - 2] + ")"
        return desc 