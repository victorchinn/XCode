class Settings(object):
    
##
##    g_NVParameters.nv_ip_addr = aton("192.168.100.8");
##    g_NVParameters.nv_ip_addr = aton("192.168.100.8");
##    g_NVParameters.nv_netmask = aton("255.255.0.0");
##    g_NVParameters.nv_gateway = aton("192.168.100.1");
##    g_NVParameters.nv_port = 5025; // default port address for industry standard SCPI  //
##    g_NVParameters.nv_useDHCP = TRUE;               // DHCP DEFAULT SHOULD BE ON 08.02.21
##    g_NVParameters.nv_overshoot = TRUE;             // added 04.18.07
##    g_NVParameters.nv_autodrop = TRUE;              // added 03.16.15
##    g_NVParameters.nv_terminal_mode = FALSE;        // added 05.24.05
##    g_NVParameters.nv_nsps_cycle_mode = CYCLE_UNIT; // added 07.02.08 // 04.10.18
##    g_NVParameters.nv_overshoot_PS = 5; 			// added 06.06.22 SET DEFAULT OVERSHOOT VALUE TO 5 PS
##    strcpy(g_NVParameters.nv_description, "XS-100 Programmable Delay Line Instrument");
##    strcpy(g_NVParameters.nv_password, "password");
##    //	int   nv_cal_table[SIZE_CAL_TABLE];     // float for # of PS with 3 decimal pt precision adjustment
##    //	char  nv_cal_info[SIZE_CAL_INFO_FIELD]; // calibration table information max of 128 characters
##
##    strcpy(g_NVParameters.nv_cal_info, "NO CALIBRATION");
##    strcpy(g_NVParameters.nv_hostname, "COLBY_XXXXXXXX"); // 01.24.21
##    g_NVParameters.nv_useCTSTORE = FALSE;
##
##
##    SYSTEM_SaveNVParametersXT(); // 02.02.22 PRESERVE SERIAL PORT B
#

    def set_MODEL_TYPE(self, Arg1):
        self.MODEL_TYPE = Arg1
    def get_MODEL_TYPE(self):
        return self.MODEL_TYPE

    def set_NV_IP_ADDR(self, Arg1):
        self.NV_IP_ADDR = Arg1
    def get_NV_IP_ADDR(self):
        return self.NV_IP_ADDR

    def set_NV_NETMASK(self, Arg1):
        self.NV_NETMASK = Arg1
    def get_NV_NETMASK(self):
        return self.NV_NETMASK

    def set_NV_GATEWAY(self, Arg1):
        self.NV_GATEWAY = Arg1
    def get_NV_GATEWAY(self):
        return self.NV_GATEWAY

    def set_NV_PORT(self, Arg1):
        self.NV_PORT = Arg1
    def get_NV_PORT(self):
        return self.NV_PORT

    def set_NV_USE_DHCP(self, Arg1):
        self.NV_USE_DHCP = Arg1
    def get_NV_USE_DHCP(self):
        return self.NV_USE_DHCP

    def set_NV_OVERSHOOT(self, Arg1):
        self.NV_OVERSHOOT = Arg1
    def get_NV_OVERSHOOT(self):
        return self.NV_OVERSHOOT

    def set_NV_AUTODROP(self, Arg1):
        self.NV_AUTODROP = Arg1
    def get_NV_AUTODROP(self):
        return self.NV_AUTODROP

    def set_NV_TERMINAL_MODE(self, Arg1):
        self.NV_TERMINAL_MODE = Arg1
    def get_NV_TERMINAL_MODE(self):
        return self.NV_TERMINAL_MODE

    def set_NV_NSPS_CYCLE_MODE(self, Arg1):
        self.NV_NSPS_CYCLE_MODE = Arg1
    def get_NV_NSPS_CYCLE_MODE(self):
        return self.NV_NSPS_CYCLE_MODE

    def set_NV_OVERSHOOT_PS(self, Arg1):
        self.NV_OVERSHOOT_PS = Arg1
    def get_NV_OVERSHOOT_PS(self):
        return self.NV_OVERSHOOT_PS

    def set_NV_DESCRIPTION(self, Arg1):
        self.NV_DESCRIPTION = Arg1
    def get_NV_DESCRIPTION(self):
        return self.NV_DESCRIPTION

    def set_NV_PASSWORD(self, Arg1):
        self.NV_PASSWORD = Arg1
    def get_NV_PASSWORD(self):
        return self.NV_PASSWORD

    def set_NV_CAL_INFO(self, Arg1):
        self.NV_CAL_INFO = Arg1
    def get_NV_CAL_INFO(self):
        return self.NV_CAL_INFO

    def set_NV_HOSTNAME(self, Arg1):
        self.NV_HOSTNAME = Arg1
    def get_NV_HOSTNAME(self):
        return self.NV_HOSTNAME

    def set_NV_USE_CTSTORE(self, Arg1):
        self.NV_USE_CTSTORE = Arg1
    def get_NV_USE_CTSTORE(self):
        return self.NV_USE_CTSTORE

    def read_NV_file(self):
        # read the NV_Parameters File for NV_ settings values
        pass
    def write_NV_file(self):
        pass

    def get_INST_IDN_INFO(self):
        return self.INST_IDN_INFO


    def __init__(self,model_type):

        self.MODEL_TYPE = model_type
        # NON-VOLATILE STORED VALUES
        self.NV_MODEL_TYPE = model_type
        self.NV_IP_ADDR = "192.168.100.8"
        self.NV_NETMASK = "255.255.0.0"
        self.NV_GATEWAY = "255.255.0.0"
        self.NV_PORT = 5025
        self.NV_USE_DHCP = True
        self.NV_OVERSHOOT = True
        self.NV_AUTODROP = True
        self.NV_TERMINAL_MODE = False
        self.NV_NSPS_CYCLE_MODE = "CYCLE_UNIT"
        self.NV_OVERSHOOT_PS = 5
        self.NV_DESCRIPTION = "XT-100 Programmable Delay Line Instrument"
        self.NV_PASSWORD = "password"
        self.NV_CAL_INFO = "NO CALIBRATION"
        self.NV_HOSTNAME = "COLBY_2206YYYY"
        self.NV_USE_CTSTORE = False
        self.NV_CAL_TABLE = [0,0,0,0,0]     # LIST OF 1251 ENTRIES FROM 0 TO 1250 INDEX]

        # INSTRUMENT INFO

        if (model_type == "XT-100-625P"):
            self.MODEL_RANGE = 625.0
            self.MODEL_STEP = 0.50
            self.MODEL_NUM_RELAYS = 0
            self.MODEL_RELAY_VALUES = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XT-100-001N"):
            self.MODEL_RANGE = 1250.0
            self.MODEL_STEP = 0.50
            self.MODEL_NUM_RELAYS = 1
            self.MODEL_RELAY_VALUES = [625.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XT-100-002N"):
            self.MODEL_RANGE = 2500.0
            self.MODEL_STEP = 0.50
            self.MODEL_NUM_RELAYS = 2
            self.MODEL_RELAY_VALUES = [625.0,1250.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XT-100-005N"):
            self.MODEL_RANGE = 5000.0
            self.MODEL_STEP = 0.50
            self.MODEL_NUM_RELAYS = 3
            self.MODEL_RELAY_VALUES = [625.0,1250.0,2500.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XT-100-010N"):
            self.MODEL_RANGE = 10000.0
            self.MODEL_STEP = 0.50
            self.MODEL_NUM_RELAYS = 4
            self.MODEL_RELAY_VALUES = [625.0,1250.0,2500.0,5000.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XT-100-020N"):
            self.MODEL_RANGE = 20000.0
            self.MODEL_STEP = 0.50
            self.MODEL_NUM_RELAYS = 5
            self.MODEL_RELAY_VALUES = [625.0,1250.0,2500.0,5000.0,10000.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XT-100-040N"):
            self.MODEL_RANGE = 40000.0
            self.MODEL_STEP = 0.50
            self.MODEL_NUM_RELAYS = 6
            self.MODEL_RELAY_VALUES = [625.0,1250.0,2500.0,5000.0,10000.0,20000.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XT-100-050N"):
            self.MODEL_RANGE = 50000.0
            self.MODEL_STEP = 0.50
            self.MODEL_NUM_RELAYS = 7
            self.MODEL_RELAY_VALUES = [625,1250.0,2500.0,5000.0,10000.0,20000.0,10000.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XT-100-080N"):
            self.MODEL_RANGE = 80000.0
            self.MODEL_STEP = 0.50
            self.MODEL_NUM_RELAYS = 7
            self.MODEL_RELAY_VALUES = [625,1250.0,2500.0,5000.0,10000.0,20000.0,40000.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XT-100-100N"):
            self.MODEL_RANGE = 100000.0
            self.MODEL_STEP = 0.50
            self.MODEL_NUM_RELAYS = 0
            self.MODEL_RELAY_VALUES = [625,1250.0,2500.0,5000.0,10000.0,20000.0,40000.0,20000.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XR-100-010N-010P-10"):
            self.MODEL_RANGE = 10230.0
            self.MODEL_STEP = 10.0
            self.MODEL_NUM_RELAYS = 10
            self.MODEL_RELAY_VALUES = [10.0,20.0,40.0,80.0,160.0,320.0,640.0,1280.0,2560.0,5120.0,0.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XR-100-010N-005P-11"):
            self.MODEL_RANGE = 10230.0
            self.MODEL_STEP = 10.0
            self.MODEL_NUM_RELAYS = 11
            self.MODEL_RELAY_VALUES = [5.0,10.0,20.0,40.0,80.0,160.0,320.0,640.0,1280.0,2560.0,5120.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XR-100-050N-010P-13"):
            self.MODEL_RANGE = 50950.0
            self.MODEL_STEP = 10.0
            self.MODEL_NUM_RELAYS = 13
            self.MODEL_RELAY_VALUES = [10.0,20.0,40.0,80.0,160.0,320.0,640.0,1280.0,2560.0,5120.0,0.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XR-100-080N-020P-12"):
            self.MODEL_RANGE = 81900.0
            self.MODEL_STEP = 20.0
            self.MODEL_NUM_RELAYS = 13
            self.MODEL_RELAY_VALUES = [10.0,20.0,40.0,80.0,160.0,320.0,640.0,1280.0,2560.0,5120.0,10240.0,20480.0,40960.0,0.0,0.0,0.0]
        elif (model_type == "XR-100-100N-010P-14"):
            self.MODEL_RANGE = 101910.0
            self.MODEL_STEP = 10
            self.MODEL_NUM_RELAYS = 14
            self.MODEL_RELAY_VALUES = [10.0,20.0,40.0,80.0,160.0,320.0,640.0,1280.0,2560.0,5120.0,10240.0,20480.0,40960.0,20000.0,0.0,0.0]
        elif (model_type == "XR-100-200N-001N-8"):
            self.MODEL_RANGE = 200000.0
            self.MODEL_STEP = 10
            self.MODEL_NUM_RELAYS = 8
            self.MODEL_RELAY_VALUES = [1000.0,2000.0,4000.0,8000.0,16000.0,32000.0,64000.0,73000.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XT-200-312P"):
            self.MODEL_RANGE = 312.50
            self.MODEL_STEP = 0.25
            self.MODEL_NUM_RELAYS = 0
            self.MODEL_RELAY_VALUES = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XT-200-625P"):
            self.MODEL_RANGE = 625.0
            self.MODEL_STEP = 0.50
            self.MODEL_NUM_RELAYS = 0
            self.MODEL_RELAY_VALUES = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        elif (model_type == "XS-100-005N-001P-14"):
            self.MODEL_RANGE = 10230.0
            self.MODEL_STEP = 1.0
            self.MODEL_NUM_RELAYS = 14
            self.MODEL_RELAY_VALUES = [1,2,4,8,5,10.0,20.0,40.0,80.0,160.0,320.0,640.0,1280.0,2560.0,0.0,0.0]

        self.INST_SERIAL_NUMBER = "2212YYYY"
        self.INST_VER_INFO = "V2.00"
        self.INST_IDN_INFO = (f"Colby Instruments,{self.MODEL_TYPE},{self.INST_VER_INFO},{self.INST_SERIAL_NUMBER}")
        self.INST_MAC_ID = "xx:xx:xx:xx"
        self.INST_OPERATION_COMPLETE = False
        self.INST_REMOTE_MODE = True
        self.INST_CYCLE_MODE = "CYCLE_CHANNEL" # CYCLE_SEQ | CYCLE_UNIT | CYCLE_CHANNEL 
        self.INST_SERIAL_MODE = True
        self.INST_STEP_SIZE = 5     # INC/DEC STEP IN NUMBER OF PICOSECONDS
        if ("XT-200" in self.MODEL_TYPE):
            self.INST_PRIMARY_TROMBONE = True   # SET TO TRUE FOR PRIMARY TROMBONE, AND FALSE FOR SECONDARY TRONBONE
        else:
            self.INST_PRIMARY_TROMBONE = False  # SET TO TRUE FOR SECONDARY TROMBONE, AND FALSE FOR PRIMARY TROMBONE



        





