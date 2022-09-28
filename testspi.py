import pigpio
import time

# START THE DAEMON FIRST sudo pigpiod


# GPIO2 is SDA
# GPIO3 is SCL

INPUT_PORT = 0x00
OUTPUT_PORT = 0x01
POL_INV = 0x02
CONFIG = 0x03
ZEROES = 0x00
ALL_ONES = 0xFF
RELAY_ONE = 0x01
RELAY_TWO = 0x02
RELAY_BOTH = 0x03

BUS = 1

FAC_DEF_SWITCH = 10
SPI_MOSI= 19    # DATA BIT
SPI_CLOCK = 21  # CLOCK EACH BIT INTO REGISTER
SPI_LOAD = 20   # LOAD THE BARGRAPH REGISTER

HIGH=1
LOW=0

def spi_mosi_high():
    HW.write(SPI_MOSI,HIGH)

def spi_mosi_low():
    HW.write(SPI_MOSI,LOW)

def toggle_spi_clock():
    HW.write(SPI_CLOCK, LOW)
    time.sleep(0.001)
    HW.write(SPI_CLOCK, HIGH)
    time.sleep(0.0010)
    HW.write(SPI_CLOCK, LOW)
    
def bar_graph_load():
    HW.write(SPI_LOAD,HIGH)
    time.sleep(0.0010)
    HW.write(SPI_LOAD,LOW)
    time.sleep(0.0010)
    HW.write(SPI_LOAD,HIGH)

if __name__ == "__main__":

    HW = pigpio.pi()

    # print (HW.get_pigpio_version)

    HW.set_mode(SPI_MOSI, pigpio.OUTPUT)
    HW.set_mode(SPI_CLOCK, pigpio.OUTPUT)
    HW.set_mode(SPI_LOAD, pigpio.OUTPUT)


    while True:

        spi_mosi_low()
        toggle_spi_clock()

        spi_mosi_low()
        toggle_spi_clock()

        spi_mosi_low()
        toggle_spi_clock()

        spi_mosi_low()
        toggle_spi_clock()

        spi_mosi_high()
        toggle_spi_clock()

        spi_mosi_high()
        toggle_spi_clock()

        spi_mosi_high()
        toggle_spi_clock()

        spi_mosi_high()
        toggle_spi_clock()

        spi_mosi_low()
        toggle_spi_clock()

        spi_mosi_low()
        toggle_spi_clock()

        spi_mosi_low()
        toggle_spi_clock()

        spi_mosi_low()
        toggle_spi_clock()

        spi_mosi_high()
        toggle_spi_clock()

        spi_mosi_high()
        toggle_spi_clock()

        spi_mosi_high()
        toggle_spi_clock()

        spi_mosi_high()
        toggle_spi_clock()

        spi_mosi_low()
        toggle_spi_clock()

        spi_mosi_low()
        toggle_spi_clock()

        spi_mosi_low()
        toggle_spi_clock()

        spi_mosi_high()
        toggle_spi_clock()

        spi_mosi_high()
        toggle_spi_clock()

        bar_graph_load()


