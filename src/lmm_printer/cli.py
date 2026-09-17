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

    options["chamber"] = {}
    options["chamber"]["temp"] = config["chamber"]["temp"]
    options["chamber"]["valid_diff"] = config["chamber"]["valid_diff"]
    options["recoater"] = {}
    options["recoater"]["temp"] = config["recoater"]["temp"]
    options["recoater"]["valid_diff"] = config["recoater"]["valid_diff"]
    options["reservoir"] = {}
    options["reservoir"]["extrude_multiple"] = config["reservoir"]["extrude_multiple"]

    printer = Printer(teensy , projector , options)

    user_Continue("Continue to homing?")
    
    response = input("Is everything already homed? y for yes, Enter elsewise. ").strip().lower()
    if response != "y":
        printer.home_Axes()
    

    response = input("Are you loading new slurry? y for yes, Enter elsewise. ")
    if response.strip().lower() == "y":
        printer.move_Axis_To_Top(0)
        user_Continue("Done loading slurry?")
    
    print("Adjust the reservoir until the slurry block is flush with the material plate.")
    print("Enter the amount of mm you want the reservoir to move up or down. Press enter once finished. ")
    while True:
        response = input("").strip()
        if response == "":
            break
        try:
            move = float(response)
            printer.move_Axis_Relative(0 , move)
        except Exception as e:
            print("Error moving " + response + " mm. Error is: " + str(e))

    user_Continue("Start print of: " + str(file) + " ?")

    printer.start_Heaters()
    
    for i in range(1 , num_layers + 1):
        with Print_File(file) as print_file:
            if i == num_layers:
                next_image = None
            else:
                next_image = print_file.get_Image(i + 1).value
                
            if i == 1:
                this_image = print_file.get_Image(i).value
                printer.projector.send_pixeldata_to_buffer(this_image)

        printer.do_Current_Layer(next_image)
        cli_Log("Layer " + str(i) + " done.")



    reader = CLI_Input_Reader()
    reader.start_Thread()



        


    

def main():
    args = build_Parser().parse_args()
    config = load_Config(args.config)
    if args.gui:
        print("No GUI yet.")
    else:
        run(args , config)
