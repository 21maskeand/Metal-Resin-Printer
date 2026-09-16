import sys
import threading
import queue

class CLI_Input_Reader:
    def __init__(self):
        self.input_queue = queue.Queue()

    def _reader(self):
        for line in sys.stdin:
            self.input_queue.put(line.rstrip("\n"))

    def get_Input(self):
        lines = []
        while True:
            try:
                lines.append(self.input_queue.get_nowait())
            except queue.Empty:
                break
        return lines

    def clear(self):
        self.get_Input()

    def start_Thread(self):
        threading.Thread(target=self._reader , daemon = True).start()

def _flush_stdin():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import termios
        termios.tcflush(sys.stdin , termios.TCIFLUSH)

def user_Continue(message):
    print("")
    print(message)
    _flush_stdin() # Doesn't really do anything, was here to fix double enter bug, but still needs fixed
    response = input("Press Enter to continue, enter anything else to quit.")
    if response != "":
        cli_Log("Exiting process.")
        raise SystemExit()
    print("")
    print("Successfully continuing.")
    print("")