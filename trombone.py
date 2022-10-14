
import enum
from motor import *
from dataclasses import dataclass

# SystemController CLASS
ERR_NO_ERROR = -1
ERR_INVALID_ARG = 1
ERR_NO_CALIBRATION = 2
ERR_DELAY_NOT_SET = 3
ERR_DELAY_OUT_OF_RANGE = 4

@dataclass
class Trombone:

    def __init__(self, model_type, _SystemSettings):
        # first arg = model type

        self.MODEL_TYPE = model_type

        # _SystemSettings instantiated when SystemController creates DelayProcessor
        # SystemSettings contains all the configuration information of instrument and NV parameters
        self.SystemSettings = _SystemSettings

        self.Motor = Motor()
        if (self.Motor.initialize() == False):
            pass
            # WHAT TO DO IF THERE IS A MOTOR INITIALIZATION PROBLEM HERE?
        else:
            pass

        self.CalibrationTable = [0,0]
     
    def initialize(self):
        # Initialize the Trombone ...
        # Read the calibration table into memory

        return 


    def set_CalibrationTable(self,Index,Value):
        self.CalibrationTable[Index] = Value

    def get_CalibrationTable(self,Index):
        return self.CalibrationTable[Index]

    def read_CalibrationTable_from_file(self):
        # fill the CalibrationTable with values from stored file or from NV_ file ? 
        pass

    def set_Delay(self,Value):
        # determine if ser or parallel mode
        # set the delay in the trombone only portion
        print (f"Set delay Trombone XT-100 {Value}")
        return ERR_NO_ERROR

    def set_delay(self, pri_sec:enum, value : int, overshoot: bool, caltable: bool, callback: object  ) -> None:
        if (pri_sec == 'PRI'):
            # determine which COM port to use whether XT-100 or XT-200 PRIMARY
            pass
        else:
            # use the com port for secondary trombone XT-200 SECONDARY
            pass

                    
    
    def set_Delay_Primary(self,Value):
        print (f"Set delay CH1 XT-200 {Value}")
        return ERR_NO_ERROR

    def set_Delay_Secondary(self,Value):
        print (f"Set delay CH2 XT-200 {Value}")
        return ERR_NO_ERROR

