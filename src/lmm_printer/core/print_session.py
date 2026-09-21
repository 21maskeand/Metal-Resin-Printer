from lmm_printer.core.types import State

class Print_Session:
    def __init__(self , args , config):
        self.args = args
        self.config = config
        self.add_State_File_To_Config()
        self.file_good = False
        self.stop_print = False
        self.should_go = True

        if args.gui:
            print("No GUI yet")
        else:
            self.load_CLI()

    def load_CLI(self):
        from lmm_printer.cli.inputs import Input_Handler , Print_Input_Handler
        from lmm_printer.cli.outputs import Output_Handler

        self.input_handler = Input_Handler()
        self.print_input_handler = Print_Input_Handler()
        self.output_handler = Output_Handler(self.args , self.config)

    def add_State_File_To_Config(self):
        from platformdirs import user_state_path

        state_dir = user_state_path(self.config["files"]["app_name"] , ensure_exists = True)
        state_file = state_dir / (self.config["files"]["state_file_name"] + ".json")
        self.config["files"]["state_file"] = state_file

    def load_Hardware(self):
        from lmm_printer.teensy.establish import return_Teensy_Serial
        from lmm_printer.projector.establish import return_Projector
        from lmm_printer.core.printer import Printer

        teensy_result = return_Teensy_Serial(self.config["teensy"]["vid"] , self.config["teensy"]["baudrate"] , self.config["teensy"]["timeout"] , self.config["teensy"]["enable_fallback"])
        self.output_handler.handle(teensy_result)
        if teensy_result.state == State.ERROR:
            teensy_loaded = False
        else:
            teensy_loaded = True
        teensy = teensy_result.value

        projector_result = return_Projector(self.config["projector"]["spi_max_speed"])
        self.output_handler.handle(projector_result)
        if projector_result.state == State.ERROR:
            projector_loaded = False
        else:
            projector_loaded = True
        projector = projector_result.value

        if teensy_loaded and projector_loaded:
            self.printer = Printer(teensy , projector , self.config)
            state = self.printer.load_State()
            if not state.safe_shutdown:
                self.output_handler.handle("Last shutdown was not safe. Ensure you home if you do not trust the axes' positions. ")
            else:
                self.output_handler.handle("Ensure you trust the axes' positions before starting.Home if you do not. ")
            self.hardware_good = True
        else:
            self.hardware_good = False

    def load_Print_File_Attributes(self):
        from lmm_printer.core.types import Print_File

        if not hasattr(self , "file"):
            self.output_handler.handle("Choose a file first. ")
            return
        with Print_File(self.file) as print_file:
            num_layers = print_file.get_Num_Layers()
            image_result = print_file.get_Image(round(num_layers*.75))
            options_result = print_file.get_Options()
        
        print_file_error = False
        if image_result.state == State.ERROR:
            self.output_handler.handle(image_result)
            print_file_error = True
        if options_result.state == State.ERROR:
            self.output_handler.handle(options_result)
            print_file_error = True
        if print_file_error:
            return

        self.num_layers = num_layers
        self.options = options_result.value
        self.file_good = True

    def print(self):
        from time import monotonic
        from lmm_printer.core.types import Print_File
        from lmm_printer.utils.vendored_handling import silence

        if not self.hardware_good:
            self.output_handler.handle("Cannot start a print with bad hardware or connection. ")
            return
        if not self.file_good:
            self.output_handler.handle("You must load a file before printing. ")
            return
        
        self.print_input_handler.suggestion()
        self.printer.start_Heaters()
        for i in range(1 , self.num_layers + 1):
            while True:
                self.print_input_handler.handle(self)
                if self.printer.check_Heaters():
                    break
            self.print_input_handler.handle(self)
            if self.stop_print:
                self.stop_print = False
                return
            with Print_File(self.file) as print_file:
                if i == self.num_layers:
                    next_image = None
                else:
                    next_image = print_file.get_Image(i + 1).value
                    
                if i == 1:
                    this_image = print_file.get_Image(i).value
                    with silence():
                        self.printer.projector.send_pixeldata_to_buffer(this_image , 0 , 0)

            start_time = monotonic()
            self.printer.do_Current_Layer(next_image , self.options)
            end_time = monotonic()
            self.output_handler.handle("Layer " + str(i) + " done. Took: " + str(end_time - start_time) + " seconds.")
        
    def go(self):
        self.load_Hardware()
        self.input_handler.suggestion()
        while self.should_go:
            self.input_handler.get_Do_Command(self)