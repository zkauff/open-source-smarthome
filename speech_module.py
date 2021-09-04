import speech_recognition as sr

class SpeechModule():
    def __init__(self, caller):
        # self.mic = sr.Microphone()
        self.caller = caller
        

    def process_audio(self):
        command = input("Voice commands not setup. Please enter your command here: ")
        #self.caller.log("Processing your Audio Clip.")
        #with self.mic as source:
        #    pass
        # TODO 
        for module in self.caller.smart_modules:
            if module in command:
                return command.replace(module, "").strip(), module
        return None