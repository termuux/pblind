import sys
import time
from datetime import datetime

from dyno.extensions.extension import ParentExtension
from dyno.tools.acsound import pacsound

class Activation(ParentExtension):
    @classmethod
    def eassistant(cls, **kwargs):
        pacsound()

    @classmethod
    def dassistant(cls, **kwargs):
        cls.response('Shutting Down')
        time.sleep(1)
        cls.console('Process Terminated Successfully')
        sys.exit()

    @classmethod
    def agreet(cls, **kwargs):
        now = datetime.now()
        ctime = int(now.strftime('%H'))

        if ctime < 12:
            cls.response('Hello there, Good Morning.')
        elif 12 <= day_time < 18:
            cls.response('Hello there, Good Afternoon')
        else:
            cls.response('Hello there, Good Evening')
