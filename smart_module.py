import yaml
import pprint
import importlib # used to dynamically import from our yaml configurations 

class SmartModule():
    def __init__(self, config_file):
        self.config_file = config_file
        self.conf = {}
        with open(config_file, 'r') as stream:
            try: 
                dictionary = yaml.safe_load(stream)
                self.conf = dictionary
            except yaml.YAMLError as exc:
                print(exc)
        if "base_class" in self.conf:
            with open(f"devices/{self.conf['base_class']}.yaml", 'r') as stream:
                try: 
                    self.conf.update(yaml.safe_load(stream))
                except yaml.YAMLError as exc:
                    print(exc)
        print(self.conf)
        # To maintain backwards compatability, expose id and address 
        self.id = self.get_pref("id")
        self.address = self.get_pref("address")
        #TODO: shouldn't need to store the return value... figure out why the statement isn't working
        for to_import in self.get_pref("imports"):
            print(f"importing {to_import}")
            self.conf[to_import] = importlib.import_module(to_import)
        self.execute("setup")

    def execute(self, command):
        print(f"Executing '{command}' on '{self.conf['id']}'.")
        if command in self.get_pref("commands"):
            exec(self.get_command_actions(command))
            print("Correctly executed!")
        else: 
            print("No matching command found. Please try again.")

    def get_pref(self, pref):
        if pref in self.conf.keys():
            return self.conf[pref]
        else:
            print(f"No matching preference for {pref} found!")
            return None

    def get_command_actions(self, command):
        if command in self.get_pref("commands"):
            return self.get_pref("commands")[command]