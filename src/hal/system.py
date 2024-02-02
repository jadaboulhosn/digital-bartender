import logging
import asyncio

from frontend.settings import Settings
from shared.singleton import Singleton
from hal.pump import Pump
from backend.barista import Beverages
from backend.bar import Recipe, Beverage

@Singleton
class System():
    def __init__(self):
        self.data = [] 
        self.progress = 0
        self.is_pouring = False
        self.timer = None
        
        self.loop = asyncio.get_event_loop()
    
    def attach(self, name: str, vcc_pin: int, gnd_pin: int) -> Pump:
        pump = Pump(name, vcc_pin, gnd_pin)
        
        logging.info(f"Adding {pump} to System.")
        self.data.append(pump)
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

    def validate_pumps(self):
        for pump in self.data:
            has_match = False
            for beverage in Beverages.instance():
                if pump.id != -1 and pump.id == hash(beverage):
                     has_match = True
            if not has_match:
                pump.id = -1

    def get_pump_ids(self) -> list:
        ids = []
        for pump in self.data:
            if pump.id != -1:
                ids.append(pump.id)
        return ids
    
    def can_pour(self, recipe: 'Recipe') -> bool:
        self.validate_pumps()

        ids = self.get_pump_ids()
        for step in recipe.steps:
            if hash(step.beverage) not in ids:
                return False
        return True

    def get_missing(self, recipe: 'Recipe') -> list:
        self.validate_pumps()

        missing = []
        ids = self.get_pump_ids()
        for step in recipe.steps:
            if hash(step.beverage) not in ids:
                missing.append(hash(step.beverage))
        
        beverages = []
        for id in missing:
            for beverage in Beverages.instance():
                if hash(beverage) == id:
                    beverages.append(beverage)
                    break
        return beverages          

    def pour(self, recipe: 'Recipe', callback) -> bool:
        if self.can_pour(recipe) and not self.is_pouring:
            timing = []
            self.progress = 0

            logging.info(f"Pouring {recipe} now ({recipe.volume()} mL)")
            for step in recipe.steps:                
                found = False
                for pump in self.data:
                    if pump.id == hash(step.beverage):
                        duration = float(step.volume) / float(Settings.instance().mls_per_second)
                        logging.info(f"Pouring {step.beverage} ({step.volume} mL, {round(duration, 2)} seconds)")
                        found = True

                        timing.append(PumpData(pump, duration))
                        pump.activate()
                        
                        break       
                if not found:
                    logging.error(f"Unable to locate one or more ingredients despite check!")         
                    self.abort()
                    return False
            self.is_pouring = True
            self.timer = PumpTimer(0.05, timing, self.on_progress_updated, lambda: [self.on_pour_complete(), callback()])
            return True
        elif self.is_pouring:
            logging.error(f"Unable to pour {recipe} because a pour is already in progress!")
        else:
            logging.error(f"Unable to pour {recipe} due to missing ingredients!")
        return False

    def on_progress_updated(self, progress: float):
        self.progress = progress

    def on_pour_complete(self):
        self.progress = 0
        self.is_pouring = False
        self.timer = None

    def abort(self):
        logging.warning("Aborting all pump activities now!")
        self.timer.cancel()
        for pump in self.data:
            if pump.is_active():
                logging.warning(f"\tDeactivating {pump}.")
                pump.deactivate()

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
    
class PumpData:
    def __init__(self, pump: 'Pump', duration: float):
        self.pump = pump
        self.duration = duration

class PumpTimer:
    def __init__(self, interval, data, progress_callback, completion_callback):
        self.interval = interval
        self.completion_callback = completion_callback
        self.progress_callback = progress_callback
        self.data = data
        self.running = True
        self.task = asyncio.ensure_future(self.job())
        
        self.total_time = 0
        for data in self.data:
            self.total_time = max(self.total_time, data.duration)

        self.time = 0

        logging.info(f"Starting async event loop to track pumps with {len(self.data)} tasks.")

    async def job(self):
        try:
            while self.running:
                await asyncio.sleep(self.interval)
                
                completed_pumps = []
                for data in self.data:
                    data.duration -= self.interval
                    if data.duration <= 0:                    
                        completed_pumps.append(data)
                
                for data in completed_pumps:
                    data.pump.deactivate()
                    self.data.remove(data)
                    logging.info(f"\t{data.pump} is complete. There are {len(self.data)} tasks remaining.")

                if len(self.data) == 0:
                    self.running = False   

                self.time += self.interval
                self.progress_callback(self.time / self.total_time)
                if self.time >= self.total_time:
                    logging.info(f"Pour task is now complete ({round(self.time, 2)} seconds)!")
                    self.cancel()
            self.completion_callback()
        except Exception as ex:
            logging.critical(ex, exc_info=True)

    def cancel(self):
        self.running = False
        self.task.cancel()