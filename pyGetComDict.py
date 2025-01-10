import winreg as wrg 

def getComDict() -> dict :
    """ costruisce un dictionary contenente le informazioni relative alle porte seriali del computer.
        le informazioni vengono raccolte accedendo al registry e sono restituite nella forma
    
        {'COM7':  ['\\Device\\USBSER001', 'STMicroelectronics STLink Virtual COM Port (COM7)',  'VID_0483&PID_374B&MI_02']
         'COM10': ['\\Device\\USBSER000', 'STMicroelectronics STLink Virtual COM Port (COM10)', 'VID_0483&PID_374B&MI_02']}
        ...
    """
    location = wrg.HKEY_LOCAL_MACHINE


    comDict = {}

    serialcommKey = wrg.OpenKeyEx(location, "HARDWARE\\DEVICEMAP\\SERIALCOMM")
    if serialcommKey:
        # QueryInfoKey ritorna una tupla (nSubkeys, nvalues, timestamp)
        value = wrg.QueryInfoKey(serialcommKey)
        nSerialComm = value[1]
        for i in range(nSerialComm):
            data = wrg.EnumValue(serialcommKey, i)
            #print(f'data = {data}')
            comDict[data[1]] = [data[0], '', '']
        
        wrg.CloseKey(serialcommKey)

    usbKey = wrg.OpenKeyEx(location, "SYSTEM\\ControlSet001\\Enum\\USB")
    if usbKey:
        # QueryInfoKey ritorna una tupla (nSubkeys, nvalues, timestamp)
        value = wrg.QueryInfoKey(usbKey)
        nUsbDevices = value[0]
        for i in range(nUsbDevices):
            vidpidKeyString = wrg.EnumKey(usbKey, i)
            #print(vidpidKeyString)
            vidpidkey = wrg.OpenKeyEx(location, "SYSTEM\\ControlSet001\\Enum\\USB\\%s" % str(vidpidKeyString))
            if vidpidkey:
                value = wrg.QueryInfoKey(vidpidkey)
                nUsbDevicesSameVidPid = value[0]
                for j in range(nUsbDevicesSameVidPid):
                    serialNumberKeyString =  wrg.EnumKey(vidpidkey, j)
                    #print("    %s" % serialNumberKeyString)

                    serviceVal = ''
                    friendlyName = ''
                    portName = ''
                    serialNumberKey = wrg.OpenKeyEx(location, "SYSTEM\\ControlSet001\\Enum\\USB\\%s\\%s" % (str(vidpidKeyString), str(serialNumberKeyString)))
                    if serialNumberKey:
                        try:
                            serviceVal = wrg.QueryValueEx(serialNumberKey, 'Service')[0]
                            friendlyName = wrg.QueryValueEx(serialNumberKey, 'FriendlyName')[0]
                        except:
                            pass

                        # serviceVak dipende dal driver installato e da come si registra nel registry
                        if serviceVal == 'usbser' or serviceVal == 'CH341SER_A64':
                            deviceParameterKey = wrg.OpenKeyEx(location, "SYSTEM\\ControlSet001\\Enum\\USB\\%s\\%s\\Device parameters" % (str(vidpidKeyString), str(serialNumberKeyString)))

                            if deviceParameterKey:
                                portName = wrg.QueryValueEx(deviceParameterKey, 'PortName')[0]
                                #print("            %s" % (portName))
                                wrg.CloseKey(deviceParameterKey)   
                                
                        # attiva questa print per sapere il valore di serviceVal con cui si e' registrato il driver della seriale USB
                        #print("         %s -> %s %s" % (serviceVal, friendlyName, portName))
                        if portName in comDict:
                            comDict[portName][1] = friendlyName
                            comDict[portName][2] = vidpidKeyString
            
                        wrg.CloseKey(serialNumberKey)

                wrg.CloseKey(vidpidkey)

        wrg.CloseKey(usbKey)
    return comDict

if __name__ == '__main__' :
    # module test
    comDict = getComDict()
    for port in comDict:
        print( f'{port} {comDict[port]}')
