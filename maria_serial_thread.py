import serial
import threading
import time
import datetime

thread_maria_parse_callbacks = []

def thread_maria_serial(MS_PORT, MS_BAUDRATE):
    global ms_fGoOn
    global ms_ser
    ms_fGoOn = True
    ms_ser = serial.Serial(MS_PORT, MS_BAUDRATE, timeout=0)

    stringa = ""
    while ms_fGoOn:
        c = ms_ser.read()
        # print(type(c))
        if len(c):
            if c == b'\n':
                x = datetime.datetime.now()
                print("[%s] %s" % (x.strftime('%H:%M:%S.%f'), stringa))
                on_thread_maria_serial_parse(stringa)
                stringa = ''
            else:
                try:
                    s = str(c.decode('utf-8'))
                except:
                    pass
                else:
                    stringa = stringa + s
                


    if ms_ser.is_open:
        ms_ser.close()

def thread_maria_serial_stop():
    global thr_maria_serial
    global ms_fGoOn

    ms_fGoOn = False
    thr_maria_serial.join()
    print("thread_maria_serial ended\n")

def thread_maria_serial_start(MS_PORT, MS_BAUDRATE):
    global thr_maria_serial
    thr_maria_serial = threading.Thread(target=thread_maria_serial, args=(MS_PORT, MS_BAUDRATE))
    thr_maria_serial.start()

def ms(msg):
    global ms_ser
    strMsg = msg + "\n"
    ms_ser.write(strMsg.encode('ascii'))

def on_thread_maria_serial_parse(msg):
    for functionPtr in thread_maria_parse_callbacks:
        functionPtr(msg)

def thread_maria_serial_register_parse_callback( functPointer):
    thread_maria_parse_callbacks.append(functPointer)