import subprocess
import logging

from hal.system import System
from shared.singleton import Singleton
from backend.util import get_hostname

@Singleton
class Updater:
    def __init__(self):
        pass

    def can_update(self):
        if get_hostname() != 'barntender':
            return False
        
        for pump in System.instance():
            if pump.active:
                return False
        return True

    def check_for_updates(self):
        if self.can_update():
            subprocess.check_output(['git', 'fetch'])
            if "up to date" not in subprocess.check_output(['git', 'status']).decode("utf-8").replace("\n", "").strip():
                logging.info("Update was detected in git. Retreiving...")
                subprocess.check_output(['git', 'pull'])
                
                logging.info("Update downloaded... restarting!")
                subprocess.Popen(["../run.sh"], start_new_session=True)
                exit()