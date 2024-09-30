from . import maria_serial_thread as mst
import time

eeprg_help_list = [
    ('eeprg.help()                   ', 'mostra questo menu'),
    ('', ''),
    ('eeprg.stato()                  ', 'mostra l\'elenco delle immagini EEPROM'),
    ('eeprg.eepromProgramAndVerify() ', 'programma la EEPROM con l\'immagine selezionata'),
    ('eeprg.selectEepromImage(idx)   ', 'seleziona l\'immagine da programmare'),
]

def help():
    global eeprg_help_list
    for t in eeprg_help_list:
        print(t[0] + t[1])

def stato():
    mst.ms('showStat 2')

def eepromProgramAndVerify():
    mst.ms('eepromProgramAndVerify')

def selectEepromImage( idx ):
    mst.ms('selectEepromImage %d' % (idx))

def parseMsg(msg):
    #print("parsing: %s" % (msg))
    pass # todo:

# register parser callback
mst.thread_maria_serial_register_parse_callback(parseMsg)

