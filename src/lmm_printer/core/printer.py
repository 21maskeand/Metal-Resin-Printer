

def home_Axis(ser , axis_id):
    command_string = "H" + str(axis_id) + "\n"
    command_string = command_string.encode()
    ser.write(command_string)

def home_Axes(ser):
    for i in range(3):
        home_Axis(ser , i)