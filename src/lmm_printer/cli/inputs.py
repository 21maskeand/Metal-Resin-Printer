import sys , select
from lmm_printer.core.types import Result , State

class Input_Handler:
    def suggestion(self):
        print("")
        print("Enter 'help' for a list of commands. ")

    def ask_Yes_No(self , message):
        print("")
        print(message)
        print("'y' for yes, 'n' for no. ")
        while True:
            response = input("").strip().lower()
            if response == "y":
                return True
            elif response == "n":
                return False
            else:
                print("Enter 'y' or 'n'. ")

    def wait_To_Continue(self , message):
        print("")
        print(message)
        print("Press Enter to continue. ")
        while True:
            response = input("").strip().lower()
            if response == "":
                return
            else:
                print("Invalid entry. ")

    def help(self):
        print("")
        print("help: Prints this message. ")
        print("choose file: Enter the file select menu. ")
        print("quit: Quits the program safely. ")
        print("home: Enter the home menu. ")
        print("move: Enter the move menu. ")
        print("get pos: Gets the position of an axis. ")
        print("print: Prints selected file. ")

    def choose_File(self , print_session):
        from lmm_printer.core.files import return_RM_Drives , get_Files
        from pathlib import Path

        print("")
        drives_result = return_RM_Drives()
        print_session.output_handler.handle(drives_result)
        if drives_result.state == State.ERROR:
            return
        drives = drives_result.value

        file_names , file_mnts = get_Files(drives)
        print("Available Files: ")
        print(file_names)

        print("")
        response = input("Choose file by entering name.extension or press enter to return to command selection. ")

        if response.strip() == "":
            return
        else:
            response = response.strip()
            if response in file_names:
                index = file_names.index(response)
                mnt = file_mnts[index]
                file_result = Result(value = Path(mnt) / response , state = State.SUCCESS , message = "Successfully chose file: " + response + ", at mount: " + mnt + ".")
            else:
                print("File name invalid.")
                return self.choose_File(print_session)
        
        print_session.output_handler.handle(file_result)
        print_session.file = file_result.value
        print_session.load_Print_File_Attributes()

    def quit(self , print_session):
        if print_session.hardware_good:
            print_session.printer.safe_Shutdown()
        raise SystemExit(1)

    def home(self , print_session):
        print("")
        print("Enter 'all' to home all axes. Enter axis number to home that axis. Press enter when finished.")
        print("Enter the axes you want to home one at a time and wait till they are done to continue. Enter 'all' to home all. Press enter once finished. ")
        while True:
            response = input("").strip()
            if response == "":
                break
            elif response == "all":
                print_session.printer.home_Axes() 
                print_session.printer.save_State()
                break
            try:
                axis_id = int(response)
                if (axis_id < 0) or (axis_id >= 3):
                    print_session.output_handler.handle("Axis ID: " + str(axis_id) + " invalid.")
                    continue
                print_session.printer.home_Axis(axis_id)
                print_session.printer.save_State()
            except Exception as e:
                print("Error homing axis " + response + ". Error is: " + str(e))

    def relative(self , print_session , axis_id):
        print("")
        print("Enter the amount of mm you want the axis to move up or down. Press Enter to return. ")
        while True:
            response = input("").strip()
            if response == "":
                break
            try:
                move = float(response)
                print_session.printer.move_Axis_Relative(axis_id , move)
                print_session.printer.save_State()
            except Exception as e:
                print_session.output_handler.handle("Error moving " + response + " mm. Error is: " + str(e))

    def absolute(self , print_session , axis_id):
        print("")
        print("Enter the position you want the axis to move to. Press Enter to return. ")
        while True:
            response = input("").strip()
            if response == "":
                break
            try:
                move = float(response)
                print_session.printer.move_Axis_Absolute(axis_id , move)
                print_session.printer.save_State()
            except Exception as e:
                print("Error moving " + response + " mm. Error is: " + str(e))

    def move(self , print_session):
        while True:
            print("")
            print("Enter the axis to move. Press Enter to return")
            response = input("").strip().lower()
            if response == "":
                break
            try:
                axis_id = int(response)
                if (axis_id < 0) or (axis_id >= 3):
                    print_session.output_handler.handle("Axis ID: " + str(axis_id) + " out of bounds.")
                    continue
                print("")
                print("top: Move axis to its maximum. ")
                print("relative: Move axis relative to current position in mm. ")
                print("absolute: Move axis relative to current position in mm. ")
                response = input("").strip().lower()
                if response == "top":
                    print_session.printer.move_Axis_To_Top(axis_id)
                    print_session.printer.save_State()
                elif response == "relative":
                    self.relative(print_session , axis_id)
                elif response == "absolute":
                    self.absolute(print_session , axis_id)
                else:
                    print("Invalid command. ")
            except Exception as e:
                print_session.output_handler.handle("Error moving axis. Error was: " + str(e))

    def get_Pos(self , print_session):
        print("")
        print("Enter the axis number to see its position. Press enter when finished.")
        while True:
            response = input("").strip()
            if response == "":
                break
            try:
                axis_id = int(response)
                if (axis_id < 0) or (axis_id >= 3):
                    print_session.output_handler.handle("Axis ID: " + str(axis_id) + " invalid.")
                    continue
                pos = print_session.printer.get_Axis_Position(axis_id)
                print_session.output_handler.handle("Position of axis " + str(axis_id) + " is " + str(pos))
            except Exception as e:
                print("Error checking position of axis " + response + ". Error is: " + str(e))

    def print(self , print_session):
        print_session.print()

    def get_Do_Command(self , print_session):
        print("")
        response = input("Enter Command: ").strip().lower()

        if response == "help":
            self.help()
        elif response == "choose file":
            self.choose_File(print_session)
        elif response == "quit":
            self.quit(print_session)
        elif response == "home":
            self.home(print_session)
        elif response == "move":
            self.move(print_session)
        elif response == "get pos":
            self.get_Pos(print_session)
        elif response == "print":
            self.print(print_session)


class Print_Input_Handler:
    def suggestion(self):
        print("Enter h at any time for a list of commands. ")

    def clear(self):
        self.get_Inputs()

    def dispatch(self , inp , print_session):
        if inp == "h":
            print("")
            print("h: Prints this message.")
            print("p: Pauses the printer.")
            print("q: Safely quits the process.")
            print("Note - neither pausing nor quitting will stop axes from completing their current move.")
            print("")

        elif inp == "p":
            print("Enter r to resume.")
            while True:
                response = input("").strip().lower()
                if response == "r":
                    break
                    
        elif inp == "q":
            from lmm_printer.utils.vendored_handling import silence
            print("Shutting down.")
            print_session.printer.save_State()
            with silence():
                print_session.printer.projector.stop_exposure()
            print_session.printer.set_Heater(0 , 0)
            print_session.printer.set_Heater(1 , 0)
            print_session.stop_print = True
            
    def line_Ready(self):
        return select.select([sys.stdin] , [] , [] , 0)[0] != []

    def handle(self , print_session):
        while self.line_Ready():
            cmd = sys.stdin.readline().strip().lower()
            self.dispatch(cmd , print_session)