import logging

from shared.singleton import Singleton
from hal.pump import Pump

@Singleton
class System():
    def __init__(self):
        self.data = []
    
    def attach(self, name: str, pin_number: int) -> Pump:
        pump = Pump(name, pin_number)
        self.data.append(pump)

        logging.info(f"Adding {pump} to System.")
        return pump

    def disconnect(self, pump: 'Pump') -> bool:
        if pump in self.data:
            logging.info(f"Disconnecting {pump} from System.")
            
            pump.teardown()
            self.data.remove(pump)
        else:
            logging.error(f"Unable to disconnect {pump} from System as it does not exist!")
            return False
        
    def clear(self):
        self.data = []

    def __iter__(self):
        return iter(self.data)
    
    def __next__(self):
        if self.current == None:
            self.current = 0
        
        if self.current >= len(self):
            raise StopIteration
        
        self.current += 1
        return self.current

    def __getitem__(self, index: int) -> Pump:
        if index >= 0 and index < len(self.data):
            return self.data[index]
        return None
 
    def __len__(self) -> int:
        return len(self.data)