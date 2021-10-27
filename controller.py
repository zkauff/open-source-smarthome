# Base controller class
# Author : zkauff

from rivescript import RiveScript
import pathlib
from speech_module import SpeechModule
from datetime import datetime
from smart_module import SmartModule 

class SmartController():
    def __init__(self, logfile=None):
        self.rivebot = RiveScript()
        self.rivebot.load_directory(f"{pathlib.Path(__file__).parent.resolve()}/rive_commands")
        self.rivebot.sort_replies()
        self.web_server = False
        self.speech_module = SpeechModule(self)
        self.smart_modules = {}
        self.motion_triggers = {}
        self.logfile = logfile 
        self.attach_module(SmartModule("devices/bedroomlight.yaml"))

    def attach_module(self, module):
        self.smart_modules[module.id] = module

    def listen(self):
        self.log("Listening for commands...")
        command, module = self.speech_module.process_audio(self.rivebot)
        self.log(f"Received command '{command}' for {self.smart_modules[module].get_pref('type')} '{module}'")
        if module in self.smart_modules:
            self.smart_modules[module].execute(command)
        else:
            self.log(f"Error! '{module}' not present.")
            self.log("Did you feed in the correct configuration file?")

    def log(self, str):
        if self.logfile:
            with open(self.logfile, "a") as f:
                f.write(f"[{datetime.now().strftime('%m/%d/%Y|%H:%M:%S')}]:  {str}\n")
        else:
            print(str)

if __name__ == "__main__":
    controller = SmartController("tmp.log")
    controller.listen()
