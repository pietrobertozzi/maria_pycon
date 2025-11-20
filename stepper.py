import maria_serial_thread as mst

stepper_help_list = [
    ('stepper.help()                   ', 'mostra questo menu'),
]

module_com = ""

def help():
    global stepper_help_list
    for t in stepper_help_list:
        print(t[0] + t[1])

def init(mode: int):
    global module_com
    mst.ms(module_com, 'stepperInit %d' % (mode))

def set(steps: int, dir=0):
    global module_com
    mst.ms(module_com, 'stepperSet %d %d' % (steps, dir))

def stat():
    global module_com
    mst.ms(module_com, 'showStat 1')

def parseMsg(msg):
    #print("parsing: %s" % (msg))
    pass # todo:

def register(com: str):
    global module_com
    module_com = com
    # register parser callback
    mst.thread_maria_serial_register_parse_callback(com, parseMsg)
