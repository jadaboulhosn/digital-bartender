import subprocess
import asyncio

class Updater:
    def __init__(self, app):
        self.task = asyncio.Task(self.check_for_updates())
        self.ready = True
        self.app = app
        pass

    def set_update_readiness(self, state):
        prev_state = self.ready
        self.ready = state
        if prev_state != state:
            if state:
                print("Updates are now enabled.")
            else:
                print("Updates are now disabled.")

    async def check_for_updates(self):
        while True:
            if "up to date" not in subprocess.check_output(['git', 'status']).decode("utf-8").replace("\n", "").strip() and self.ready:
                print("Update was detected in git. Retreiving...")
                subprocess.check_output(['git', 'pull'])
                
                print("Update downloaded... restarting!")
                self.task.cancel()

                subprocess.Popen(["python3", "../main.py"], start_new_session=True)

                self.app.settings.save_settings()

                exit()
            asyncio.sleep(1)