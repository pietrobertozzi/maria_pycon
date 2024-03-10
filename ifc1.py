import maria_serial_thread as mst
import time

# BOARD POWERIO ----------------------------------------------------------
### frcGPIOPP 0            # blocco completamente la macchina a stati
# testMax7300 0 0 0      # max7300 write/read reg
# testMax7300 4 0 0      # Dump Max7300
# testMax7300 5 0 0      # Test INPUTS
# testMax7300 3 X 1 B    # RELAY B.X ON
# testMax7300 3 X 0 B    # RELAY B.X OFF
# testMax7300 6 4 0 B    # read board B inputs

# BOARD INPUTSOUTPUTS ----------------------------------------------------
### frcGPIOPP 0            # blocco completamente la macchina a stati
# testMcp2317 0 0 0     # mcp2317 write/read reg
# testMcp2317 1 0 0     # mcp2317 dump
# testMcp2317 2 0 0     # mcp2317 input self-test

# BOARD POWER ------------------------------------------------------------
### frcGPIOPP 0           # blocco completamente la macchina a stati
# testLtc4151 0 0 0     # Ltc4151 write/read reg
# testLtc4151 1 0 0     # Ltc4151 dump
# testLtc4151 2 0 0     # Ltc4151 measures
# testPca59536D 0 0 0   # Pca59536D write/read reg
# testPca59536D 1 0 0   # dump Pca59536D regs
# testPca59536D 2 0 1   # set pin0
# testPca59536D 3 0 0   # Pca59536D read Pins

# SISTEMA ----------------------------------------------------------------
### showStat 1            # SYSTEM status
### showStat 2 0          # CENTRALINA status
### showStat 2 1          # SCHEDE status
### showStat 2 2          # ZONE status
### showStat 2 3          # I/O status
### showStat 3 x          # IFDx status
### reset 
# frcLogOff 1           # stop log
### showEnv 2             # CENTRALINA configurazione
### envLoad               # carica configurazione da codice micro
### envWrite              # Salva Configrazione in EXTFLASH
# dbgFlashLl 0, 0       # FLASH Write/Read
# dbgFlashLl 1, 0       # FLASH erase

### frcGPIOPP
### frcLogModbus
# frcLogOff
# frcProfile
# frcStopInputRefresh

# BOARD ANALOG ------------------------------------------------------------
# testMcp3428 1 0       # Read Inputs

ifc1_help_list = [
    ('ifc1.help                  ', 'mostra questo menu'),
    ('', ''),
    ('----- HARDWARE', ''),
    ('mst.ms(\'showI2C\')        ', 'I2C scan'),
    ('', ''),
    ('----- MACCHINA A STATI PRINCIPALE', ''),
    ('ifc1.GPIOPP_ll()           ', 'Mette il sistema in LOW-LEVEL test mode (BLOCCO IN/FSM/OUT)'),
    ('ifc1.GPIOPP_ml()           ', 'Mette il sistema in MEDIUM-LEVEL test mode (BLOCCO FSM)'),
    ('ifc1.GPIOPP_hl()           ', 'Mette il sistema in RUN mode'),
    ('ifc1.GPIOPP_noOut()        ', 'Mette il sistema in RUN mode ma non gestisce gli output (BLOCCO OUT)'),
    ('', ''),
    ('----- TEST IN LOW LEVEL', ''),
    ('ifc1.LL_OUT(idx, val)      ', 'controlla singolo output di indice idx (solo schede POWER-OUTPUTS)'),
    ('', ''),
    ('----- TEST IN MEDIUM LEVEL', ''),
    ('ifc1.ML_OUT(idx, val)      ', 'controlla singolo output di indice idx'),
    ('ifc1.ML_IN(idx, val)       ', 'forza singolo input di indice idx'),
    ('', ''),
    ('----- VISUALIZZAZIONE LIVE ', ''),
    ('ifc1.modbusDump(on)        ', 'Attiva/disattiva il dump dei pacchetti modbus'),
    ('ifc1.diagDump(on)          ', 'Attiva/disattiva il dump dei messaggi DIAGNOSTICA'),
    ('ifc1.logOn(on)             ', 'Attiva/disattiva log'),
    ('', ''),
    ('----- SISTEMA              ', ''),
    ('ifc1.reset()               ', 'Reboot centralina'),
    ('ifc1.nuovaConfigurazione() ', 'Carica e attiva la nuova configurazione'),
    ('', ''),
    ('ifc1.environment()         ', 'Mostra onfigurazione impianto'),
    ('ifc1.stato()               ', 'Mostra stato Centralina'),
    ('ifc1.statoSchede()         ', 'Mostra stato delle schede'),
    ('ifc1.statoZone()           ', 'Mostra stato delle zone'),
    ('ifc1.statoIO()             ', 'Mostra stato degli INPUTS/OUTPUTS'),
    ('ifc1.statoIFD1(n)          ', 'Mostra stato del rilevatore con indirizzo modbus n'),
]

def help():
    global ifc1_help_list
    for t in ifc1_help_list:
        print(t[0] + t[1])

def GPIOPP_ll():
    mst.ms('frcGPIOPP 0')

def GPIOPP_ml():
    mst.ms('frcGPIOPP 3')

def GPIOPP_hl():
    mst.ms('frcGPIOPP 0xFFFF')

def GPIOPP_noOut():
    mst.ms('frcGPIOPP 0x1D')

def modbusDump(on):
    mst.ms('frcLogModbus '+ str(on))

def diagDump(on):
    mst.ms('frcLogDiag '+ str(on))

def logOn(on):
    off = 1
    if on:
        off = 0
    mst.ms('frcLogOff '+ str(off))

def reset():
    mst.ms('reset')

def nuovaConfigurazione():
    mst.ms('envLoad')
    time.sleep(1.0)  # pausa di un secondo
    mst.ms('envWrite')
    reset()

def environment():
    mst.ms('showEnv 2')

def stato():
    mst.ms('showStat 1')
    time.sleep(0.3)
    mst.ms('showStat 2 0')

def statoSchede():
    mst.ms('showStat 2 1')

def statoZone():
    mst.ms('showStat 2 2')

def statoIO():
    mst.ms('showStat 2 3')

def statoIFD1(ifd1Idx):
    mst.ms('showStat 3 ' + str(ifd1Idx))

def ML_OUT(idx, val):
    mst.ms('dbgSetOutputVal(' + str(idx) + ',' + str(val) + ')')

def LL_OUT(idx, val):
    if idx in [64, 65, 66, 67, 68]:
        # scheda output-power 0
        ioAddr = idx - 64
        mst.ms("testMax7300( 3, %d, %d, 0 )" % (ioAddr, val))
    elif idx in [69, 70, 71, 72, 73]:
        # scheda output-power 1
        ioAddr = idx - 69
        mst.ms("testMax7300( 3, %d, %d, 1 )" % (ioAddr, val))
    else:
        print('per controllare gli OUTPUTS delle schede I/O utilizzare il test di medio livello')

def ML_IN(idx, val)
    mst.ms("dbgSetInputVal(%d, %d)" % idx, val)
