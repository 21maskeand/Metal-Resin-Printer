import argparse
from time import sleep
from lmm_printer.config import load_Config
from lmm_printer.teensy.establish import return_Teensy_Serial
from lmm_printer.projector.establish import return_Projector
from lmm_printer.core.files import return_RM_Drives , cli_Choose_File
from lmm_printer.core.logs import cli_Log
from lmm_printer.core.types import Print_File , State
from lmm_printer.core.user_inputs import CLI_Input_Reader , user_Continue
from lmm_printer.core.printer import Printer

def build_Parser():
    parser = argparse.ArgumentParser(prog = "lmm_printer")
    parser.add_argument("-c" , "--config" , default = "config.yaml" , help = "The name of the yaml format file to use in the config folder. Include extenstion.")
    parser.add_argument("-g" , "--gui" , action = "store_true" , help = "GUI Flag. Defaults to no GUI.")
    return parser



def run(args , config):
    teensy_result = return_Teensy_Serial(config["teensy"]["vid"] , config["teensy"]["baudrate"] , config["teensy"]["timeout"] , config["teensy"]["enable_fallback"])
    cli_Log(teensy_result)
    if teensy_result.state == State.ERROR:
        raise SystemExit(1)
    teensy = teensy_result.value

    projector_result = return_Projector(config["projector"]["spi_max_speed"])
    cli_Log(projector_result)
    if projector_result.state == State.ERROR:
        raise SystemExit(1)
    projector = projector_result.value

    drives_result = return_RM_Drives()
    cli_Log(drives_result)
    if drives_result.state == State.ERROR:
        raise SystemExit(1)
    drives = drives_result.value

    file_result = cli_Choose_File(drives)
    cli_Log(file_result)
    file = file_result.value

    with Print_File(file) as print_file:
        num_layers = print_file.get_Num_Layers()
        image_result = print_file.get_Image(round(num_layers*.75))
        options_result = print_file.get_Options()
    
    print_file_error = False
    if image_result.state == State.ERROR:
        cli_Log(image_result)
        print_file_error = True
    if options_result.state == State.ERROR:
        cli_Log(options_result)
        print_file_error = True
    if print_file_error:
        raise SystemExit(1)

    options = options_result.value

    printer = Printer(teensy , projector , options)

    user_Continue("Continue to homing?")
    printer.home_Axes()





    reader = CLI_Input_Reader()
    reader.start_Thread()



        


    

def main():
    args = build_Parser().parse_args()
    config = load_Config(args.config)
    if args.gui:
        print("No GUI yet.")
    else:
        run(args , config)
