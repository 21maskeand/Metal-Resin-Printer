from lmm_printer.core.types import Result , State

def cli_Log(result):
    if isinstance(result , Result):
        print(result.message)
    elif isinstance(result , str):
        print(result)
    else:
        print("Unknown log type.")