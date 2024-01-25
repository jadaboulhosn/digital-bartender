class Type(object):
    def __init__(self, name: str):
        self.name = name
        
    def __str__(self):
        return self.name

    def __eq__(self, other):
        if other is None:
            return False
        
        if isinstance(other, Type):
            return other.name == self.name
        else:
            return self.__dict__ == other.__dict__