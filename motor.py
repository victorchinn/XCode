#!/usr/bin/env python

import time
import serial

# MOTOR CLASS
# Interface
I2C = 0
SPI = 1

AUX_SPI = 256
OVER_SAMPLE_1 = 0

# CONSTANTS DEFINED FOR MOTOR
SC_CODE_ALARM_PRESENT = 0x0200
IS_INPUT_STATUS_OPTO_BIT_ON = 0x01
DI_STOP_DISTANCE_AFTER_SENSOR = 225000
MAX_NUMBER_MOTOR_STEPS = 525000
ACK_RESPONSE = "0%\r"

MOTOR_CurrentStepPosition = 0   # THIS IS TO BE DEFINED EXTERNALLY

#defines from X_SER_HWIO.LIB

#define MOTOR_STEPS_PER_FIVE_PS 4152.50

#define SC_CODE_MOTOR_ENABLED 0x0001
#define SC_CODE_DRIVE_FAULT 0x0004
#define SC_CODE_IN_POSITION 0x0008
#define SC_CODE_ALARM_PRESENT 0x0200

#define AL_CODE_POS_LIMIT 0x0001
#define AL_CODE_CCW_LIMIT 0x0002
#define AL_CODE_CW_LIMIT 0x0004
#define AL_CODE_OVER_TEMP 0x0008
#define AL_CODE_COMM_ERROR 0x0400
#define AL_CODE_NO_MOVE 0x1000

#define DI_STOP_DISTANCE_AFTER_SENSOR 1
#define HALF_SEC 500
#define ONE_SEC 1000

#define WAIT 1
#define NOWAIT 0

#define REMOTE 1
#define LOCAL 0

class Motor:

    # class to handle all motor commands via com serial port link
    # Motor accepts commands to directly control the hybrid stepper motor
    # using the TWO CHAR commands as specified by Applied Motion
    # Motor should be called by DelayController

