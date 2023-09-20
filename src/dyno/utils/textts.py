import threading
import pyttsx3
import queue

from dyno.core.coutput import VerboseInterface

class TextToSpeech:
   

    def __init__(self):
        self.tts = self.set_voice()

    def run_voice(self):
        try:
            self.tts.runAndWait()
        except RuntimeError:
            pass

    @staticmethod
    def set_voice():
        
        tts = pyttsx3.init()
        tts.setProperty('rate', 160) 
        tts.setProperty('volume', 1.0) 
        return tts


class TexttsEngine(TextToSpeech):
    def __init__(self):
        super().__init__()
        self.mqueue = queue.Queue(maxsize=9) 
        self.pspeak = False
        self.vint = VerboseInterface()

    
    def tts_response(self, message):
        self.insert_mqueue(message)
        try:
            speecht = threading.Thread(target=self.sverbose)
            speecht.start()
        except RuntimeError as e:
            self.vint.error_output('Threading error ... {0}'.format(e))
            
    def insert_mqueue(self, message):
        try:
            self.pspeak = False
            self.mqueue.put(message)
        except Exception as e:
            self.vint.error_output('Queing error ... {0}'.format(e))

    def sverbose(self):
        try:
            while not self.mqueue.empty():
                cbatch = ''
                message = self.mqueue.get()
                if message:
                    batches = self.create_tbatches(rtext=message)
                    for batch in batches:
                        self.tts.say(batch)
                        cbatch += batch
                        self.vint.info_output(cbatch)
                        self.run_voice()
                        if self.pspeak:
                            self.vint.warn_output('Interrupting Speech ...')
                            self.pseak = False
                            break
        except Exception as e:
            self.vint.error_output(e)

    @staticmethod
    def create_tbatches(rtext, nwords=8):
        rtext = rtext + ' '
        lbatches = []
        twords = rtext.count(' ')
        lid = 0

        for split in range(0, int(twords / nwords)):
            batch = ''
            wcount = 0
            while wcount < nwords:
                batch += rtext[lid]
                if rtext[lid] == ' ':
                    wcount += 1
                lid += 1
            lbatches.append(batch)

        if lid < len(rtext): 
            lbatches.append(rtext[lid:])
        return lbatches
