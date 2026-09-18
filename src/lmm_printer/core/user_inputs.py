import sys
import threading
import queue
from lmm_printer.core.logs import cli_Log

class CLI_Input_Handler:
    def __init__(self):
        self.input_queue = queue.Queue()
        self._stop = threading.Event()
        print("Enter h at any time for a list of commands. ")

    def _reader(self):
        while not self._stop.is_set():
            for line in sys.stdin:
                self.input_queue.put(line.rstrip("\n").strip().lower())

    def get_Inputs(self):
        lines = []
        while True:
            try:
                lines.append(self.input_queue.get_nowait())
            except queue.Empty:
                break
        return lines

    def clear(self):
        self.get_Inputs()

    def dispatch(self , inp , printer):
        if inp == "h":
            print("")
            print("h: Prints this message.")
            print("p: Pauses the printer.")
            print("q: Safely quits the process.")
            print("Note - neither pausing nor quitting will stop axes from completing their current move.")
            print("")

        elif inp == "p":
            print("Enter r to resume.")
            while True:
                response = input("").strip().lower()
                if response == "r":
                    break

        elif inp == "q":
            print("Shutting down.")
            printer.safe_Shutdown()
            raise SystemExit(1)

    def handle(self , printer):
        inputs = self.get_Inputs()
        for inp in inputs:
            self.dispatch(inp , printer)

    def start_Thread(self):
        if getattr(self , '_thread' , None) and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._reader , daemon = True)
        self._thread.start()

    def stop_Thread(self):
        self._stop.set()
        self._thread.join()

def user_Continue(message , printer = None):
    print("")
    print(message)
    response = input("Press Enter to continue, enter anything else to quit. ")
    if response != "":
        cli_Log("Exiting process.")
        if printer is not None:
            printer.safe_Shutdown()
        raise SystemExit(1)
    print("")
    print("Successfully continuing.")
    print("")