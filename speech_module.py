import speech_recognition as sr
import queue
import sounddevice as sd
import vosk
import sys
import json

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

class SpeechModule():
    def __init__(self, caller, model="model", device=None):
        self.model = vosk.Model(model)
        self.device = device
        self.device_info = sd.query_devices(device, 'input')
        self.samplerate = int(self.device_info['default_samplerate'])
        self.caller = caller

    def process_audio(self, rivebot, audio=True):
        cmds_to_return = []
        modules_to_return = []
        if audio:
            with sd.RawInputStream(
                    samplerate=self.samplerate, 
                    blocksize = 8000,
                    device=self.device,
                    dtype='int16',
                    channels=1,
                    callback=callback):
                print('-' * 80)
                print('now recording. press Ctrl+C to stop')
                print('-' * 80)
                rec = vosk.KaldiRecognizer(self.model, self.samplerate)
                while True:
                    data = q.get()
                    if rec.AcceptWaveform(data):
                        commands = json.loads(rec.Result())["text"].split("and")
                        print(commands)
                        brk = False
                        for command in commands:
                            print(f"Heard '{command}'")
                            command = rivebot.reply("localuser", command)
                            print(f"Parsed command: '{command}'")
                            for module in self.caller.smart_modules:
                                if module in command:
                                    cmds_to_return.append(command.replace(module, "").strip())
                                    modules_to_return.append(module)
                                    brk = True
                            if command and self.caller.text_to_speech and not brk and "didn't catch that" not in command:
                                self.caller.voice_response("Sorry, I didn't quite catch that.")
                        if brk:
                            break
        else:
            commands = input("Voice commands not setup. Please enter your command here: ").split("and")
            for command in commands:
                print(f"Heard '{command}'")
                command = rivebot.reply("localuser", command)
                print(f"Parsed command: '{command}'")
                brk = False
                for module in self.caller.smart_modules:
                    if module in command:
                        cmds_to_return.append(command.replace(module, "").strip())
                        modules_to_return.append(module)
                        brk = True
        return cmds_to_return, modules_to_return
