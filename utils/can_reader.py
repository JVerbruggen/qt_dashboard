import can

bus = can.Bus(interface='serial', channel='/dev/ttyUSB0')

while True:
    print("loop")
    for msg in bus:
        print("for")
        print(msg.data)