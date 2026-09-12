import argparse
from lmm_printer.config import load_Config

def build_Parser():
    parser = argparse.ArgumentParser(prog = "lmm_printer")
    parser.add_argument("-g" , "--gui" , default = "y" , help = "Whether or not to launch with gui. 'y' for yes, 'n' for no. DOES NOTHING")
    return parser

def main():
    parser = build_Parser()
    args = parser.parse_args()