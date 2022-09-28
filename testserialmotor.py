import serial
import time


def sendcmdtomotor(serialport,motorcommand,waittime):
    command = "0" + motorcommand + '\r'
    serialport.write(command.encode())    # encode into bytes
    time.sleep(waittime) # send to motor and wait 100 ms to read response

def readresponsemotor(serialport):
    if (serialport.in_waiting > 0):
        number_bytes = serialport.in_waiting
        from_motor = serialport.read(number_bytes)
        if from_motor == None:
            return None
        else:
            return from_motor.decode()

if __name__ == "__main__":

    #first serial port
    # GPIO14 for txc
    # GPIO15 FOR RXC
    com1 = serial.Serial(port = "/dev/ttyAMA0", baudrate=9600,bytesize=8, timeout=0.10, stopbits=serial.STOPBITS_ONE)
    # second serial port
    # GPIO4 TXD
    # GPIO5 RXD
    com2 = serial.Serial(port = "/dev/ttyAMA1", baudrate=9600,bytesize=8, timeout=0.10, stopbits=serial.STOPBITS_ONE)

    com1.isOpen()
    com2.isOpen()

    com1.flushInput()
    com1.flushOutput()

    com2.flushInput()
    com2.flushOutput()

    while True:


        getinput = input()
        motorcommand = getinput
        sendcmdtomotor(com1,motorcommand,0.100)
        result = readresponsemotor(com1)
        print (motorcommand, result)


