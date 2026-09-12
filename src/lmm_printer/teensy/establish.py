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
    line = ser.readline().decode("utf-8")
    line = ' '.join(line.split())
    return line == "hello"

def return_Teensy_Serial(teensy_vid , baudrate , timeout , enable_fallback):
    port = find_Teensy_Port(teensy_vid , False)
    if port is None:
        print("No Teensy port found.")
        return None

    try:
        ser = open_Serial(port , baudrate , timeout)   
    except Exception as e:
        print("Error opening the serial port:", port , "Error was:")
        print(e)
        return None

    if is_Teensy_Listening(ser):
        return ser
    else:
        print("Teensy not listening.")
        return None

