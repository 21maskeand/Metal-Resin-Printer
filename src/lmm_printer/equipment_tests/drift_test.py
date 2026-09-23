import argparse
import sys
from lmm_printer.config import load_Config
from lmm_printer.core.print_session import Print_Session

def build_Parser():
    parser = argparse.ArgumentParser(prog = "lmm_printer")
    parser.add_argument("-c" , "--config" , default = "config.yaml" , help = "The name of the yaml format file to use in the config folder. Include extenstion.")
    parser.add_argument("-g" , "--gui" , action = "store_true" , help = "GUI Flag. Defaults to no GUI.")
    parser.add_argument("-l" , "--log" , action = "store_true" , help = "Log Flag. Defaults to no Logs.")
    return parser

args = build_Parser().parse_args()
config = load_Config(args.config)
print_session = Print_Session(args , config)
print_session.load_Hardware()
print_session.printer.home_Axes()
print_session.printer.move_Axis_Absolute(0 , 80)


options = {"layer_thickness": .05 , "num_layers": 210}
self = print_session.printer   

def do_Current_Layer_Fast():
    self.move_Axis_Relative(0 , self.config["reservoir"]["extrude_multiple"] * options["layer_thickness"] + self.config["recoater"]["vertical_pullback"] , wait = False)
    self.move_Axis_Relative(1 , -options["layer_thickness"] , wait = False)
    self.wait_For_Response()

    self.move_Axis_Relative(0 , -self.config["recoater"]["vertical_pullback"] , wait = False)
    self.move_Axis_Relative(1 , -self.config["recoater"]["vertical_pullback"] , wait = False)
    self.wait_For_Response()

    self.move_Axis_Relative(1 , self.config["recoater"]["vertical_pullback"])

    self.save_State()

def do_Current_Layer():
    self.move_Axis_Relative(0 , self.config["reservoir"]["extrude_multiple"] * options["layer_thickness"] , wait = False)
    self.move_Axis_Relative(1 , -options["layer_thickness"] , wait = False)
    self.wait_For_Response()

    self.save_State()


for iteration in range(options["num_layers"]):
    
    do_Current_Layer()

    print_session.output_handler.handle("Iteration: " + str(iteration) + " done.")

    if print_session.print_input_handler._line_Ready():
        cmd = sys.stdin.readline().strip().lower()
        if cmd == "end":
            break


print_session.input_handler.suggestion()
while print_session.should_go:
    print_session.input_handler.get_Do_Command(print_session)