import maria_serial_thread as mst

# BOARD POWERIO ----------------------------------------------------------
# frcGPIOPP 0            # blocco completamente la macchina a stati
# testMax7300 0 0 0      # max7300 write/read reg
# testMax7300 4 0 0      # Dump Max7300
# testMax7300 5 0 0      # Test INPUTS
# testMax7300 3 X 1 B    # RELAY B.X ON
# testMax7300 3 X 0 B    # RELAY B.X OFF
# testMax7300 6 4 0 B    # read board B inputs

# BOARD INPUTSOUTPUTS ----------------------------------------------------
# frcGPIOPP 0            # blocco completamente la macchina a stati
# testMcp2317 0 0 0     # mcp2317 write/read reg
# testMcp2317 1 0 0     # mcp2317 dump
# testMcp2317 2 0 0     # mcp2317 input self-test

# BOARD POWER ------------------------------------------------------------
# frcGPIOPP 0           # blocco completamente la macchina a stati
# testLtc4151 0 0 0     # Ltc4151 write/read reg
# testLtc4151 1 0 0     # Ltc4151 dump
# testLtc4151 2 0 0     # Ltc4151 measures
# testPca59536D 0 0 0   # Pca59536D write/read reg
# testPca59536D 1 0 0   # dump Pca59536D regs
# testPca59536D 2 0 1   # set pin0
# testPca59536D 3 0 0   # Pca59536D read Pins

# SISTEMA ----------------------------------------------------------------
# showStat 1            # SYSTEM status
# showStat 2 0          # CENTRALINA status
# showStat 2 1          # SCHEDE status
# showStat 2 2          # ZONE status
# showStat 2 3          # I/O status
# showStat 3 x          # IFDx status
# reset 
# frcLogOff 1           # stop log
# showEnv 2             # CENTRALINA configurazione
# envLoad               # carica configurazione da codice micro
# envWrite              # Salva Configrazione in EXTFLASH
# dbgFlashLl 0, 0       # FLASH Write/Read
# dbgFlashLl 1, 0       # FLASH erase

# frcGPIOPP
# frcLogModbus
# frcLogOff
# frcProfile
# frcStopInputRefresh


# BOARD ANALOG ------------------------------------------------------------
# testMcp3428 1 0       # Read Inputs



help_list = [
    ('help', 'mostra questo menu'),
    ('GPIOPP_ll()', 'Mette il sistema in LOW-LEVEL test mode'),
    ('GPIOPP_ml()', 'Mette il sistema in MEDIUM-LEVEL test mode'),
    ('GPIOPP_hl()', 'Mette il sistema in RUN mode'),
    ('modbusDump(on)', 'Attiva/disattiva il dump dei pacchetti modbus'),
]

def help():
    global help_list
    for t in help_list:
        print(t[0] +'\t' + t[1])

def GPIOPP_ll():
    mst.ms('frcGPIOPP 0')

def GPIOPP_ml():
    mst.ms('frcGPIOPP 3')

def GPIOPP_hl():
    mst.ms('frcGPIOPP 0xFFFF')

def modbusDump(on):
    mst.ms('frcLogModbus '+ str(on))