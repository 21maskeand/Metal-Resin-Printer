from lmm_printer.core.types import Result , State

class Non_Logger:
    """
    This is the non logger, which is a logger that does not log.
    """

    def log(*args , **kwargs):
        """
        This is the non loggers log function, it takes anything as input and does nothing but return.
        """

        return

class Output_Handler:
    """
    The main CLI output handler. Just prints and logs outputs.

    Parameters:
        args (dict): Dict of passed arguments.
        config (dict): Dict representation of the config file.
    """

    def __init__(self , args , config):
        self.args = args
        self.config = config

        if args.log:
            print("No Logging yet")
        else:
            self.logger = Non_Logger()

    def handle(self , message):
        """
        Takes a message and hands it off to other handle 
        functions based on type or prints an unknown type message.

        Parameters:
            message: The message to be output.
        """

        if isinstance(message , str):
            self.handle_String(message)
        elif isinstance(message , Result):
            self.handle_Result(message)
        else:
            self.handle_Unknown_Type(message)

    def handle_String(self , message):
        """
        Prints and logs a string message.

        Parameters:
            message (str): Message to be printed and logged.
        """

        print("")
        print(message)
        self.logger.log(message)

    def handle_Result(self , message):
        """
        Prints the message associated with the Result type and logs the result.

        Parameters:
            message (Result): The message result to be printed and logged.
        """

        print("")
        print(message.message)
        self.logger.log(message)

    def handle_Unknown_Type(self , message):
        """
        Handles unknown types by logging and printing an error message. Which contains the message.

        Parameters:
            message: The message to be printed and logged.
        """

        print("")
        error_message = "Output: " + str(message) + " has unknown output type. "
        logger.log(error_message)
        print(error_message)
