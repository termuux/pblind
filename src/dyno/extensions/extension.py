from dyno.core.coutput import VerboseInterface
from dyno import iengine,oengine

class ParentExtension:
    first_activation = True
    vint = VerboseInterface()

    @classmethod
    def console(cls, text=''):
        cls.vint.info_output(text)
    
    @classmethod
    def response(cls, text):
        oengine.tts_response(text)

    @classmethod
    def user_input(cls):
        user_input = iengine.reco_input(active=True)
        return user_input

    @classmethod
    def extract_tags(cls, vstream, tags):
        try:
            swords = vstream.split()
            tags = tags.split(',')
            return set(swords).intersection(tags)
        except Exception as e:
            cls.vint('Tags extraction error {0}'.format(e))
            return set()
