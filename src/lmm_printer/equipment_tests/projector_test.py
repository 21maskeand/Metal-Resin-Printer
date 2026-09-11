import RPi.GPIO as GPIO
import time
import numpy as np
import smbus  # I2C
import spidev  # SPI
from lmm_printer.vendored.UV_projector.controller import DLPC1438, Mode


GPIO.setmode(GPIO.BCM)

try:

    # Initialize I2C (SMBus) on channel 1
    i2c = smbus.SMBus(1)

    # Initialise SPI (bus 0, with CE0 as chip select pin)
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 125000000  # FPGA/DCLP1438 limit: 50 MB/s; 125MHz seems limit for Pi zero 1W
    spi.mode = 3 

    # Initialise the DLPC1438
    DMD = DLPC1438(i2c, spi)


    # let's try external print mode now
    DMD.configure_external_print(LED_PWM = 1000)
    DMD.switch_mode(Mode.EXTERNALPRINT)

    # intialise FPGA buffers to zero
    DMD.set_background(intensity = 0, both_buffers = True)

    # Send an image, where the raspberry pi determines the exposure time
    DMD.send_image_to_buffer('media/openMLA_logo_1280x720.png', 0,0)  # send the image data into FPGA buffer over SPI
    DMD.swap_buffer()
    DMD.expose_pattern(exposed_frames = 10*60)  # infinite exposure time, until we send the stop_exposure() command
    DMD.send_image_to_buffer('media/openMLA_logo_2560x1440.png', 0,0)
    time.sleep(10)
    DMD.swap_buffer()
    DMD.expose_pattern(exposed_frames = 10*60)  # infinite exposure time, until we send the stop_exposure() command
    time.sleep(10)

except KeyboardInterrupt:
    GPIO.cleanup()