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