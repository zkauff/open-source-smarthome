# Base controller class
# Author : zkauff

from rivescript import RiveScript
import pathlib
from speech_module import SpeechModule
from datetime import datetime

class SmartController():
    def __init__(self, logfile=None):
        self.rivebot = RiveScript()
        self.rivebot.load_directory(f"{pathlib.Path(__file__).parent.resolve()}/rive_commands")
        self.web_server = False
        self.speech_module = SpeechModule(self)
        self.smart_modules = {}
        self.logfile = logfile 

    def attach_module(self, module, module_configuration):
        self.smart_modules[module.id] = module_configuration

    def listen(self):
        self.log("Listening for commands...")
        self.log(self.speech_module.process_audio())

    def log(self, str):
        if self.logfile:
            with open(self.logfile, "a") as f:
                f.write(f"[{datetime.now().strftime('%m/%d/%Y|%H:%M:%S')}]:  {str}\n")
        else:
            print(str)

if __name__ == "__main__":
    controller = SmartController("tmp.log")
    controller.listen()