import maria_serial_thread as mst
import atexit
import signal
import sys
import time

# import ifc1
# import gufo
# import eeprg
import stepper


MS_PORT='COM6'
MS_BAUDRATE=115200
mss=mst.MARIA_SERIAL()

#######################################################################
# FUNZIONI    
def mstEnd():
    # scorro tutto msDict e chiudo le seriali

    for key in mst.msDict:
        mst.msDict[key].thread_maria_serial_stop()
        print('canale %s off' % key)

def handler(signal_received, frame):
    mstEnd()
    #exit(0)    
	
def off():
    mstEnd()
    exit(0)

#######################################################################
# MAIN

if __name__ == '__main__':
    print("running MAIN")
    print("CTRL-C to stop")

    if len(sys.argv) >= 2:
        MS_PORT = sys.argv[1]

    print("using %s" % (MS_PORT))

    # Tell Python to run the handler() function when SIGINT is recieved
    signal.signal(signal.SIGINT, handler) # ctlr + c
    atexit.register(mstEnd)

    mss.thread_maria_serial_start(MS_PORT, MS_BAUDRATE)

    time.sleep(2.0)

    ### registrazione callback parser di risposta
    # ifc1.register(MS_PORT)
    # gufo.register(MS_PORT)
    # eeprg.register(MS_PORT)
    stepper.register(MS_PORT)

    print("MAIN init end")
