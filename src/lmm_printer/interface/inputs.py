from abc import ABC , abstractmethod

class Generic_Input_Handler(ABC):
    """
    The generic input handler all others inherit from. Enforces the creation of certain methods used in Print_Session methods.
    """

    @property
    @abstractmethod
    def suggestion(self):
            """
            Prints a helpful suggestion.
            """
            ...

    @property
    @abstractmethod
    def ask_Yes_No(self , message):
        """
        Asks a yes no question to the user.

        Parameters:
            message (str): The question to be asked.

        Returns:
            bool: True if the answer was yes, False if the answer was no. 
        """
        ...

    @property
    @abstractmethod
    def wait_To_Continue(self , message):
        """
        Prints a message and waits until for the user to continue.

        Parameters:
            message (str): The message to be printed.
        """
        ...

    @property
    @abstractmethod
    def get_Do_Command(self , print_session):
        """
        Queries the user for a command and then does it.

        Parameters:
            print_session (Print_Session): The print session to act upon.
        """
        ...


class Generic_Print_Input_Handler(ABC):
    """
    This is the generic print input handler.
    """

    @property
    @abstractmethod
    def suggestion(self):
        """
        Prints a helpful suggestion.
        """
        ...

    @property
    @abstractmethod
    def handle(self , print_session):
        """
        Handles the inputs while print_session is printing.
        """
        ...
