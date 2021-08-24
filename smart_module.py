class SmartModule():
    def __init__(self, config_file, caller):
        self.config_file = config_file
        self.caller = caller

    def execute(self, command):
        self.caller.log(f"Executing {command}.")