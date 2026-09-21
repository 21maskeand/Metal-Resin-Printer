import argparse
from lmm_printer.config import load_Config
from lmm_printer.core.print_session import Print_Session

def build_Parser():
    parser = argparse.ArgumentParser(prog = "lmm_printer")
    parser.add_argument("-c" , "--config" , default = "config.yaml" , help = "The name of the yaml format file to use in the config folder. Include extenstion.")
    parser.add_argument("-g" , "--gui" , action = "store_true" , help = "GUI Flag. Defaults to no GUI.")
    parser.add_argument("-l" , "--log" , action = "store_true" , help = "Log Flag. Defaults to no Logs.")
    return parser

if __name__ == "__main__":

    args = build_Parser().parse_args()
    config = load_Config(args.config)
    print_session = Print_Session(args , config)
    print_session.go()

    # if args.gui:
    #     print("No GUI yet.")
    # else:
    #     from lmm_printer.cli_main import main
    #     main(args , config)