import argparse
from time import sleep
from lmm_printer.config import load_Config
from lmm_printer.teensy.establish import return_Teensy_Serial
from lmm_printer.projector.establish import return_Projector
from lmm_printer.core.files import return_RM_Drives , cli_Choose_File
from lmm_printer.core.logs import cli_Log
from lmm_printer.core.types import Print_File , State
from lmm_printer.core.user_inputs import CLI_Input_Reader
from lmm_printer.core import printer

def build_Parser():
    parser = argparse.ArgumentParser(prog = "lmm_printer")
    parser.add_argument("-c" , "--config" , default = "config.yaml" , help = "The name of the yaml format file to use in the config folder. Include extenstion.")
    parser.add_argument("-g" , "--gui" , action = "store_true" , help = "GUI Flag. Defaults to no GUI.")
    return parser



def run(args , config):
    teensy = return_Teensy_Serial(config["teensy"]["vid"] , config["teensy"]["baudrate"] , config["teensy"]["timeout"] , config["teensy"]["enable_fallback"])
    cli_Log(teensy)
    if teensy.state == State.ERROR:
        raise SystemExit(1)

    projector = return_Projector(config["projector"]["spi_max_speed"])
    cli_Log(projector)
    if projector.state == State.ERROR:
        raise SystemExit(1)

    drives = return_RM_Drives()
    cli_Log(drives)
    if drives.state == State.ERROR:
        raise SystemExit(1)

    file = cli_Choose_File(drives)
    cli_Log(file)

    with Print_File(file.value) as print_file:
        num_layers = print_file.get_Num_Layers()
        image = print_file.get_Image(round(num_layers*.75))
        options = print_file.get_Options()
    
    print_file_error = False
    if image.state == State.ERROR:
        cli_Log(image)
        print_file_error = True
    if options.state == State.ERROR:
        cli_Log(options)
        print_file_error = True
    if print_file_error:
        raise SystemExit(1)

    response = input("Press Enter to start, enter anything else to quit.").strip()
    if response != "":
        cli_Log("Exiting process.")
        raise SystemExit()

    reader = CLI_Input_Reader()
    reader.start_Thread()

    printer.home_Axis(teensy.value , 0)


        


    

def main():
    args = build_Parser().parse_args()
    config = load_Config(args.config)
    if args.gui:
        print("No GUI yet.")
    else:
        run(args , config)
