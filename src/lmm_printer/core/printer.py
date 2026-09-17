import time
from lmm_printer.core.files import save_Dict , load_Dict

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

    def home_Axes(self , ids = None , one_at_a_time = False):
        if ids is None:
            for i in range(3):
                self.home_Axis(i , one_at_a_time)
        else:
            for i in ids:
                self.home_Axis(i , one_at_a_time)
        if not one_at_a_time:
            self.wait_For_Response()

    def move_Axis_Relative(self , axis_id , move , wait = True):
        command = "MR" + str(axis_id) + " " + str(move)
        self.teensy.send_Command(command)
        self.listening_for.append("M" + str(axis_id))
        if wait:
            self.wait_For_Response()

    def move_Axis_Absolute(self , axis_id , move , wait = True):
        command = "MA" + str(axis_id) + " " + str(move)
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

    def get_Axis_Position(self , axis_id):
        command = "GP" + str(probe_id)
        self.teensy.send_Command(command)
        self.teensy.listening_for.append(command)
        response = self.wait_For_Response()[0]
        pos = float(response.split()[-1])
        return pos

    def set_Axis_Position(self , axis_id , position , wait = True):
        command = "SP" + str(probe_id) + " " + str(position)
        self.teensy.send_Command(command)

    def get_Temp(self , probe_id):
        command = "GT" + str(probe_id)
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

    def do__Current_Layer(next_image):
        while True:
            if self.check_Heaters():
                break

        self.move_Axis_Relative(0 ,-options["reservoir"]["extrude_multiple"] * options["layer_thickness"])
        self.move_Axis_Relative(1 , options["layer_thickness"])

        self.move_Axis_To_Top(2)

        self.projector.swap_buffer()
        start_time = time.monotonic()
        self.projector.expose_pattern(exposed_frames = 60 * options["exposure_time"])
        self.projector.send_pixeldata_to_buffer(next_image)
        while True:
            if time.monotonic() - start_time > options["exposure_time"]:
                break

        self.move_Axis_Relative(0 , -options["layer_thickness"])
        self.move_Axis_Relative(1 , -options["layer_thickness"])
        self.move_Axis_Absolute(2 , 0)
        self.move_Axis_Relative(0 , options["layer_thickness"])
        self.move_Axis_Relative(1 , options["layer_thickness"])


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

    def return_Current_State(self):
        pos = []
        for i in range(3):
            pos.append(self.get_Axis_Position(i))

        state = {"pos": pos}
        return state

    def save_State(self):
        state = self.return_Current_State()
        save_Dict(self.options["files"]["state_file"] , state)

    def load_State(self):
        state_result = load_Dict(self.options["files"]["state_file"])
        state = state_result.value
        for i in range(3):
            self.set_Axis_Position(i , state["pos"][i])

        return state_result
