#!/usr/bin/env python

import time

# Parser CLASS

class CommandParser:

    # check each of the connections for received RAW command data
    #   1. check web socket session interface (remote sessions)
    #   2. check web server interface
    #   3. check serial port for Microterminal
    # Parser breaks down the raw data and passes on the command, arg1, arg2, arg ... to SystemController class
    #
     
    def __init__(self,model_type,_SystemSettings):

        # _SystemSettings instantiated when SystemController creates DelayProcessor
        # SystemSettings contains all the configuration information of instrument and NV parameters
        self.SystemSettings = _SystemSettings

        self.PARSER_HAS_COMMAND_DATA = False
        self.PARSER_COMMAND_DATA_VALID = False
        self.PARSER_COMMAND_SOURCE = "Socket"
        self.PARSER_ARG1 = ""
        self.PARSER_ARG2 = ""
        self.PARSER_ARG3 = ""
        self.MODEL_TYPE = model_type

        self.XT100_DICTIONARY = {'CAL' : True, 'CTSTORE' : True, 'CTSTOREM' : True, 'CTSTOREM?' : True, '*CLS' : True,
                                 'DEL' : True, '*ERR?' : True, 'ERR?' : True, 'HWTRGEDGE' : True, '*IDN?' : True,
                                 'MODE' : True, 'MODE?' : True, 'NET' : True, 'NET?' : True, 'NETM?' : True,
                                 'NETSTATE?' : True, '*OPC' : True, '*OPC?' : True, 'OVER' : True, 'OVER?' : True,
                                 'OVS' : True, 'OVS?' : True, '*RST' : True, 'REM' : True, 'REM?' : True,
                                 'STEP' : True, 'STEP_INC' : True, 'STEP_DEC' : True, 'STEP?' : True, 'TERM' : True,
                                 'TERM?' : True, '*TST?' : True, 'UNITS' : True, 'UNITS?' : True }
        
        self.XT200_DICTIONARY = {'CTSTORE?' : True, 'DEL1' : True, 'DEL2' : True, 'DEL1?' : True, 'DEL2?' : True,
                                 'DEL?' : True}
                                 
        self.XR100_DICTIONARY = {'RELC' : True, 'REL' : True, 'REL?' : True, 'MEMSTORE' : True, 'MEMPTR' : True,
                                 'MEMPTR?' : True, 'MEMWRAP' : True, 'MEMWRAP?' : True, 'MEM?' : True, 'TRIGGER' : True,
                                 'TRIGGER?' : True, 'MEMPTRW' : True, 'MEMPTRW?' : True }

        if ("XT-100" in self.MODEL_TYPE):
            self.PARSER_MODEL_DICT = self.XT100_DICTIONARY
        elif ("XT-200" in self.MODEL_TYPE):
            self.PARSER_MODEL_DICT = self.XT100_DICTIONARY
            self.PARSER_MODEL_DICT.update(self.XT200_DICTIONARY)    # ADD THESE COMMANDS
        elif ("XR-100" in self.MODEL_TYPE):
            self.PARSER_MODEL_DICT = self.XR100_DICTIONARY
            self.PARSER_MODEL_DICT.update(self.XR100_DICTIONARY)    # ADD THESE COMMANDS


	# define a property 
    def set_ParserHasCommandData(self,Value):
        self.PARSER_HAS_COMMAND_DATA = Value

    def parse_command(self,RawData):
        # break down RawData into three parts:
        # Arg1, Arg2, and Arg3

        Args = RawData.split(' ')

        if (len(Args) == 0):
            print ("no arguments in raw data input")
            return False
        elif (len(Args) > 3):
            print ("too many arguments in raw data input")
            return False
        elif (len(Args) == 1):
            self.PARSER_ARG1 = str.upper(Args[0])
            self.PARSER_ARG2 = None
            self.PARSER_ARG3 = None
        elif (len(Args) == 2):
            self.PARSER_ARG1 = str.upper(Args[0])
            self.PARSER_ARG2 = str.upper(Args[1])
            self.PARSER_ARG3 = None
        elif (len(Args) == 3):
            self.PARSER_ARG1 = str.upper(Args[0])
            self.PARSER_ARG2 = str.upper(Args[1])
            self.PARSER_ARG3 = str.upper(Args[2])


        self.PARSER_HAS_COMMAND_DATA = True

        if (self.check_valid_args() == True):
            self.PARSER_COMMAND_DATA_VALID = True
        else:
            self.PARSER_COMMAND_DATA_VALID = False

        return True

    def check_valid_args(self):
        # check the model type and determine if self.PARSER_ARG1 is valid (true/false) for this model_type
        if (self.PARSER_MODEL_DICT.get(self.PARSER_ARG1) == True):
            return True
        else:
            # ADD CHECK TO SEE IF ONLY 1 ARG IS A NUMERIC ARGUMENT, IF SO, THEN SET THAT DELAY VALUE AND RETURN TRUE ELSE RETURN FALSE
            return False

    


if __name__ == "__main__":

    p = CommandParser()
    p.parse_command("del 100 ps")

    print(p.PARSER_ARG1, p.PARSER_ARG2, p.PARSER_ARG3)
