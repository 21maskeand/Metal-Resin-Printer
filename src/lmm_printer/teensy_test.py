import serial
import serial.tools.list_ports

TEENSY_VID = 0x16C0

def find_teensy():
    for port in serial.tools.list_ports.comports():
        if port.vid == TEENSY_VID:
            return port.device
        if port.description and "Teensy" in port.description:
            return port.device
    return None

port = find_teensy()
if port is None:
    raise RuntimeError("No Teensy Found")

ser = serial.Serial(port , baudrate = 9600 , timeout = 1)

ser.write(b"H0")