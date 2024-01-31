from backend.util import get_hash

class Entity(object):
    def __init__(self):
        pass

    def __hash__(self) -> int:
        members = [
            attr for attr in dir(self) 
            if not callable(getattr(self, attr)) 
            and not attr.startswith("__")
            ]
        hash_str = ""
        for attr in members:
            attr_val = getattr(self, attr)
            if isinstance(attr_val, list):
                for list_val in attr_val:
                    hash_str += str(list_val)
            else:
                hash_str += str(attr_val)
        
        return get_hash(hash_str)

    def __eq__(self, other):
        if other is None:
            return False
        
        if isinstance(other, Entity):
            return hash(other) == hash(self)

        return False
        