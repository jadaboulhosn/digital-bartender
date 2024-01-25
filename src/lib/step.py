from beverage import Beverage
from hash import get_hash

class Step(object):
    def __init__(self, beverage: 'Beverage', volume: int):
        self.beverage = beverage
        self.volume = volume

    def get_beverage(self) -> Beverage:
        return self.beverage
    
    def get_volume(self) -> int:
        return self.volume
    
    def get_id(self) -> int:
        return get_hash(str(self.beverage) + str(self.volume))

    def __str__(self) -> str:
        return str(self.beverage) + " [" + str(self.volume) + " mL]"

    def __eq__(self, other):
        if other is None:
            return False
        
        if isinstance(other, Step):
            return other.beverage == self.beverage and other.volume == self.volume
        else:
            return self.__dict__ == other.__dict__