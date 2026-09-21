from abc import ABC , abstractmethod

class Generic_Output_Handler(ABC):
    """
    This is the generic output handler which output handlers should inherit from to ensure they function properly.
    """

    @property
    @abstractmethod
    def handle(self , message):
        """
        Takes a message and hands it off to other handle 
        functions based on type or prints an unknown type message.

        Parameters:
            message: The message to be output.
        """
        ...

