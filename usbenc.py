from . import maria_serial_thread as mst
import time

programmingCommands = [
    #  cmdString      INC
    ( '@w00B1EA',	   8 ),
    ( '@w01702A',	  10 ),
    ( '@w02302B',	  16 ),
    ( '@w03F1EB',	  20 ),
    ( '@w04B029',	  25 ),
    ( '@w0571E9',	  32 ),
    ( '@w0631E8',	  40 ),
    ( '@w07F028',	  50 ),
    ( '@w08B02C',	  64 ),
    ( '@w0971EC',	  80 ),
    ( '@w0A71CE',	 100 ),
    ( '@w0B31CF',	 125 ),
    ( '@w0CF00F',	 128 ),
    ( '@w0DB1CD',	 200 ),
    ( '@w0E700D',	 250 ),
    ( '@w0F300C',	 256 ),
    ( '@w10B07A',	 400 ),
    ( '@w1171BA',	 500 ),
    ( '@w1231BB',	 512 ),
    ( '@w13F07B',	1024 ),
    ( '@w14B1B9',	2048 ),
    ( '@w157079',      0 ),
    ( '@w163078',      0 ),
    ( '@w17F1B8',      0 ),
    ( '@w18B1BC',      0 ),
    ( '@w19707C',      0 ),
    ( '@w1A705E',      0 ),
    ( '@w1B305F',      0 ),
    ( '@w1CF19F',      0 ),
    ( '@w1DB05D',      0 ),
    ( '@w1E719D',      0 ),
    ( '@w1F319C',      0 ),
]

eeprg_help_list = [
    ('usbenc.help()                   ', 'mostra questo menu'),
    ('', ''),
    ('usbenc.stato()                  ', 'mostra la programmazione corrente'),
    ('usbenc.usbProgram()             ', 'programma la EEPROM con la risoluzione desiderata'),
]

module_com = ""
currentSelectionIdx = -1

def help():
    global eeprg_help_list
    for t in eeprg_help_list:
        print(t[0] + t[1])

def stato() -> int:
    global currentSelectionIdx
    global module_com
    print('@i')
    mst.ms(module_com, '@i', '\r')
    return currentSelectionIdx      


def usbProgram(resolutionCode):
    global currentSelectionIdx
    global module_com
    mst.ms(programmingCommands[resolutionCode][0], '\r')
    time.sleep(1)
    mst.ms(module_com, '@x', '\r')
    currentSelectionIdx = -1

def parseMsg(msg):
    global currentSelectionIdx
    print("parsing: %s" % (msg))

    if(msg[0:3] == '@ir'):
        # risposta a richiesta di stato [e.g. @ir0D ]
        currentSelectionIdx = int(msg[3:5], 16)       # estraggo la parte numerica e la converto da hex a int
        print(currentSelectionIdx)

def register(com: str):
    global module_com
    module_com = com
    # register parser callback
    mst.thread_maria_serial_register_parse_callback(com, parseMsg)

