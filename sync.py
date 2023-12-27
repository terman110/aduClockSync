#!/usr/bin/python
import sys
import glob
import serial
import syslog
import time
from datetime import datetime

# import serial.tools.list_ports
# ports = serial.tools.list_ports.comports()
# for port, desc, hwid in sorted(ports):
#     print("{}: {} [{}]".format(port, desc, hwid))

def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
        result = []
        for port in ports:
            try:
                with serial.Serial(port) as ser:
                    result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    return ports


if __name__ == '__main__':
    print(serial_ports())

    # The following line is for serial over GPIO
    port = '/dev/ttyUSB0'

    try:
        now = datetime.now()
        print("Port: " + port)
        print("Current time: " + now.strftime("%H:%M:%S"))
        strNow = now.strftime("%H%M%S#")
        print("Sending string: " + strNow)

        with serial.Serial(port, 9600, timeout=5) as ser:
            # print(ser.name)
            time.sleep(5)
            while ser.in_waiting:
                print(str(ser.readline(), 'utf-8').replace("\r", "").replace("\n", ""))
            print(strNow.encode('utf-8'))
            ser.write(strNow.encode('utf-8'))
            time.sleep(1)
            while ser.in_waiting:
                string = str(ser.readline(), 'utf-8').replace("\r", "").replace("\n", "")
                print(string)
                if string == "OK":
                    exit(0)
            exit(2)

    except (OSError, serial.SerialException) as e:
        print("Error:")
        print(e)
        exit(1)