#!/usr/bin/env python

import time

# Delayprocessor CLASS


class Delayprocessor:

    # class to handle control and commands FROM SystemController 
    # sets the delay according to the correct model configuration and type
    # uses and commands Trombone object and Relays object

    def __init__(self, command):

        self.pi = pi

	#

    def set_delay(self):
        return

    def set_delay_ch1(self):
        return

    def set_delay_ch2(self, _DelaySetting):
        return

    def initialize(self):
        return

    def calibration(self):
        return
    
    def set_calibration_table(self): # set the entries for the Trombone Calibration Table
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
