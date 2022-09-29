#!/usr/bin/env python

import time

# Parser CLASS


class Parser:

    # check each of the connections for received RAW command data
    #   1. check web socket session interface (remote sessions)
    #   2. check web server interface
    #   3. check serial port for Microterminal
    # Parser breaks down the raw data and passes on the command, arg1, arg2, arg ... to Systemcontroller class
    #
     
    def __init__(self, command):

        self.pi = pi

	#

    def parse_command(self):
        return



if __name__ == "__main__":

    import time
#   import BME280
    import pigpio

    pi = pigpio.pi()

    if not pi.connected:
        exit(0)

#   s = BME280.sensor(pi)

    stop = time.time() + 60

    while stop > time.time():
        t, p, h = s.read_data()
        print("h={:.2f} p={:.1f} t={:.2f}".format(h, p/100.0, t))
        time.sleep(0.9)

#   s.cancel()

    pi.stop()
