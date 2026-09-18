import time
import RPi.GPIO as GPIO
from lmm_printer.core.files import save_Dict , load_Dict
from lmm_printer.core.user_inputs import user_Continue
from lmm_printer.core.logs import cli_Log
from lmm_printer.core.types import State
from lmm_printer.utils.vendored_handling import silence


class Printer:
    def __init__(self , teensy , projector , options):
        self.teensy = teensy
        self.projector = projector
        self.options = options

        self.teensy.start_Thread()

        self.listening_for = []

    def home_Axis(self , axis_id , wait = True , listen = True):
        command = "H" + str(axis_id)
        self.teensy.send_Command(command)
        if listen:
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

    def move_Axis_Relative(self , axis_id , move , wait = True , listen = True):
        command = "MR" + str(axis_id) + " " + str(move)
        self.teensy.send_Command(command)
        if listen:
            self.listening_for.append("M" + str(axis_id))
        if wait:
            self.wait_For_Response()

    def move_Axis_Absolute(self , axis_id , move , wait = True , listen = True):
        command = "MA" + str(axis_id) + " " + str(move)
        self.teensy.send_Command(command)
        if listen:
            self.listening_for.append("M" + str(axis_id))
        if wait:
            self.wait_For_Response()

    def move_Axis_To_Top(self , axis_id , wait = True , listen = True):
        command = "MT" + str(axis_id)
        self.teensy.send_Command(command)
        if listen:
            self.listening_for.append("M" + str(axis_id))
        if wait:
            self.wait_For_Response()

    def get_Axis_Position(self , axis_id):
        command = "GP" + str(axis_id)
        self.teensy.send_Command(command)
        self.listening_for.append(command)
        response = self.wait_For_Response()[0]
        pos = float(response.split()[-1])
        return pos

    def set_Axis_Position(self , axis_id , position):
        command = "SP" + str(axis_id) + " " + str(position)
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

    def do_Current_Layer(self , next_image , handler = None):
        while True:
            if handler is not None:
                handler.handle(self)
            if self.check_Heaters():
                break
                
        if handler is not None:
            handler.handle(self)

        self.move_Axis_Relative(0 , self.options["reservoir"]["extrude_multiple"] * self.options["layer_thickness"])
        self.move_Axis_Relative(1 ,-self.options["layer_thickness"])
        self.save_State()

        self.move_Axis_To_Top(2)
        self.save_State()

        self.move_Axis_Relative(0 , -self.options["recoater"]["vertical_pullback"] , wait = False)
        self.move_Axis_Relative(1 , -self.options["recoater"]["vertical_pullback"] , wait = False)
        self.wait_For_Response()
        self.move_Axis_Absolute(2 , 0 , wait = False , listen = False)
        while True:
            recoater_pos = self.get_Axis_Position(2)
            if recoater_pos < self.options["recoater"]["clear_pos"]:
                break

        self.move_Axis_Relative(1 , self.options["recoater"]["vertical_pullback"])
        self.save_State()

        with silence():
            self.projector.swap_buffer()
            exposure_start_time = time.monotonic()
            self.projector.expose_pattern(exposed_frames = int(60 * self.options["exposure_time"]))
            self.projector.send_pixeldata_to_buffer(next_image , 0 , 0)

        while True:
            if handler is not None:
                handler.handle(self)
            if time.monotonic() - exposure_start_time > self.options["exposure_time"]:
                break

        self.listening_for.append("M2")
        self.wait_For_Response()
        self.move_Axis_Relative(0 , self.options["recoater"]["vertical_pullback"])

        self.save_State()

    def wait_For_Response(self , timeout = 60):
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

    def save_State(self , safe_shutdown = False):
        state = self.return_Current_State()
        state["safe_shutdown"] = safe_shutdown
        save_Dict(self.options["files"]["state_file"] , state)

    def load_State(self):
        state_result = load_Dict(self.options["files"]["state_file"])
        state = state_result.value
        for i in range(3):
            self.set_Axis_Position(i , state["pos"][i])

        return state_result

    def safe_Shutdown(self):
        self.save_State(safe_shutdown = True)
        with silence():
            self.projector.stop_exposure()
        self.set_Heater(0 , 0)
        self.set_Heater(1 , 0)
        self.teensy.shutdown()
        GPIO.cleanup()
        



def cli_Preparation(printer):
    user_Continue("Continue to preparation?" , printer = printer)
    
    print("Did any of the axes move since last shutdown?")
    print("Is this the first time running this machine?")
    print("Would you like to home all axes regardless of saved positions?")
    response = input("y for yes to any, n for no to all. ").strip().lower()
    if response == "y":
        user_Continue("Continue to homing?" , printer = printer)
        printer.home_Axes()
        printer.save_State(safe_shutdown = True)

    state_result = printer.load_State()
    cli_Log(state_result)
    if state_result.state == State.ERROR:
        raise SystemExit(1)

    if not state_result.value["safe_shutdown"]:
        response = input("Last update was not safe, Home? y for yes, n for no. ").strip().lower()
        if response == "y":
            printer.home_Axes()
    printer.save_State()

    response = input("Would you like to home a specific axis? y for yes, n for no. ").strip().lower()
    if response == "y":
        print("Enter the axes you want to home one at a time and wait till they are done to continue. Press enter once finished. ")
        while True:
            response = input("").strip()
            if response == "":
                break
            try:
                axis_id = int(response)
                if (axis_id < 0) or (axis_id >= 3):
                    raise ValueError("Axis ID: " + str(axis_id) + " invalid.")
                printer.home_Axis(axis_id)
            except Exception as e:
                print("Error homing axis " + response + ". Error is: " + str(e))

    response = input("Is everything ready to go? y for yes, n for no. ").strip().lower()
    if response != "y":
        response = input("Are you loading new slurry? y for yes, n for no. ").strip().lower()
        if response == "y":
            user_Continue("Unload current slurry / bring the plate to top?" , printer = printer)
            printer.move_Axis_To_Top(0)
            printer.save_State()
            user_Continue("Done placing slurry on plate?" , printer = printer)
            
        response = input("Is the slurry flush with the material plate? y for yes, n for no. ").strip().lower()
        if response != "y":
            print("Adjust the reservoir until the slurry block is flush with the material plate.")
            print("Enter the amount of mm you want the reservoir to move up or down. Press enter once finished. ")
            while True:
                response = input("").strip()
                if response == "":
                    break
                try:
                    move = float(response)
                    printer.move_Axis_Relative(0 , move)
                    printer.save_State()
                except Exception as e:
                    print("Error moving " + response + " mm. Error is: " + str(e))

    printer.save_State()