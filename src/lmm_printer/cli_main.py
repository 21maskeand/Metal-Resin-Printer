from time import sleep , monotonic
from platformdirs import user_state_path
from lmm_printer.teensy.establish import return_Teensy_Serial
from lmm_printer.projector.establish import return_Projector
from lmm_printer.core.files import return_RM_Drives , cli_Choose_File
from lmm_printer.core.logs import cli_Log
from lmm_printer.core.types import Print_File , State
from lmm_printer.core.user_inputs import CLI_Input_Handler , user_Continue
from lmm_printer.core.printer import Printer , cli_Preparation
from lmm_printer.utils.vendored_handling import silence

def cli_Run(args , config):
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
    options = options | config
    state_dir = user_state_path(config["files"]["app_name"] , ensure_exists = True)
    state_file = state_dir / (config["files"]["state_file_name"] + ".json")
    options["files"]["state_file"] = state_file

    printer = Printer(teensy , projector , options)

    cli_Preparation(printer)

    user_Continue("Start print of: " + str(file) + " ?"  , printer = printer)

    printer.start_Heaters()

    handler = CLI_Input_Handler()
    handler.start_Thread()
    
    for i in range(1 , num_layers + 1):
        with Print_File(file) as print_file:
            if i == num_layers:
                next_image = None
            else:
                next_image = print_file.get_Image(i + 1).value
                
            if i == 1:
                this_image = print_file.get_Image(i).value
                with silence():
                    printer.projector.send_pixeldata_to_buffer(this_image , 0 , 0)

        start_time = monotonic()
        printer.do_Current_Layer(next_image , handler = handler)
        end_time = monotonic()
        cli_Log("Layer " + str(i) + " done. Took: " + str(end_time - start_time) + " seconds.")


def main(args , config):
    cli_Run(args , config)
