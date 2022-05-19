import can
import serial

device = '/dev/ttyUSB0'

bus = can.Bus(interface='serial', channel=device)


def start_can():
    while True:
        print("loop")
        for msg in bus:
            print("for")
            print(msg.data)

def start_serial():
    with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
        while True:
            x = ser.readline()
            print(x)

start_serial()