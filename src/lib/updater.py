import subprocess
import shlex
import asyncio

class Updater:
    def __init__(self):
        self.task = asyncio.Task(self.check_for_updates())
        self.ready = True
        pass

    def set_update_readiness(self, state):
        self.ready = state
        if state:
            print("Updates are now enabled.")
        else:
            print("Updates are now disabled.")

    async def check_for_updates(self):
        while True:
            if "up to date" not in subprocess.check_output(['git', 'status']) and self.ready:
                print("Update was detected in git. Retreiving...")
                subprocess.check_output(['git', 'pull'])
                
                print("Update downloaded... restarting!")
                self.task.cancel()

                cmds = shlex.split("python3 ../main.py")
                subprocess.Popen(cmds, start_new_session=True)

                exit()
            asyncio.sleep(1)