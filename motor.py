 #!/usr/bin/env python

import time


# MOTOR CLASS

# Interface

I2C=0
SPI=1

AUX_SPI=256

# Sampling

OVER_SAMPLE_1 = 1
OVER_SAMPLE_2 = 2
OVER_SAMPLE_4 = 3
OVER_SAMPLE_8 = 4
OVER_SAMPLE_16 = 5

class Motor:

    # class to handle all motor commands via com serial port link
    # BME280 Registers

    _os_ms = [0, 1, 2, 4, 8, 16]

   def __init__(self, pi, sampling=OVER_SAMPLE_1, interface=I2C,
                   bus=1, address=0x76,
                   channel=0, baud=10000000, flags=0):
      """
      Instantiate with the Pi.


      Example using I2C, bus 1, address 0x76

      s = BME280.sensor(pi)


      Example using main SPI, channel 0, baud 10Mbps

      s = BME280.sensor(pi, interface=SPI)


      Example using auxiliary SPI, channel 2, baud 50k

      s = BME280.sensor(pi, sampling=OVER_SAMPLE_4,
             interface=SPI, channel=2, flags=AUX_SPI, baud=50000)


      GPIO       pin  pin    GPIO
      3V3         1    2      5V
      2 (SDA)     3    4      5V
      3 (SCL)     5    6      0V
      4           7    8      14 (TXD)
      0V          9   10      15 (RXD)
      17 (ce1)   11   12      18 (ce0)
      27         13   14      0V
      22         15   16      23
      3V3        17   18      24
      10 (MOSI)  19   20      0V
      9 (MISO)   21   22      25
      11 (SCLK)  23   24      8 (CE0)
      0V         25   26      7 (CE1)
                 .......
      0 (ID_SD)  27   28      1 (ID_SC)
      5          29   30      0V
      6          31   32      12
      13         33   34      0V
      19 (miso)  35   36      16 (ce2)
      26         37   38      20 (mosi)
      0V         39   40      21 (sclk)
      """
      self.pi = pi

      if interface == I2C:
         self.I2C = True
      else:
         self.I2C = False

      self.sampling = sampling

      if self.I2C:
         self.h = pi.i2c_open(bus, address)
      else:
         self.h = pi.spi_open(channel, baud, flags)

      self._load_calibration()

      self.measure_delay = self._measurement_time(sampling, sampling, sampling)

      self.t_fine = 0.0

   def _measurement_time(self, os_temp, os_press, os_hum):
      ms = ( (1.25  + 2.3 * Motor._os_ms[os_temp]) +
             (0.575 + 2.3 * Motor._os_ms[os_press]) +
             (0.575 + 2.3 * Motor._os_ms[os_hum]) )
      return (ms/1000.0)

   def _u16(self, _calib, off):
      return (_calib[off] | (_calib[off+1]<<8))

   def _s16(self, _calib, off):
      v = self._u16(_calib, off)
      if v > 32767:
         v -= 65536
      return v

   def _u8(self, _calib, off):
      return _calib[off]

   def _s8(self, _calib, off):
      v = self._u8(_calib,off)
      if v > 127:
         v -= 256
      return v

   def _write_registers(self, data):
      if self.I2C:
         self.pi.i2c_write_device(self.h, data)
      else:
         for i in range(0, len(data), 2):
            data[i] &= 0x7F
         self.pi.spi_xfer(self.h, data)

   def _read_registers(self, reg, count):
      if self.I2C:
         return self.pi.i2c_read_i2c_block_data(self.h, reg, count)
      else:
         c, d = self.pi.spi_xfer(self.h, [reg|0x80] + [0]*count)
         if c > 0:
            return c-1, d[1:]
         else:
            return c, d

   def _load_calibration(self):

      c, d1 = self._read_registers(sensor._calib00, 26)

      self.T1 = self._u16(d1, sensor._T1)
      self.T2 = self._s16(d1, sensor._T2)
      self.T3 = self._s16(d1, sensor._T3)

      self.P1 = self._u16(d1, sensor._P1)
      self.P2 = self._s16(d1, sensor._P2)
      self.P3 = self._s16(d1, sensor._P3)
      self.P4 = self._s16(d1, sensor._P4)
      self.P5 = self._s16(d1, sensor._P5)
      self.P6 = self._s16(d1, sensor._P6)
      self.P7 = self._s16(d1, sensor._P7)
      self.P8 = self._s16(d1, sensor._P8)
      self.P9 = self._s16(d1, sensor._P9)

      self.H1 = self._u8(d1, sensor._H1)

      c, d2 = self._read_registers(sensor._calib26, 7)

      self.H2 = self._s16(d2, sensor._H2)

      self.H3 = self._u8(d2, sensor._H3)

      t = self._u8(d2, sensor._xE5)

      t_l = t & 15
      t_h = (t >> 4) & 15

      self.H4 = (self._u8(d2, sensor._xE4) << 4) | t_l

      if self.H4 > 2047:
         self.H4 -= 4096

      self.H5 = (self._u8(d2, sensor._xE6) << 4) | t_h

      if self.H5 > 2047:
         self.H5 -= 4096

      self.H6 = self._s8(d2, sensor._H6)

   def _read_raw_data(self):

      # Set oversampling rate and force reading.

      self._write_registers(
         [sensor._ctrl_hum, self.sampling,
          sensor._ctrl_meas, self.sampling << 5 | self.sampling << 2 | 1])

      # Measurement delay.

      time.sleep(self.measure_delay)

      # Grab reading.

      c, d = self._read_registers(sensor._rawdata, 8)

      msb = self._u8(d, sensor._t_msb)
      lsb = self._u8(d, sensor._t_lsb)
      xlsb = self._u8(d, sensor._t_xlsb)
      raw_t = ((msb << 16) | (lsb << 8) | xlsb) >> 4

      msb = self._u8(d, sensor._p_msb)
      lsb = self._u8(d, sensor._p_lsb)
      xlsb = self._u8(d, sensor._p_xlsb)
      raw_p = ((msb << 16) | (lsb << 8) | xlsb) >> 4

      msb = self._u8(d, sensor._h_msb)
      lsb = self._u8(d, sensor._h_lsb)
      raw_h = (msb << 8) | lsb

      return raw_t, raw_p, raw_h

   def read_data(self):
      """
      Returns the temperature, pressure, and humidity as a tuple.

      Each value is a float.

      The temperature is returned in degrees centigrade.  The
      pressure is returned in Pascals.  The humidity is returned
      as the relative humidity between 0 and 100%.
      """

      raw_t, raw_p, raw_h = self._read_raw_data()

      var1 = (raw_t/16384.0 - (self.T1)/1024.0) * float(self.T2)
      var2 = (((raw_t)/131072.0 - (self.T1)/8192.0) *
              ((raw_t)/131072.0 - (self.T1)/8192.0)) * (self.T3)

      self.t_fine = var1 + var2

      t = (var1 + var2) / 5120.0

      var1 = (self.t_fine/2.0) - 64000.0
      var2 = var1 * var1 * self.P6 / 32768.0
      var2 = var2 + (var1 * self.P5 * 2.0)
      var2 = (var2/4.0)+(self.P4 * 65536.0)
      var1 = ((self.P3 * var1 * var1 / 524288.0) + (self.P2 * var1)) / 524288.0
      var1 = (1.0 + var1 / 32768.0)*self.P1
      if var1 != 0.0:
         p = 1048576.0 - raw_p
         p = (p - (var2 / 4096.0)) * 6250.0 / var1
         var1 = self.P9 * p * p / 2147483648.0
         var2 = p * self.P8 / 32768.0
         p = p + (var1 + var2 + self.P7) / 16.0
      else:
         p = 0

      h = self.t_fine - 76800.0

      h = ( (raw_h - ((self.H4) * 64.0 + (self.H5) / 16384.0 * h)) *
            ((self.H2) / 65536.0 * (1.0 + (self.H6) / 67108864.0 * h *
            (1.0 + (self.H3) / 67108864.0 * h))))

      h = h * (1.0 - self.H1 * h / 524288.0)

      if h > 100.0:
         h = 100.0
      elif h < 0.0:
         h = 0.0

      return t, p, h

   def cancel(self):
      """
      Cancels the sensor and releases resources.
      """
      if self.h is not None:

         if self.I2C:
            self.pi.i2c_close(self.h)
         else:
            self.pi.spi_close(self.h)

         self.h = None

# void MOTOR_MoveLeft(void);
# void MOTOR_MoveRight(void);
# void MOTOR_SetZero(void);
# void MOTOR_SetDI(void);
# //unsigned char MOTOR_SetDelay(float _DelaySetting);
# void MOTOR_Initialize(void);
# float MOTOR_MoveToPosition(float position, unsigned int overshoot);
# short MOTOR_Calibration(void);
# unsigned char MOTOR_SetDelayDigital(long _NewDelaySettingDigital_L);
# unsigned char MOTOR_VerifyAndRoundDelay(float *del);
# void MOTOR_Command(enum MOTOR_COMMAND _COMMAND, long _ARG1, short int _Wait);
# void MOTOR_ProcessResponse(char *_MotorResponseCommandLine);
# long MOTOR_ParseResponse(char *_MotorResponseCommandLine);



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

