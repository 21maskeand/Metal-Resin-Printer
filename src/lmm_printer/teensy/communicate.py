import serial
import serial.tools.list_ports

def find_Teensy_Port(teensy_vid , enable_fallback):
    for port in serial.tools.list_ports.comports():
        if port.vid == teensy_vid:
            return port.device
        if enable_fallback and port.description and "Teensy" in port.description:
            return port.device
    return None

def open_Serial(port , baudrate , timeout):
    return serial.Serial(port , baudrate = baudrate , timeout = timeout)

def is_Teensy_Listening(ser):
    ser.write(b"E hello\n")
    line = ser.readline()
    print(line)
