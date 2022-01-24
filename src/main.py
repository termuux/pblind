from dyno import config
from dyno.tools.connection import check_connection
from dyno.core.compute import Compute
from dyno.core.coutput import VerboseInterface

def main():
    vint = VerboseInterface()
    vint.info_output('Starting ... ')
    check_connection()
    vint.info_output('Booted ...')
    computer = Compute(vint, config)

    while True:
        computer.execute()

if __name__ == '__main__':
    main()
