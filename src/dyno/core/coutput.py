import subprocess

from dyno.opt.cverbose import Andromeda

class VerboseInterface:
    def __init__(self):
        pass

    @staticmethod
    def info_output(text):
        print('[+] ' + text)
    

    @staticmethod
    def warn_output(text):
        print('[!] ' + text)

    
    @staticmethod
    def error_output(text):
        print('[-] ' + text)