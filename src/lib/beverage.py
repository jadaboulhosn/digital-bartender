from type import Type
from hash import get_hash

class Beverage(object):
    def __init__(self, name: str, type: Type):
        self.name = name
        self.type = type

    def get_name(self) -> str:
        return self.name
    
    def get_type(self) -> Type:
        return self.type

    def get_id(self) -> int:
        return get_hash(self.name + str(self.type))
    
    def __str__(self):
        return self.name + " (" + str(self.type) + ")"

    def __eq__(self, other): 
        if other is None:
            return False
        
        if isinstance(other, Beverage):
            return other.name == self.name and other.type == self.type
        else:
            return self.__dict__ == other.__dict__

