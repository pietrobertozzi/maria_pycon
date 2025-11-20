import maria_serial_thread as mst
import time

# int dbgGoDma(void)
# int dbgStopDma(void)
# int dbgSoundOpen(int gufoIdx)
# // rate 0..98
# int dbgSetUltrasound(int rate)
# int dbgSetStrobo(int rate)
# int dbgSetGpio(int port, int pin, int val)
# int reset(void)

gufo_help_list = [
    ('gufo.help()               ', 'mostra questo menu'),
    ('', ''),
    ('gufo.stato()              ', 'mostra lo stato dell\'applicazione'),
    ('gufo.reset()              ', 'soft reset microcontrollore'),
    ('gufo.sdCard()             ', 'test SDCARD'),
]

module_com = ""

def help():
    global gufo_help_list
    for t in gufo_help_list:
        print(t[0] + t[1])

def stato():
    global module_com 
    mst.ms(module_com, 'showStat 2')

def reset():
    mst.ms(module_com, 'reset')

def sdCard():
    mst.ms(module_com, 'dbgSdcard')

def parseMsg(msg):
    #print("parsing: %s" % (msg))
    pass # todo:

def register(com: str):
    global module_com
    module_com = com
    # register parser callback
    mst.thread_maria_serial_register_parse_callback(com, parseMsg)

