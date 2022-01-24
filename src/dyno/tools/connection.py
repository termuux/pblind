import requests
from dyno.core import coutput

def check_connection(url='https://google.com', timeout=3):
    cout = coutput.VerboseInterface()

    try:
        cout.info_output('Checking whether cloud connection exists')
        connection = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        cout.info_output('Connection is not available.')
        cout.warn_output('You may experience issues with speech recognition and synthesis')
        return False

        