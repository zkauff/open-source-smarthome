# Base controller class
# Author : zkauff

from rivescript import RiveScript
import pathlib

class SmartController():
    def __init__(self):
        self.rivebot = RiveScript()
        self.rivebot.load_directory(f"{pathlib.Path(__file__).parent.resolve()}/rive_commands")
        print("Starting Execution.")

controller = SmartController()
