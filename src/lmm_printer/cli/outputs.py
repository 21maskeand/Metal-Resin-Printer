from lmm_printer.core.types import Result , State

class Non_Logger:
    def log(*args , **kwargs):
        return

class Output_Handler:
    def __init__(self , args , config):
        self.args = args
        self.config = config

        if args.log:
            print("No Logging yet")
        else:
            self.logger = Non_Logger()

    def handle(self , message):
        if isinstance(message , str):
            self.handle_String(message)
        elif isinstance(message , Result):
            self.handle_Result(message)
        else:
            self.handle_Unknown_Type(message)

    def handle_String(self , message):
        print("")
        print(message)
        self.logger.log(message)

    def handle_Result(self , message):
        print("")
        print(message.message)
        self.logger.log(message)

    def handle_Unknown_Type(self , message):
        print("")
        error_message = "Output: " + str(message) + " has unknown output type. "
        logger.log(error_message)
        raise TypeError(error_message)
