from . import maria_serial_thread as mst
import time
from datetime import datetime

eeprg_help_list = [
    ('ssienc.help()                   ', 'mostra questo menu'),
]

currentPosition = 0
monoflopTime = 0
frcLog = 1

def help():
    global eeprg_help_list
    for t in eeprg_help_list:
        print(t[0] + t[1])


def dataBits(bits : int):
    if bits <= 0:
        bits = 1

    if bits > 32:
        bits = 32

    mst.ms("frcSSIDataSize=%d" % (bits))


def greyDecode( onOff : bool):
    if onOff:
        mst.ms("frcSSIGray2bin=1")
    else:
        mst.ms("frcSSIGray2bin=0")


def printPollMs(millSecs : int):
    if millSecs < 5:
        millSecs = 5
    if millSecs > 20000:
        millSecs = 20000
    mst.ms("frcSSIPrintPollMs=%d" % (millSecs))

def startPos(startStop: bool):
    if startStop:
        print("frcSSIPrint=1")
        mst.ms("frcSSIPrint=1")
    else:
        print("frcSSIPrint=0")
        mst.ms("frcSSIPrint=0")


def scanPollUs(microSecs : int):
    if microSecs < 100:
        microSecs = 100

    if microSecs > 60000:
        microSecs = 60000

    mst.ms("ssiPollPeriod %d" % (microSecs))        


def resetPos():
    mst.ms("latchPos")


def countUp( up : bool):
    if up:
        mst.ms("upDown 1")
    else:
        mst.ms("upDown 0")

def spiFreq( freqKHz : int):
    mst.ms("spiClkFreq %d" % freqKHz)

def parseMsg(msg):
    global currentPosition
    global monoflopTime
    #print("parsing: %s" % (msg))
    if msg[0:5] == '[POS:': 
        l = msg[5:].replace(']', '').split()
        currentPosition = int(l[0])
        monoflopTime = int(l[1])
        if frcLog:
            logData()

# register parser callback
mst.thread_maria_serial_register_parse_callback(parseMsg)

def logData():
    now = datetime.now()
    ts = datetime.timestamp(now)    # ritorna il timestamp in floating

    fd = open("ssienc_log.txt", 'a', encoding='utf-8')
    s = "%f, %d, %d\n" % (ts, currentPosition, monoflopTime)
    fd.write(s)
    fd.close()