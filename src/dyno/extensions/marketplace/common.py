from dyno.extensions.extension import ParentExtension
import dyno

class Maintain(ParentExtension):
    @classmethod
    def stop_speech(cls, **kwargs):
        dyno.oengine.pspeak = True
        
