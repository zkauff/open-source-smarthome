import yaml
import pprint

class SmartModule():
    def __init__(self, config_file, caller):
        self.config_file = config_file
        self.caller = caller
        self.conf = {}
        with open(config_file, 'r') as stream:
            try: 
                dictionary = yaml.safe_load(stream)
                self.conf = dictionary
            except yaml.YAMLError as exc:
                print(exc)
        pprint.PrettyPrinter(indent=4).pprint(self.__dict__)
        self.id = self.conf["id"]

    def execute(self, command):
        self.caller.log(f"Executing '{command}' on '{self.conf['id']}''.")
        if command in self.get_pref("commands"):
            print("Correctly executed!")
        else: 
            print("No matching command found. Please try again.")

    def get_pref(self, pref):
        if pref in self.conf.keys():
            return self.conf[pref]
        else:
            print("No matching preference found!")
            return None