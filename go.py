import maria_serial_thread as mst
import atexit
import signal
import sys

import ifc1
#import gufo
#import eeprg

MS_PORT='COM6'
MS_BAUDRATE=115200

#######################################################################
# FUNZIONI    
def mstEnd():
    mst.thread_maria_serial_stop()

def handler(signal_received, frame):
    mstEnd()
    exit(0)    

def off():
    mstEnd()
    exit(0)

#######################################################################
# MAIN

if __name__ == '__main__':
    print("running MAIN\n")

    if len(sys.argv) >= 2:
        MS_PORT = sys.argv[1]

    print("using %s" % (MS_PORT))

    # Tell Python to run the handler() function when SIGINT is recieved
    signal.signal(signal.SIGINT, handler) # ctlr + c
    atexit.register(mstEnd)

    mst.thread_maria_serial_start(MS_PORT, MS_BAUDRATE)


    print("MAIN init end\n")
