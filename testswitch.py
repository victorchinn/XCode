import pigpio

# START THE DAEMON FIRST sudo pigpiod

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

BUS = 1

FAC_DEF_SWITCH = 10
HW = pigpio.pi()

# print (HW.get_pigpio_version)

HW.set_mode(FAC_DEF_SWITCH,pigpio.INPUT)

while True:
    print(HW.read(FAC_DEF_SWITCH))



