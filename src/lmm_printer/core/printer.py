import time

class Printer:
    def __init__(self , teensy , projector , options):
        self.teensy = teensy
        self.projector = projector
        self.options = options

        self.teensy.start_Thread()

        self.listening_for = []

    def home_Axis(self , axis_id , wait = True):
        command = "H" + str(axis_id)
        self.teensy.send_Command(command)
        self.listening_for.append(command)
        if wait:
            self.wait_For_Response()

    def home_Axes(self , ids = None):
        if ids is None:
            for i in range(3):
                self.home_Axis(i)
        else:
            for i in ids:
                self.home_Axis(i)

    def move_Axis_Relative(self , axis_id , move , wait = True):
        command = "MR" + str(axis_id) + " " + str(move)
        self.teensy.send_Command(command)
        self.listening_for.append("M" + str(axis_id))
        if wait:
            self.wait_For_Response()

    def move_Axis_To_Top(self , axis_id , wait = True):
        command = "MT" + str(axis_id)
        self.teensy.send_Command(command)
        self.listening_for.append("M" + str(axis_id))
        if wait:
            self.wait_For_Response()

    def get_Temp(self , probe_id):
        command = "RT" + str(probe_id)
        self.teensy.send_Command(command)
        self.listening_for.append(command)
        response = self.wait_For_Response()[0]
        temp = float(response.split()[-1])
        return temp

    def set_Heater(self , heater_id , temp):
        command = "SH" + str(heater_id) + " " + str(temp)    
        self.teensy.send_Command(command)
    
    def start_Heaters(self):
        self.set_Heater(0 , self.options["chamber"]["temp"])
        self.set_chamber_temp = self.options["chamber"]["temp"]

        self.set_Heater(1 , self.options["recoater"]["temp"])
        self.set_recoater_temp = self.options["recoater"]["temp"]

    def check_Heaters(self):
        chamber_good = False
        recoater_good = False

        chamber_temp = self.get_Temp(0)
        recoater_temp = self.get_Temp(2)

        if (self.set_chamber_temp != self.options["chamber"]["temp"]) or (self.set_recoater_temp != self.options["recoater"]["temp"]):
            self.start_Heaters()
        
        if self.set_chamber_temp - self.options["chamber"]["valid_diff"] <= chamber_temp <= self.set_chamber_temp + self.options["chamber"]["valid_diff"]:
            chamber_good = True
        if self.set_recoater_temp - self.options["recoater"]["valid_diff"] <= recoater_temp <= self.set_recoater_temp + self.options["recoater"]["valid_diff"]:
            recoater_good = True

        if chamber_good and recoater_good:
            return True
        else:
            return False


    def wait_For_Response(self , timeout = 60*2):
        return_list = []
        start = time.monotonic()
        while len(self.listening_for) != 0:
            if time.monotonic() - start > timeout:
                raise TimeoutError("Teensy never responded to one of these: " + str(self.listening_for))
            messages = self.teensy.get_Messages()
            for lf in list(self.listening_for):
                responses = [s for s in messages if lf in s]
                if responses:
                    response = responses[0]
                    while lf in self.listening_for:
                        self.listening_for.remove(lf)
                    return_list.append(response)
            time.sleep(.005)
        return return_list