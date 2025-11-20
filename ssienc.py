from . import maria_serial_thread as mst
import time
from datetime import datetime

eeprg_help_list = [
    ('ssienc.help()                   ', 'mostra questo menu'),
]

currentPosition = 0
monoflopTime = 0
frcLog = 1
module_com = ""

def help():
    global eeprg_help_list
    for t in eeprg_help_list:
        print(t[0] + t[1])


def dataBits(bits : int):
    global module_com
    if bits <= 0:
        bits = 1

    if bits > 32:
        bits = 32

    mst.ms(module_com, "frcSSIDataSize=%d" % (bits))


def greyDecode( onOff : bool):
    global module_com
    if onOff:
        mst.ms(module_com, "frcSSIGray2bin=1")
    else:
        mst.ms(module_com, "frcSSIGray2bin=0")


def printPollMs(millSecs : int):
    global module_com
    if millSecs < 5:
        millSecs = 5
    if millSecs > 20000:
        millSecs = 20000
    mst.ms(module_com, "frcSSIPrintPollMs=%d" % (millSecs))

def startPos(startStop: bool):
    global module_com
    if startStop:
        print("frcSSIPrint=1")
        mst.ms(module_com, "frcSSIPrint=1")
    else:
        print("frcSSIPrint=0")
        mst.ms(module_com, "frcSSIPrint=0")


def scanPollUs(microSecs : int):
    global module_com
    if microSecs < 100:
        microSecs = 100

    if microSecs > 60000:
        microSecs = 60000

    mst.ms(module_com, "ssiPollPeriod %d" % (microSecs))        


def resetPos():
    global module_com
    mst.ms(module_com, "latchPos")


def countUp( up : bool):
    global module_com
    if up:
        mst.ms(module_com, "upDown 1")
    else:
        mst.ms(module_com, "upDown 0")

def spiFreq( freqKHz : int):
    global module_com
    mst.ms(module_com, "spiClkFreq %d" % freqKHz)

def parseMsg(msg):
    global module_com
    global currentPosition
    global monoflopTime
    #print("parsing: %s" % (msg))
    if msg[0:5] == '[POS:': 
        l = msg[5:].replace(']', '').split()
        currentPosition = int(l[0])
        monoflopTime = int(l[1])
        if frcLog:
            logData()

def logData():
    now = datetime.now()
    ts = datetime.timestamp(now)    # ritorna il timestamp in floating

    fd = open("ssienc_log.txt", 'a', encoding='utf-8')
    s = "%f, %d, %d\n" % (ts, currentPosition, monoflopTime)
    fd.write(s)
    fd.close()

def register(com: str):
    global module_com
    module_com = com
    # register parser callback
    mst.thread_maria_serial_register_parse_callback(com, parseMsg)
    