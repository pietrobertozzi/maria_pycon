import maria_serial_thread as mst
import atexit
import signal
from sys import exit

import ifc1

MS_PORT='COM5'
MS_BAUDRATE=115200

#######################################################################
# FUNZIONI    
def mstEnd():
    mst.thread_maria_serial_stop()

def handler(signal_received, frame):
    mstEnd()
    exit(0)    

#######################################################################
# MAIN

if __name__ == '__main__':
    print("running MAIN\n")

    # Tell Python to run the handler() function when SIGINT is recieved
    signal.signal(signal.SIGINT, handler) # ctlr + c
    atexit.register(mstEnd)

    mst.thread_maria_serial_start(MS_PORT, MS_BAUDRATE)


    print("MAIN init end\n")
