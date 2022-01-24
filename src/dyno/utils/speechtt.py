import dyno
import json
import pyaudio
from vosk import Model, KaldiRecognizer
from dyno.core.coutput import VerboseInterface


class SpeechText:

    def __init__(self):
        super().__init__()
        self.vint = VerboseInterface()
        self.capture = pyaudio.PyAudio()
        self.model = Model('src/dyno/assets/model')
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.stream = self.capture.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192 ) 
        self.stream.start_stream()

    def reco_input(self, active=False):
        while True:
            input_data = self.stream.read(4096)
            if self.recognizer.AcceptWaveform(input_data):
                text = self.recognizer.Result()
                try:
                    text = json.loads(text)['text'] 
                    self.vint.warn_output(text)
                    identify_action = self.has_action(text)
                    if active or identify_action[0]:
                        text = self.purge_waction(text, identify_action[1])
                        return text 
                except:
                    pass

    @staticmethod
    def has_action(stream):
        if stream:
            stream_in = stream.split()
            for match in dyno.helper:
                if set(stream_in).intersection([match]):
                    return [True,match]
            return [False,None]
        else:
            return [False,None]

    @staticmethod
    def purge_waction(stream, match):
        stream = stream.replace(match, '')
        return stream

