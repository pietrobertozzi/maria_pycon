import serial
import threading
import time
import datetime

msDict = {}

class MARIA_SERIAL:
    def __init__(self):
        global msList

        self.thread_maria_parse_callbacks = []
        self.ms_ser = None
        self.ms_fGoOn = False
        self.MS_PORT = ""
        self.thr_maria_serial = None

    def thread_maria_serial(self, MS_PORT, MS_BAUDRATE, eofChar):
        """
            Apre la porta seriale e imposta la comunicazione al baudrate desiderato 
            e' possibile indicare il carattere di fine trama tramite il parametro eofChar di tipo bytearray
        """
        global msDict

        self.ms_fGoOn = True
        self.MS_PORT = MS_PORT
        self.ms_ser = serial.Serial(self.MS_PORT, MS_BAUDRATE, timeout=1.0)

        msDict[MS_PORT] = self  # aggiungo l'oggetto al dict con la com come chiave
        i=0

        stringa = ""
        while self.ms_fGoOn:
            c = self.ms_ser.read()
            # print(type(c))
            if len(c):
                if c == eofChar:
                    x = datetime.datetime.now()
                    print("[%s] %s" % (x.strftime('%H:%M:%S.%f'), stringa))
                    self.on_thread_maria_serial_parse(stringa)
                    stringa = ''
                else:
                    try:
                        s = str(c.decode('ascii'))
                    except:
                        pass
                    else:
                        stringa = stringa + s

        if self.ms_ser.is_open:
            self.ms_ser.close()

    def thread_maria_serial_stop(self):
        self.ms_fGoOn = False
        print("stopping thread\n")
        self.thr_maria_serial.join()
        print("thread_maria_serial ended\n")

    def thread_maria_serial_start(self, MS_PORT, MS_BAUDRATE, eofByte=b'\n'):
        """ attiva il thread di ricezione accettando come parametri la porta, il baudrate e il byte di end of frame """
        self.thr_maria_serial = threading.Thread(target=self.thread_maria_serial, args=(MS_PORT, MS_BAUDRATE, eofByte))
        self.thr_maria_serial.start()

    def on_thread_maria_serial_parse(self, msg):
        for functionPtr in self.thread_maria_parse_callbacks:
            functionPtr(msg)

def ms(port, msg, eofStr = '\n'):
    global msDict
    strMsg = msg + eofStr
    msDict[port].ms_ser.write(strMsg.encode('ascii'))

def thread_maria_serial_register_parse_callback(port, functPointer):
    global msDict
    msDict[port].thread_maria_parse_callbacks.append(functPointer)