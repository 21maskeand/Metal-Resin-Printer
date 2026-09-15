from lmm_printer.vendored.UV_projector.controller import DLPC1438

class DLP(DLPC1438):
    def send_numpy_to_buffer(self, pxldata, xoffset, yoffset):  
        '''
        Send an image's pixel data to the inactive buffer at the specified pixel offset
        in x and y.

        Main image display function that takes an 8-bit grayscale image as input, and sends it
        over to the inactive buffer (i.e. the buffer that is not currently received on DMD).
        Image position offsets are specified in pixels. Note that this function does
        not display image sent; it merely loads into into the inactive buffer and requires
        a buffer swap and expose command to actually be used.
        '''

        print("> Sending Image Data over SPI... (SPLIT TECHNIQUE)")

        self.split_spi_transmission(xoffset, yoffset, pxldata)