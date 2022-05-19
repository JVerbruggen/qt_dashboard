import can

general_bus = can.Bus(interface='serial', channel='/dev/bus/usb/001/001')

while True:
    for msg in bus:
        print(msg.data)