#    def __init__(self, pi, sampling=OVER_SAMPLE_1, interface=I2C,
#                 bus=1, address=0x76,
#                 channel=0, baud=10000000, flags=0):



    def __init__(self):

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
          
          
        #first serial port
        # GPIO14 for txc
        # GPIO15 FOR RXC
        self.com1 = serial.Serial(port = "/dev/ttyAMA0", baudrate=9600,bytesize=8, timeout=0.10, stopbits=serial.STOPBITS_ONE)
        # second serial port
        # GPIO4 TXD
        # GPIO5 RXDsc
        
        self.com2 = serial.Serial(port = "/dev/ttyAMA1", baudrate=9600,bytesize=8, timeout=0.10, stopbits=serial.STOPBITS_ONE)

        self.com1.isOpen()
        self.com2.isOpen()

        self.com1.flushInput()
        self.com1.flushOutput()

        self.com2.flushInput()
        self.com2.flushOutput()
        #
        #
        # define using the same API as in original library
        return

    def calibration(self):
        # perform a self calibration on the trombone
        return

    def move_left(self):
        return

    def move_right(self):
        return

    def set_zeroposition(self):
        return

    def set_di(self):
        return

    def set_delay(self,_DelaySetting):
        return

    # these MOTOR commands return a VALUE
    def get_motor_SC(self) -> int:
        _result = self.get_command("SC") # GET STATUS CODE
        return int(_result,base=16)  # RETURNS INT VALUE
    
    def get_motor_AL(self) -> int:
        _result = self.get_command("AL") # GET ALARM CODE
        return int(_result,base=16)  # RETURNS INT VALUE

    def get_motor_IS(self) -> int:
        _result = self.get_command("IS") # GET INPUT STATUS
        return int(_result,base=16)  # RETURNS INT VALUE

    def get_motor_IP(self) -> int:
        _result = self.get_command("IP") # GET IP
        return int(_result,base=10)  # RETURNS INT VALUE

    def get_motor_DI(self) -> int:
        _result = self.get_command("DI") # GET DI
        return int(_result,base=10)  # RETURNS INT VALUE

    # these MOTOR commands return an 0% ACKNOWLEDGEMENT

    def set_motor_AR(self) -> str:
        _response = self.set_command("AR") # SET ALARM RESET
        return _response

    def set_motor_MD(self,arg1: int) -> str:
        _response = self.set_command("DI"+str(arg1)) # SET MOTOR DISTANCE (ACTUALLY DI COMMAND)
        return _response

    def set_motor_ME(self) -> str:
        _response = self.set_command("ME") # SET MOTOR ENABLE
        return _response

    def set_motor_MO(self) -> str:
        _response = self.set_command("MO") # MOVE TO OPTO INTERRUPT
        return _response

    def set_motor_EP(self,arg1:int) -> str:
        _response = self.set_command("EP"+str(arg1)) # SET EP
        return _response

    def set_motor_SP(self,arg1:int) -> str:
        _response = self.set_command("SP"+str(arg1)) # SET SP
        return _response

    def set_motor_ML(self,arg1:int) -> str:
        _response = self.set_command("ML"+str(arg1)) # SET MOVE LEFT
        return _response

    def set_motor_MR(self,arg1:int) -> str:
        _response = self.set_command("MR"+str(arg1)) # SET MOVE RIGHT
        return _response


    # POWER ON - INITIALIZATION
    # 
    def initialize(self) -> bool:
        
        # Initialize the Motor at STARTUP
        # Returns TRUE or FALSE if initialized
        # WAIT HALF SECOND AT MOTOR STARTUP
        time.sleep(0.50)
        
        # SEND COMMAND SC TO GET INITIAL STATUS CODE
        # Establish communication and see if there is an Alarm
        # CHECK THE STATUS CODE.  IF ALARM PRESENT, RESET THE ALARM.
        _result = self.get_motor_SC()
        
        if (_result & SC_CODE_ALARM_PRESENT):
            # ALARM PRESENT ... GET THE ALARM CODE
            _result = self.get_motor_AL()
            print(f"Motor Alarm Code {hex(_result)}")
            # DO WE PRINT OR NOTIFY SOMEHOW THERE IS AN ALARM CODE IN MOTOR?

            # MOTOR_Command(AR, 0, WAIT); //waitfor(sRMRA); sRMRA = FALSE; // get ACK 0%
            # MOTOR_Command(ME, 0, WAIT); // MUST enable the motor after an alarm reset
            
            # RESET THE ALARM
            _response = self.set_motor_AR()
            if (_response != ACK_RESPONSE):
                print(f"CANNOT RESET MOTOR ALARM {_response}")
                
            # MUST ENABLE THE MOTOR AFTER AN ALARM RESET
            _response = self.set_motor_ME()
            if (_response != ACK_RESPONSE):
                print(f"CANNOT ENABLE MOTOR {_response}")
            
            # CHECK THE STATUS AFTER RESETTING THE ALARM
            _result = self.get_motor_SC()
            if (_result) & SC_CODE_ALARM_PRESENT:
                # // HALT // ??
                # // RESETTING THE ALARM DOESN'T FIX PROBLEM.  MOTOR FAIL PROBLEM.
                print(f"ALARM RESET FAIL. HALT. {_response}")
                return False
        
        # CONTINUE ... MOTOR IS INITIALIZED
        # GET ALARM CODE == LINE 537
        _result = self.get_motor_AL()       

        # ALARM STILL PRESENT?
        if (_result != 0x00):
            # MOTOR_Command(AR, 0, WAIT); // RESET IT //waitfor(sRMRA); sRMRA = FALSE; // get ACK 0%
            # MOTOR_Command(AL, 0, WAIT); // waitfor(sRMRA); sRMRA = FALSE; // get ACK 0%
            # RESET THE ALARM
            _response = self.set_motor_AR()
            if (_response != ACK_RESPONSE):
                print(f"CANNOT RESET MOTOR ALARM {_response}")

            _result = self.get_motor_AL()
            if (_result != 0):
                print(f"Motor Alarm Code {hex(_result)}")
                # IF RESETTING ALARM DOESN'T RESOLVE IT THEN HAVE A MOTOR FAIL
                # RESETTING THE ALARM DOESN'T FIX PROBLEM.  MOTOR FAIL PROBLEM.
                return False

        # NORMAL ... CONTINUE ... MOTOR HAS STARTED 
        # WE DONT KNOW THE INITIAL POSITION AT THE START
        
        # READ CURRENT INPUT STATUS OF MOTOR LINE # 558
        _result = self.get_motor_IS()
        if (_result & IS_INPUT_STATUS_OPTO_BIT_ON):
            # CURRENT LOCATION IS INSIDE THE BARRIER SINCE THE OPTO BIT IS ON

            # MOTOR_Command(FL, -100000, WAIT); # MOVE BACK 100000 STEPS
            _response = self.set_command("FL-100000")
            if (_response != ACK_RESPONSE):
                print(f"CANNOT MOVE MOTOR FL-100000.")

            time.sleep(0.50)
            
            # SEE IF THERE IS AN ALARM AFTER THIS INITIAL MOVEMENT
            # CHECK THE STATUS CODE.  IF ALARM PRESENT, RESET THE ALARM.
            _result = self.get_motor_SC()
            if (_result & SC_CODE_ALARM_PRESENT):
                _result = self.get_motor_AL()
                print(f"Motor Alarm Code {hex(_result)}")
                
                # MOTOR_Command(AR, 0, WAIT); //waitfor(sRMRA); sRMRA = FALSE; // get ACK 0%
                # MOTOR_Command(ME, 0, WAIT); // MUST enable the motor after an alarm reset
                
                # RESET THE ALARM
                _response = self.set_motor_AR() # RESET THE ALARM
                if (_response != ACK_RESPONSE):
                    print(f"CANNOT RESET MOTOR ALARM {_response}")
                    
                # MUST ENABLE THE MOTOR AFTER AN ALARM RESET
                _response = self.set_motor_ME()
                if (_response != ACK_RESPONSE):
                    print(f"CANNOT ENABLE MOTOR {_response}")

                _result = self.get_motor_AL() # GET THE ALARM CODE
                if (_result != "0x00"):
                    print(f"Motor Alarm Code {hex(_result)}")
                    
                time.sleep(0.500)
                
                # SET THE MOVE DISTANCE TO STOP FOR FS MOVEMENT
                _response = self.set_motor_MD(DI_STOP_DISTANCE_AFTER_SENSOR)
               
                _result = self.get_motor_AL() # GET THE ALARM CODE
                if (_result != 0):
                    print(f"Motor Alarm Code {hex(_result)}")
                    return False

            # LOCATION IS NOW 100000 STEPS BACK FROM OPTO LIMIT line 614

            # MOVE BACK ANOTHER 100000 STEPS
            # MOTOR_Command(FL, -100000, WAIT);
            _response = self.set_command("FL-100000")
            if (_response != ACK_RESPONSE):
                print(f"FL-10000 FAIL TO ACK. {_response}")
    
            # waitfor(DelayMs(HALF_SEC));
            time.sleep(0.50)
            
            # check MOTOR status
            # MOTOR_Command(SC, 0, WAIT); // waitfor(sRMRA); sRMRA = FALSE; // get ACK 0%
            # _StatusCode = MOTOR.RESPONSE_Value;

            _result = self.get_motor_SC() # GET STATUS CODE

            # READ CURRENT INPUT/OUTPUT STATUS OF MOTOR
            # MOTOR_Command(IS, 0, WAIT); // waitfor(sRMRA); sRMRA = FALSE; // get ACK 0%
            # _InputStatusCode = MOTOR.RESPONSE_Value;

            _result = self.get_motor_IS() # GET INPUT STATUS CODE == LINE 621
            if (_result & IS_INPUT_STATUS_OPTO_BIT_ON): 
                # WITH OPTO-BIT ON,POSITION IS INSIDE OPTO BARRIER
                # CHECK MOTOR STATUS // LINE # 632 // SHOULD NOT BE INSIDE
                # MOTOR_Command(SC, 0, WAIT); // waitfor(sRMRA); sRMRA = FALSE; // get ACK 0%
                _result = self.get_motor_SC() # GET STATUS CODE
                    
                # CANNOT POSITION MOTOR OUTSIDE OF OPTO DETECTOR
                print(f"CANNOT MOVE MOTOR OUT OF OPTO BARRIER. RETRY... SC = {hex(_result)}")

                # waitfor(DelayMs(ONE_SEC));
                time.sleep(1)

                # RESET THE MOTOR
                _response = self.set_motor_RE() # RESET MOTOR
                if (_response != ACK_RESPONSE):
                    print(f"RESET MOTOR FAIL TO ACK. {_response}")

                time.sleep(1)

                # MOTOR ENABLE AFTER A RESET
                _response = self.set_motor_ME() # MOTOR ENABLE
                if (_response != ACK_RESPONSE):
                    print(f"MOTOR ENABLE FAIL TO ACK. {_response}")

                time.sleep(1)

                # MOTOR_Command(MD, DI_STOP_DISTANCE_AFTER_SENSOR, WAIT); // SET THE MOVE DISTANCE TO STOP FOR FS MOVEMENT
                # MOTOR_Command(AL, 0, WAIT); // waitfor(sRMRA); sRMRA = FALSE; // get ACK 0%

                # SET THE MOVE DISTANCE TO STOP FOR FS MOVEMENT
                _response = self.set_motor_MD(self,DI_STOP_DISTANCE_AFTER_SENSOR)
                if (_response != ACK_RESPONSE):
                    print(f"MOTOR DISTANCE SET FAIL TO ACK. {_response}")
               
                # CHECK THE ALARM CODE
                _result = self.get_motor_AL() # GET THE ALARM CODE
                if (_result != 0):
                    print(f"Motor Alarm Code {hex(_result)}")

                # MOVE BACK 100000 STEPS
                _response = self.set_command(self,"FL-100000")
                if (_response != ACK_RESPONSE):
                    print(f"FL-10000 FAIL TO ACK. {_response}")

                time.sleep(0.50)

                _result = self.get_motor_SC() # GET STATUS CODE

                # AT LINE 624

                _result = self.get_motor_IS() # GET INPUT STATUS CODE
                if (_result & (int(IS_INPUT_STATUS_OPTO_BIT_ON))): 
                    # WITH OPTO-BIT ON,POSITION IS INSIDE OPTO BARRIER
                    # POSITION IS STILL INSIDE THE OPTO-BARRIER EVEN AFTER TRYING TO MOVE IT OUT
                    _result = self.get_motor_SC() # GET INPUT STATUS CODE
                    print(f"STATUS CODE {hex(_result)}")
                    # CANNOT POSITION MOTOR OUTSIDE OF OPTO DETECTOR
                    print(f"CANNOT MOVE MOTOR OUT OF OPTO BARRIER. RETRYING...")

                time.sleep(1)

                # RESET THE MOTOR
                _response = self.set_motor_RE() # RESET MOTOR
                if (_response != ACK_RESPONSE):
                    print(f"RESET MOTOR FAIL TO ACK. {_response}")

                time.sleep(1)

                # MOTOR ENABLE AFTER A RESET
                _response = self.set_motor_ME() # MOTOR ENABLE
                if (_response != ACK_RESPONSE):
                    print(f"MOTOR ENABLE FAIL TO ACK. {_response}")

                time.sleep(1)

                # SET THE MOVE DISTANCE TO STOP FOR FS MOVEMENT
                _response = self.set_motor_MD(DI_STOP_DISTANCE_AFTER_SENSOR)
                if (_response != ACK_RESPONSE):
                    print(f"MOTOR DISTANCE SET FAIL TO ACK. {_response}")
               
                # CHECK THE ALARM CODE
                _result = self.get_motor_AL() # GET THE ALARM CODE
                if (_result != 0):
                    print(f"Motor Alarm Code {hex(_result)}")
                    return False

                # MOVE BACK 100000 STEPS
                _response = self.set_command(self,"FL-100000")
                if (_response != ACK_RESPONSE):
                    print(f"FL-10000 FAIL TO ACK. {_response}")

                time.sleep(0.50)

        # MOTOR POSITION IS NOT IN BARRIER BUT OTHERWISE UNKNOWN.
        # LINE 662

        # GET IP POSITION
        _result = self.get_motor_IP() # GET IP POSITION

        # SET THE MOVE DISTANCE TO STOP FOR FS MOVEMENT
        _response = self.set_motor_MD(DI_STOP_DISTANCE_AFTER_SENSOR)
        if (_response != ACK_RESPONSE):
            print(f"MOTOR DISTANCE SET FAIL TO ACK. {_response}")

        # GET DI VALUE
        _result = self.get_motor_DI() # GET DI # SHOULD BE 225000

        # GET STATUS CODE
        _result = self.get_motor_SC() # GET STATUS CODE SHOULD BE 0SC=0009

        # GET CURRENT POSITION AND RECORD IT
        # GET IP POSITION
        _result = self.get_motor_IP() # GET IP POSITION
        _StartupMotorPosition = _result    

        # MOVE TO OPTO LIMIT
        # LINE 690

        # MOVE TO OPTO LIMIT
        _response = self.set_motor_MO() # MOVE TO OPTO LIMIT
        if (_response != ACK_RESPONSE):
            print(f"GET STATUS CODE FAIL TO ACK. CANNOT MOVE TO OPTO LIMIT {_response}")

        time.sleep(1.5)

        # GET STATUS CODE
        _result = self.get_motor_SC()      # == LINE 701
        if (_result & SC_CODE_ALARM_PRESENT):
            _result = self.get_motor_AL()
            print(f"Motor Alarm Code {hex(_result)}")
            
            # RESET THE ALARM
            _response = self.set_motor_AR() # RESET THE ALARM
            if (_response != ACK_RESPONSE):
                print(f"CANNOT RESET MOTOR ALARM {_response}")
                
            # MUST ENABLE THE MOTOR AFTER AN ALARM RESET
            _response = self.set_motor_ME()
            if (_response != ACK_RESPONSE):
                print(f"CANNOT ENABLE MOTOR {_response}")

            # GET STATUS CODE
            _result = self.get_motor_SC()
            if (_result & SC_CODE_ALARM_PRESENT):
                print(f"MOTOR ALARM RESET FAIL CODE {hex(_result)}")
                return False

        # NO ALARM CONTINUE

        # GET IP POSITION == LINE 727
        _result = self.get_motor_IP() # GET IP POSITION
        _MotorPosition = _result 
        if (_result == _StartupMotorPosition):
        # IF THE MOTOR POSITION IS THE SAME THEN THERE WAS A PROBLEM WITH OPTODETECT MOVE

            # GET STATUS CODE
            _result = self.get_motor_SC()
            if (_result & SC_CODE_ALARM_PRESENT):
                print(f"NO MOVE ERROR. SC = {hex(_result)}")
                return False
        
        # MOTOR OPTO HAS PASSED

        # IF THE STARTING MOTOR POSITION IS ABOVE 525000, THEN MR 100000
        # ELSE MR FOR THE ENTIRE AMOUNT OF THE INITIAL POSITION

        # LINE 735
        if (_MotorPosition > MAX_NUMBER_MOTOR_STEPS):
            #
            # MOVE BACK 100000 STEPS
            _response = self.set_command(self,"FL-100000")
            if (_response != ACK_RESPONSE):
                print(f"FL-10000 FAIL TO ACK. {_response}")

            time.sleep(0.50)

            # MOVE TO OPTO LIMIT
            _response = self.set_motor_MO() # MOVE TO OPTO LIMIT
            if (_response != ACK_RESPONSE):
                print(f"GET STATUS CODE FAIL TO ACK. {_response}")

            time.sleep(0.5)

            # GET IP POSITION
            _result = self.get_motor_IP() # GET IP POSITION
            _MotorPosition = _result

        # CURRENT MOTOR POSITION IS INSIDE THE OPTO
        # BACK OFF A FIXED NUMBER OF STEPS (MAX FOR INSTRUMENT) AND THEN SET AS ZERO POSITION
        # FL COMMANDS MOVES RELATIVE NUMVER OF STEPS FROM CURRENT POSITION
        
        _response = self.set_command("FL-"+ str(MAX_NUMBER_MOTOR_STEPS))
        if (_response != ACK_RESPONSE):
            print(f"FL-10000 FAIL TO ACK. {_response}")

        time.sleep(1.5) # IS THIS ENOUGH TIME TO MOVE FULL RANGE END TO END ??

        # GET IP POSITION
        _result = self.get_motor_IP() # GET IP POSITION
        _MotorPosition = _result   
        
        # SHOULD NOW BE AT THE ZERO POSITION
        # SET THE ZERO POSITION HERE

        # EP ENCODER POSITION COMMAND // EP0 TO RESET INTERNAL POSITION COUNTER TO 0
        _response = self.set_motor_EP(0)
        if (_response != ACK_RESPONSE):
            print(f"EP0 FAIL TO ACK. {_response}")

        # SP SET POSITION // SP0 TO RESET INTERNAL POSITION COUNTER TO 0 == ZERO POINT
        _response = self.set_motor_SP(0)
        if (_response != ACK_RESPONSE):
            print(f"SP0 FAIL TO ACK. {_response}")

        # GET IP POSITION
        _result = self.get_motor_IP() # GET IP POSITION
        _MotorPosition = _result

        time.sleep(0.50)
        
        return True

    def move_to(self, position, overshoot):
        return

    def calibration(self):
        
        return

    def set_DelayDigital(self,_NewDelaySettingDigital_L):
        # SET THE NEW DIGITAL DELAY POSITION

        # NOTE: MOTOR IS POSITIONED ON THE LEFT HAND SIDE.  TROMBONE MOVES FROM LEFT TO RIGHT.
        # FAR LEFT IS LEAST DELAY AND FAR RIGHT IS MOST DELAY.
        # if result is POSITIVE(+) then need to move the MOTOR to the LEFT (MORE DELAY TO LESS DELAY)
        # if result is NEGATIVE(-) then need to move the MOTOR to the RIGHT(LESS DELAY TO MORE DELAY)
        # ZERO POSITION IS AT THE LIGHT BARRIER

        # MOVE TO THE NEW DIGITAL STEP POSITION
        if (_NewDelaySettingDigital_L >= 0):
            _DeltaSteps = MOTOR_CurrentStepPosition - (_NewDelaySettingDigital_L)
            MOTOR_CurrentStepPosition = _NewDelaySettingDigital_L
        else:
            # NEW DELAY SETTING IS NEGATIVE ... NOT POSSIBLE
            return False

        if (_DeltaSteps > 0):
            # going from higher step number (MORE Delay) to lower step number (LESS Delay)
            # after sending command, WAIT for the acknowledgement before returning
            # MOTOR_Command(MR, _DeltaSteps, WAIT); // MR = move right with MOTOR ON RIGHT SIDE
            _response = self.motor_MR(self,_DeltaSteps)
            if (_response != ACK_RESPONSE):
                print(f"MR FAIL TO ACK. {_response}")
        else:
            _DeltaSteps = _DeltaSteps * -1;
            # going from lower step number (LESS delay) to higher step number (MORE delay)
            # after sending command, WAIT for the acknowledgement before returning
            # MOTOR_Command(ML, _DeltaSteps, WAIT); // ML = move left with MOTOR ON RIGHT SIDE
            _response = self.motor_ML(self,_DeltaSteps)
            if (_response != ACK_RESPONSE):
                print(f"ML FAIL TO ACK. {_response}")

        # NOTE: when sending a COMMAND to move the motor, the motor replies with 0% acknowledgement
        # 
        # if (_CheckPosition == FALSE) { return TRUE; } ;   // no wait to check position...just return
        # return TRUE here if dont want to wait
        # 
        # wait to let MOTOR MOVE for NEW MOTOR
        # this is a costatement way to wait 500 ms
        # TBD should try using HWIO_msDelay(x) where x is a variable amount depending
        # on the distance that needs to be moved

        return True

    def verify_and_round(self,delay):
        return
    
    def set_command(self,motor_command) -> str:
        # Send motor_command to the motor
        # Get the response from the motor 
        # could be 0% or XX=VALUE
        self.send_cmd(self.com1,motor_command,0.100)
        response = self.read_response(self.com1)
        print (f"Sent: {motor_command} Response: {response}")
        return response # return a str should be ACK_RESPONSE "0%\r"

    def get_command(self,motor_command) -> str:
        # Send motor_command to the motor
        # Get the response from the motor 
        # could be 0% or XX=VALUE
        self.send_cmd(self.com1,motor_command,0.100)
        response = self.read_response(self.com1)
        print (f"Sent: {motor_command} Response: {response}")
        # process the response and return just the digits in the response
        digits = self._process_response(response)
        return digits 


    def _process_response(self,_MotorResponseCommandLine:str) -> str:
        # RESPONSE FROM MOTOR IS XX=VALUE
        # PARSE THE TWO LETTER COMMAND AND THE INTEGER VALUE
        # NEED TO PARSE THIS RESPONSE
        string_response = _MotorResponseCommandLine.replace("\r","")
        digits_only = string_response.split("=") 
        digits = digits_only[1]
        return digits   # returns a string of chars

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
    
    def send_cmd(self,serialport,motorcommand,waittime):
        command = "0" + motorcommand + '\r'
        serialport.write(command.encode())    # encode into bytes
        time.sleep(waittime) # send to motor and wait 100 ms to read response

    def read_response(self,serialport):
        if (serialport.in_waiting > 0):
            number_bytes = serialport.in_waiting
            from_motor = serialport.read(number_bytes)
            if from_motor == None:
                return None
            else:
                return from_motor.decode()
            
    def test_input_command(self):
        getinput = input()
        motorcommand = getinput
        m.send_cmd(m.com1,motorcommand,0.100)
        result = m.read_response(m.com1)
        print (motorcommand, result)


        

if __name__ == "__main__":

    import time
    print ("Main program ")
    m = Motor()
#    m.initialize()

    while True:
        m.test_input_command()

        m.initialize()
    
    




