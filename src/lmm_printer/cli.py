import argparse
from lmm_printer.config import load_Config
from lmm_printer.teensy.establish import return_Teensy_Serial
from lmm_printer.projector.establish import return_Projector
from lmm_printer.core.files import return_RM_Drives , cli_Choose_File
from lmm_printer.core.logs import cli_Log

def build_Parser():
    parser = argparse.ArgumentParser(prog = "lmm_printer")
    parser.add_argument("-c" , "--config" , default = "config.yaml" , help = "The name of the yaml format file to use in the config folder. Include extenstion.")
    parser.add_argument("-g" , "--gui" , action = "store_true" , help = "GUI Flag. Defaults to no GUI.")
    return parser

def run(args , config):
    teensy = return_Teensy_Serial(config["teensy"]["vid"] , config["teensy"]["baudrate"] , config["teensy"]["timeout"] , config["teensy"]["enable_fallback"])
    cli_Log(teensy)
    if teensy.value is None:
        raise SystemExit(1)

    projector = return_Projector(config["projector"]["spi_max_speed"])
    cli_Log(projector)
    if projector.value is None:
        raise SystemExit(1)

    drives = return_RM_Drives()
    cli_Log(drives)
    if drives.value is None:
        raise SystemExit(1)

    file = cli_Choose_File(drives)
    cli_Log(file)

def main():
    args = build_Parser().parse_args()
    config = load_Config(args.config)
    if args.gui:
        print("No GUI yet.")
    else:
        run(args , config)
