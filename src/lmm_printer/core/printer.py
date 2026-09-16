

class Printer:
    def __init__(self , teensy , projector , options):
        self.teensy = teensy
        self.projector = projector
        self.options = options

        self.teensy.start_Thread()

        self.listening_for = []

    def home_Axis(self , axis_id):
        command = "H" + str(axis_id)
        self.teensy.send_Command(command)

    def home_Axes(self):
        for i in range(3):
            self.home_Axis(i)