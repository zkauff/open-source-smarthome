class SpeechModule():
    def __init__(self, caller):
        self.mic = False
        self.caller = caller

    def process_audio(self):
        self.caller.log("Processing your Audio Clip.")
        # TODO 
        return "turn on", "bedroom light"