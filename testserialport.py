import pigpio
import time

SECTION_0_ADDR = 0x20

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

GPIO_14 = 14
GPIO_15 = 15
FAC_DEF_SWITCH = 10


BUS = 1

HW = pigpio.pi()

# print (HW.get_pigpio_version)f

# HW.set_mode(GPIO_14,pigpio.OUTPUT)
# HW.set_mode(GPIO_15,pigpio.ALT0)

handle = HW.serial_open("/dev/ttyAMA0", 9600)
print (HW.serial_data_available(handle))


while True:
    #HW.write(GPIO_14,1)
    #time.sleep(0.10)
    #HW.write(GPIO_14,0)
    #time.sleep(0.10)
    HW.serial_write(handle, "SC\r\n"  )
    answer = HW.serial_read(handle)






