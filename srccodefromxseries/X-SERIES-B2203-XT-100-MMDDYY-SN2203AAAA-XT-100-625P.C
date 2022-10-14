/* DESCRIPTION ***************************************************************
 *   File:    	: XT-SYSTEM-B2112-XT-100-625P
 *	Description	: XT-100 Instrument System Application
 *	Project		: Colby Instruments Programmable Delay Line X SERIES
 *	Date		: MAY 17, 2021
 *				: Copyright(c) 2021 Colby Instruments, Bellevue, WA
 *	NOTES:		:
 *END DESCRIPTION ***************************************************************/
//
// RD012821
// 01.28.21	using RD012821 VERSIONS OF LIB: METHODS, COMMANDS, AND REFACTOR
// 01.28.21 RD01 WEB_SERVER IS NOW ENABLED BY SPECIFYING #define ENABLE_WEB_SERVER
// 02.07.21	use #define WEB_SERVER when adding code to support the enabled web server
// 02.07.21 RD02 removed motor movement wait in COMMANDS.LIB with #define NOMOTORWAIT
// 02.07.21 RD02 changes were all in COMMANDS.LIB and not required in MAIN code
// 02.07.21 RD02 added #define NET_STATUS into ENET LIB to use for network status LED
// 02.07.21 RD03 added INSTRUMENT_SETTINGS.CURRENT BAR GRAPH AND CURRENT LED STATUS - global variables
// 02.07.21 RD03 added
// 02.07.21 RD03 added #define TOP_TO_BOTTOM_NEW_LED for SYSTEM_OutputPrompt in REFACTOR_HW1.LIB to FLIP BYTES TOP TO BOTTOM FOR LEDS
//
// 02.15.21 START WITH XT-100-BASE-CODE-FOR-HW1VER2
// 02.28.21	DEFINE MIN_WEB FOR JUST THE BASIC WEB CODE FOR DEBUGGING W/O HW3 HARDWARE DEPENCIES (WORK WITH DEV BOARD)
// 04.15.21	if #DEFINE MIN_WEB, THEN ONLY GET MIN WEB HTTP AND ETHERNET PROCESS CODE AS NORMAL
// 04.30.21	NOTE: serial port b gets reset/becomes unusable after doing a userblockread (LOAD NV PARAMETERS)
// 04.30.21 NOTE: after using a loadnvparameters, open the serial port B when talking to the secondary trombone
// 04.30.21 NOTE: when running as secondary, no need to do a loadnvparameters (just use the already loaded nvparameters on the initial read)
// 04.30.21 XT-100 hardware working ... last item to test integrate is the external interrupt
// 05.18.21 REMOVE GPIB CODE AND VARIABLES
// 05.19.21	REMOVE CONFIG.LIB, COMBINE SYS_COMMANDS.LIB AND REFACTOR_BASE.LIB TO FORM SYSTEM.LIB, REMOVE NON-SEQ_RELAY.LIB
// 05.27.21 REMOVE HW_RELAYS.SWITCH_SETTINGS AND REPLACED WITH INSTRUMENT.stateFACTORY_DEFAULT_PRESSED
// 05.27.21 REMOVE #ifdef NVSTORAGE, NVSTORAGE is always available so make it default
// 05.28.21 MOVED VIRTUAL ZERO BACK TO 630 PS (WAS 625PS) // WAS #define MAX_NUMBER_MOTOR_STEPS 520312 TO 524475
// 05.28.21 HANDLE OVERSHOOT WHEN IN RANGE OF 625-630 PS.  OVERSHOOT ENABLED FOR 620 TO 625 PS SETTINGS.
// 05.28.21 *OPC? returns 1 AFTER MOTOR MOVEMENT is completed.
// 06.07.21 WORKING WITH XT SYSTEM BOARD REV 2:
// 06.07.21 BARGRAPH, SECONDARY TROMBONE WORKING - PRIMARY_TROMBONE AND SECONDARY_TROMBONE
// 06.07.21 FACTORY DEFAULT SWITCH WORKING, I2C WORKING BUT WITH OLD REV RELAY BOARD
// 06.07.21 NEED TO TEST INTERRUPT HW
// 06.16.21 REMOVE #define DEVICE_XT100_XR100 and #ifdef DEVICE_XT100_XR100 all CODE
// 06.17.21 PORT 5025 DEFAULT INSTEAD OF 1234 FOR INDUSTRY STANDARD SCPI
// 06.23.21 added INSTRUMENT.statePENDING_OPC_QUERY_CH2 and 3
// 06.23.21 added stateOPC_CHAR_RECEIVED
// 06.24.21 added INSTRUMENT.stateLAST_OPERATION_CHANNEL = 1, 2, or 3 to specify channel setting of last operation
// 06.25.21 USE XT-100 AND DEFINE SECONDARY TROMBONE FOR SECOND TROMBONE IN XT-200

// 07.19.21	X SERIES FINAL PRODUCTION CODE VERSION 1.00 BUILD 2109 --------------------------------------------------
// 07.19.21 RD073021 BUILD
// 07.19.21 ADD FIRMWARE UPLOAD IN WEB SERVER
// 08.04.21	X SERIES FINAL PRODUCTION CODE VERSION 1.00 BUILD 2109 --------------------------------------------------
// 08.17.21 UPDATES FOR HWIO_REL APIS

// 08.17.21 X SERIES FINAL PRODUCTION CODE VERSION 1.01 BUILD 2109_RD080621 -----------------------------------------
// 08.17.21 X SERIES FINAL PRODUCTION CODE VERSION 1.01 BUILD 2109_RD080621 -----------------------------------------
// 08.17.21 X SERIES FINAL PRODUCTION CODE VERSION 1.01 BUILD 2109_RD080621 -----------------------------------------

// 10.05.21 added handle #ifdef DEVICE_XT100_312P
// 10.06.21 MUST USE use LIB BUILD BUILD2109_RD080621_RD081621

// 10.18.21 X SERIES FINAL PRODUCTION CODE VERSION 1.10 BUILD 2112 -----------------------------------------
// 10.18.21 X SERIES FINAL PRODUCTION CODE VERSION 1.10 BUILD 2112 -----------------------------------------
// 10.18.21 X SERIES FINAL PRODUCTION CODE VERSION 1.10 BUILD 2112 -----------------------------------------

// 10.21.21 FOR BUILD2112_RD102121  // 11.07.21 USE XT-LIB_B2112_RD102121.DIR TO BUILD
// 10.21.21 FOR BUILD2112_RD102121  // 11.07.21 USE XT-LIB_B2112_RD102121.DIR TO BUILD
// 10.21.21 FOR BUILD2112_RD102121  // 11.07.21 USE XT-LIB_B2112_RD102121.DIR TO BUILD

// 10.22.21 ADD DEVICE_XT100_200N
// 10.27.21 ADD unsigned long CurrentDelaySetting_UL;  IN MOTOR

// 11.07.21 RENAME #define DEVICE_XT100_200N to #define USE_DELAY_UL_TABLE
// 11.07.21 BUILD TARGET: XT-100-625P

// 11.11.21 DETECT THE EDGE CASE WHERE THE REMAINDER IS 625 AND THE POSITION MODULO IS ZERO
// 11.11.21 cmdSET_DELAY: if (_DelayRemainder_PS == 625) {_DesiredMotorPos_MOD_F = 625;}

// 11.11.21 X SERIES FINAL PRODUCTION CODE VERSION 1.11 BUILD 2112_RD102121 --------------------------------
// 11.11.21 X SERIES FINAL PRODUCTION CODE VERSION 1.11 BUILD 2112_RD102121 --------------------------------
// 11.11.21 X SERIES FINAL PRODUCTION CODE VERSION 1.11 BUILD 2112_RD102121 --------------------------------

// 11.11.21 BUILD2112_RD102121_RD111121
// 11.11.21	ADD #DEFINE NEW DEVICE DEVICE_XT200_312P AS PARALLEL EQUIVALENT TO XT200
// 11.13.21	FOR DEVICE_XT200-312P, ALSO MUST DEFINE #DEVICE_XT200 AND TREAT LIKE 625P MODEL IN PARALLEL MODE
// 11.13.21 MAIN_Initialize_RelaySettings: INSTRUMENT.stateDEVICE_DISPLAY_NS = FALSE;  for DEVICE_XT200_312P
// 11.13.21 MAIN_Initialize_MainXT: PARAMETERS.deviceMAX_DELAY_NS = (float)0.3125;     for DEVICE_XT200_312P
// 11.16.21 FOR SECONDARY TROMBONE ... DO NOT ENABLE WEB SERVER BECAUSE OF PORT B CONFLICT
// 11.19.21 HW_RELAYS.CURRENT_STATE -- REMOVED -- NOT USED

// 11.19.21 X SERIES FINAL PRODUCTION CODE VERSION 1.12 BUILD 2112_RD102121_RD111121-------------------------
// 11.19.21 X SERIES FINAL PRODUCTION CODE VERSION 1.12 BUILD 2112_RD102121_RD111121-------------------------
// 11.19.21 X SERIES FINAL PRODUCTION CODE VERSION 1.12 BUILD 2112_RD102121_RD111121-------------------------

// 11.22.21 X SERIES FINAL PRODUCTION CODE VERSION 1.13 BUILD_2203 ------------------------------------------
// 11.22.21 X SERIES FINAL PRODUCTION CODE VERSION 1.13 BUILD_2203 ------------------------------------------
// 11.22.21 X SERIES FINAL PRODUCTION CODE VERSION 1.13 BUILD_2203 ------------------------------------------

// 02.02.22 SYSTEM_SaveNVParametersXT: PRESERVE SERIAL PORT B WHEN WRITING TO USER BLOCK UPDATE VER 1.14
// 02.11.22 UPDATED WEB_SERVER.LIB FOR HIGHER PRECISION DISPLAY FOR XT_200_312P
// 02.16.22 UPDATES TO SECONDARY_TROMBONE VER 1.15 CODE TO HANDLE FIRMWARE UPDATE AND '>' CHAR FROM PRIMARY COMMAND
// 02.16.22 VERSION 1.15
// 04.11.22 VERSION 1.16 UPDATE
// 08.17.22 VERSION 1.17 USES UPDATED B2203_COMMANDS.LIB FOR BUG FIX WITH SEC TROMBONE *OPC? AND OPERATION COMPLETE

// 08.18.22 X SERIES FINAL PRODUCTION CODE VERSION 1.17 BUILD_2203 ------------------------------------------
// 08.18.22 X SERIES FINAL PRODUCTION CODE VERSION 1.17 BUILD_2203 ------------------------------------------
// 08.18.22 X SERIES FINAL PRODUCTION CODE VERSION 1.17 BUILD_2203 ------------------------------------------

/* Set default scope */
//#class auto
#memmap xmem // default to use eXtended memory (rather than ROOT) space
#define USE_FAR_STRING_LIB

//#define DEBUG_APP // ENABLE TO DEBUG ELSE PRODUCTION
#ifdef DEBUG_APP
#define DEBUG_WEB // ENABLE OR SUPPRESS WEB_SERVER
#else
#nodebug // NO DEBUG - PRODUCTION CODE
#endif

//---------------------------------------------------------------------------------------------------------------------//
//
// 1. MUST DEFINE ONE SPECIFIC DEVICE TYPE
//
#define DEVICE_XT100
//#define DEVICE_XT200
//#define DEVICE_XR100

// 11.11.21 BUILD2112_RD102121_RD111121
// 11.13.21 MUST ALSO INCLUDE #DEFINE DEVICE_XT200 INCLUDING DEVICE_XT200_312P
// IF DEVICE_XT200_312P AS PRIMARY TROMBONE, MUST ALSO DEFINE DEVICE_XT200
//#define DEVICE_XT200_312P
#ifdef DEVICE_XT200_312P
#ifndef DEVICE_XT200
#warns "MUST DEFINE DEVICE TYPE DEVICE_XT200 IF DEFINING DEVICE_XT200_312P"
#endif
#endif

//#define DEVICE_XT100_312P
//#define DEVICE_XT300_312P_2
//#define DEVICE_XT300_312P_3

// 10.22.21 BUILD RD102121
// IF DEVICE_XT100_200N THEN MUST USE UL TABLE
// #define DEVICE_XT100_200N
#ifdef DEVICE_XT100_200N
// 11.07.21 USE THE UL TABLE FOR DELAY VALUES // ONLY WITH DEVICE_XT100_200N
#define USE_DELAY_UL_TABLE
#endif

#ifndef DEVICE_XT100
#ifndef DEVICE_XT200
#ifndef DEVICE_XR100
#ifndef DEVICE_XT100_312P
#warns "MUST DEFINE DEVICE TYPE DEVICE_XT100 DEVICE_XT200 OR DEVICE_XR100"
#endif
#endif
#endif
#endif

//#define SECONDARY_TROMBONE
#ifdef SECONDARY_TROMBONE
#ifndef DEVICE_XT100
#ifndef DEVICE_XT100_312P
#warns "MUST DEFINE DEVICE TYPE DEVICE_XT100 IF SECONDARY_TROMBONE"
#endif
#endif
#endif

#ifdef DEVICE_XT200
#ifdef SECONDARY_TROMBONE
#warns "MUST DEFINE DEVICE TYPE DEVICE_XT100 IF SECONDARY TROMBONE"
#endif
// IF DEVICE_XT200 THEN MUST BE PRIMARY TROMBONE
#define PRIMARY_TROMBONE
#endif

//---------------------------------------------------------------------------------------------------------------------//

//
//  THESE ARE THE INTERNAL DATA STRUCTURES FOR INSTRUMENT TO EMULATE THE HARDWARE
//

// TURN ON OR OFF WEB_SERVER CAPABILITY //
#define ENABLE_WEB_SERVER

#use X_SER_ENET_B2203.LIB // 04.30.07 use VERSION 3 of ENET.LIB for use with DOWNLOADER if NOT USING WEB_SERVER

// 11.11.21 BUILD2112_RD102121_RD111121
// 11.16.21 CANNOT HAVE WEB_SERVER AND SECONDARY_TROMBONE DEFINED BECAUSE OF PORT B CONFLICT
#ifdef ENABLE_WEB_SERVER
#ifdef SECONDARY_TROMBONE
#warns "CANNOT ENABLE_WEB_SERVER AND SECONDARY_TROMBONE - PORT B CONFLICT"
#endif
#endif

#ifdef ENABLE_WEB_SERVER
#define WEB_SERVER
#endif

#ifdef WEB_SERVER
// this works #use WEB_INT_HW3VER1_B2106_HW3RD01-BROWSE-LED.LIB // 08.28.09 use WEB_INTERFACE for WEB_SERVER FOR XT-100
#use X_SER_WEB_SERVER_B2203.LIB // 08.28.09 use WEB_INTERFACE for WEB_SERVER FOR XT-100
#endif

// SPI DEFINES NEEDED FOR RCM6700
#define CLOCK_PORT D
#define CLOCK_BIT 0
// PD0 is the clock and PC0 is the data bit #
#define SPI_RX_PORT SPI_RX_PD
#define SPI_SER_D
// DEBUG FOR SPI
//#define SPI_DEBUG
#use SPI.LIB
// DEBUG FOR I2C
#define I2C_DEBUG
#use I2C_HW.lib

#define WRITE_TIME 5

#use X_SER_HWIO_B2203.LIB
#use X_SER_MOTOR_B2203.LIB
#use X_SER_COMMANDS_B2203.LIB
#use X_SER_SYSTEM_B2203.LIB

// ----------------------------------------------------------------
// GLOBAL Variables
// ----------------------------------------------------------------

// MOTOR COMMANDS
const static char Motor_FL[] = "0FL";	// feed to length
const static char Motor_SC[] = "0SC";	//
const static char Motor_DI[] = "0DI";	//
const static char Motor_FS[] = "0FS";	//
const static char Motor_IS[] = "0IS";	// input status
const static char Motor_DL[] = "0DL";	//
const static char Motor_EP[] = "0EP";	//
const static char Motor_SP[] = "0SP";	//
const static char Motor_IP[] = "0IP";	// read current location
const static char Motor_AR[] = "0AR";	// alarm reset
const static char Motor_AL[] = "0AL";	// alarm code
const static char Motor_FP[] = "0FP";	// feed position
const static char Motor_RE[] = "0RE";	// reset
const static char Motor_ME[] = "0ME";	// motor enable
const static char Motor_VE[] = "0VE";	// read velocity
const static char Motor_AC[] = "0AC";	// read acceleration
const static char Motor_DE[] = "0DE";	// read deceleration
const static char Motor_ER[] = "0ER";	// read encoder resolution
const static char Motor_RS[] = "0RS";	// request status
const static char Motor_MO[] = "0FS1H"; // feed motor until signal goes HIGH - XT SYSTEM BOARD //
const static char Motor_MD[] = "0DI";	// set DI value
const static char Motor_IV[] = "0IV";	// immediate velocity
const static char strCRLF[] = "\r\n";

//
// GLOBALS VARIABLES
//

short int stateSERIAL_CHAR_PORTC_IN;
short int stateCOMMAND_LINE_PORTC_ENTER;
short int stateCOMMAND_LINE_PORTC_ENTER_INIT_MOTOR;
short int stateSERIAL_CHAR_PORTC_IN_INIT_MOTOR;
short int stateMOTOR_RESPONSE_COMPLETE;

char CharFromSerialPortC;
static char strCOMMAND_LINE_PORTC[100];
static char strCharFromSerialPortC[2];

char cmdCOMMAND[INPUT_BUFFER_SIZE_MAX]; // contains entire command line input  // was 100 02.01.18
char cmdARG1[cmdARG1_MAX];				// argument#1 - after parsing
char cmdARG2[cmdARG2_MAX];				// argument#2
char cmdARG3[cmdARG3_MAX];				// argument#3
char cmdBUFFER[INPUT_BUFFER_SIZE_MAX];	// pending command line buffer             // was 100 02.01.18
short cmdINDEX;							// index into pending cmdCOMMAND[] array

static const char COMMAND_PROMPT[] = "\n\rCommand:";

typedef struct
{
	unsigned int nv_dev_ops;			   // number of operations device has performed  (not used! else too much wear on Flash memory user block, only 10K writes lifetime)
	long nv_ip_addr;					   // static IP address
	long nv_netmask;					   // netmask
	long nv_gateway;					   // gateway
	int nv_port;						   // port ID to use
	char nv_useDHCP;					   // TRUE == use DHCP, FALSE == use static IP addr
	char nv_terminal_mode;				   // TRUE == use RS-232 port in TERMINAL MODE, FALSE == use RS-232 port in MT-100A LCD TERMINAL
										   // NOTE: The following XORsum byte should remain in this structure.
	char nv_XSUM;						   // This is used to test the validity of the structure in the User Block.
	int nv_overshoot;					   // indicate whether to overshoot delay settings (for increased repeatability)
	int nv_overshoot_PS;				   // amount of overshoot to apply in ps
	int nv_autodrop;					   // 03.16.15 save the autodrop connections over a power cycle
	int nv_nsps_cycle_mode;				   // 03.28.18 added for XT-200/CPDL-200A stores the ns/ps button cycle mode (default = CYCLE_UNIT)
	int nv_cal_table[SIZE_CAL_TABLE];	   // float for PDL-1000A # of PS with 3 decimal pt precision adjustment
	char nv_cal_info[SIZE_CAL_INFO_FIELD]; // calibration table information max of 128 characters
	char nv_useCTSTORE;					   // use CAL TABLE (CTSTORE)
										   //#ifdef WEB_SERVER
	char nv_description[200];			   // 02.04.21 instrument description
	char nv_password[16];				   // 02.04.21 added for web_server_support and changed length (from 40) to 16
										   //#endif
	char nv_hostname[16];				   // hostname // 01.26.21 added
	int nv_cal_date_month;				   // calibration month, day, year
	int nv_cal_date_day;
	int nv_cal_date_year;

} DEVICE_NVPARAMETERS;

DEVICE_NVPARAMETERS g_NVParameters;

//
// DISPLAY_SETTINGS
//

typedef struct Settings
{
	// for XT-100
	float CURRENT_DELAY_F;	   // current delay value as float for display in Command line
	float CURRENT_DELAY_E;	   // current delay (as a float var) for display
	float CURRENT_STEP_SIZE_E; // current step size (as a float var) for display

	// for XT-200
	float CURRENT_DELAY_ONE_F; // current delay value as float for display in Command line
	float CURRENT_DELAY_ONE_E; // current delay (as a float var) for display

	float CURRENT_DELAY_TWO_F; // current delay value as float for display in Command line
	float CURRENT_DELAY_TWO_E; // current delay (as a float var) for display

	// for XT-300 TBD
};
struct Settings DISPLAY_SETTINGS;

//
// INSTRUMENT_SETTINGS
//

typedef struct InstSettings
{
	short CURRENT_UNITS;				  // either PS or NS.
	float CURRENT_STEP_SIZE;			  // current Step Size
	float CURRENT_DELAY;				  // current delay value in picoseconds
	float CURRENT_DELAY_ONE_PS;			  // current delay value in picoseconds for Channel One
	float CURRENT_DELAY_TWO_PS;			  // current delay value in picoseconds for Channel Two
	float CURRENT_DELAY_ONE_F;			  // 03.28.18 added
	float CURRENT_DELAY_TWO_F;			  // 03.28.18 added
	float CURRENT_DELAY_ONE_E;			  // 03.28.18 added
	float CURRENT_DELAY_TWO_E;			  // 03.28.18 added
	unsigned long CURRENT_BAR_GRAPH;	  // ADDED 02.05.2021 FOR BARGRAPH RD02
	unsigned char CURRENT_LAN_LED_STATUS; // ADDED 02.05.2021 FOR BARGRAPH RD02
};
struct InstSettings INSTRUMENT_SETTINGS;

//
// INSTRUMENT
// Hardware State machine -- boolean variables
// these stateXXXXX variables are used as triggers (in waitfor() commands) to trigger action
//

typedef struct statevars
{
	unsigned char statePARSE;			   // TRUE = Parse cmdCOMMAND[] array into cmdARG1, cmdARG2, cmdARG3
	unsigned char stateERROR;			   // TRUE = Error condition.  See stateERROR_CODE for error code.
	unsigned char stateSER_PORT_B_CHAR;	   // TRUE = valid char available on serial port B
	unsigned char stateSER_PORT_E_CHAR;	   // TRUE = valid char available on serial port E (MT-100A)
	unsigned char stateSER_PORT_C_CHAR;	   // TRUE = valid char available on serial port MOTOR
	unsigned char stateERROR_CODE;		   // contains error_code from previous command or 0 if command successful.
	unsigned char stateCMD_FROM_TERM;	   // TRUE indicates cmdCOMMAND[] came via SERIAL TERMINAL
	unsigned char stateCMD_FROM_LAN;	   // TRUE indicates cmdCOMMAND[] came via LAN
	unsigned char stateDEVICE_MODE;		   // == DEVICE_PARALLEL or == DEVICE_SERIAL to interpret delay commands
	unsigned char stateDEVICE_MODE_MT100A; // TRUE indicates running MT-100A over serial port, FALSE indicates running HyperTerm on serial port
	unsigned char stateDEVICE_DISPLAY_NS;  // TRUE to display in NS, FALSE to display in PS on COMMAND PROMPT. default depends on model type
	unsigned char stateMENU_MODE;		   // 0 == NORMAL, else any other number indicates MENU MODE #
	unsigned char stateMT100A_DISPLAY;	   // 03.28.18 MT-100A DISPLAY STATE: 1 = CH1+PS,2=CH1+NS,3=CH2+PS,4=CH2+NS,5=CH_BOTH+PS,6=CH_BOTH+NS
	unsigned char stateCYCLE_MODE;		   // 03.28.18 set the cycle mode of hitting the NS/PS button MT-100A
	unsigned char stateTCPIP_DATA_IN;	   // TRUE == TCPIP data available to process
	unsigned char stateTCPIP_DATA_OUT;	   // TRUE == TCPIP data available to process
	unsigned char stateMENU_MODE_LAST_RELAY;
	unsigned char stateMOTOR_ResponseProcessed; // TRUE indicates a response to a sent command has been processed
	unsigned char stateDEL_CHANNEL;				// 1 == CHANNEL 1 and 2 = CHANNEL 2 // 08.01.2017 FOR PDL-2000A
	unsigned char stateMOTOR_ResponseACK;
	unsigned char stateFACTORY_DEFAULT_PRESSED;		  // factory default button was pressed at startup
	unsigned char stateEXT_HW_INT_TRIGGERED;		  // flag if EXT HW is TRIGGERED
	unsigned char stateOPERATION_COMPLETE;			  // flag to signal when device operation is completed
	unsigned char stateOPERATION_COMPLETE_CH2;		  // flag to signal when device operation is completed
	unsigned char stateOPERATION_COMPLETE_CH3;		  // flag to signal when device operation is completed
	unsigned char stateMOTOR_MOVE_CHECK_OPC;		  // flag to indicate if this is last motor movement and to check for done to set OPC
	unsigned char stateOPC_QueryPending_CH2;		  // flag used to indicate *OPC Query is pending for CH2 and CHAR has arrived
	unsigned char stateOPC_QueryResponseReceived_CH2; // flag to indicate a CHAR response to *OPC? from the SEC trombone was received
	unsigned char stateOPC_QueryPending_CH3;		  // flag used to indicate *OPC Query is pending for CH3 and CHAR has arrived
	unsigned char stateOPC_QueryResponseReceived_CH3; // flag to indicate a CHAR response to *OPC? from the TRI trombone was received
	unsigned char stateLAST_OperationChannelNumber;	  // indicates which channel number was last operation (del1,2,or3)

	long stateMOTOR_Response_VALUE;
	enum MOTOR_COMMAND stateMOTOR_ResponseACK_TYPE;
	enum MOTOR_COMMAND stateMOTOR_Response_TYPE;
	char deviceOPTION[5];		   // to store device option type, e.g. OEM or 625PS, etc...
	char charSER_PORT_B_ONLY;	   // actual character from Serial Port B
	char charSER_PORT_E_ONLY;	   // actual character from Serial Port E
	char EXT_HW_EDGE_TYPE;		   //
	char WEB_MESSAGE_DISPLAY[100]; // Message to display in WEB SERVER MESSAGE AREA
};
struct statevars INSTRUMENT;

//
// HW_RELAYS
//

typedef struct hwrelays
{
	int SETTINGS;						// 16 BIT INTEGER VALUE CORRESPONDING ONE BIT TO EACH RELAY TO SET THE RELAYS
	unsigned int RELAY_ON_OFF[17];		// Relay values 1 thru 16, either TRUE=1 or FALSE=0
	unsigned int RELAY_DELAY_VALUE[17]; // Relay values 1 thru 16, unsigned int = 65535 MAX in PICOSECONDS
	int NUM_OF_SECTIONS;				// # of installed RELAY_SECTIONS (used in XR delay calculations)
										// 11.19.21 REMOVE -- NOT USED
										// int CURRENT_STATE;					// CURRENT STATE OF EACH RELAY WHETHER ON OR OFF

	// 10.22.21 BUILD2112_RD102121		// ADDED FOR ALL BUILDS
	//#ifdef DEVICE_XT100_200N          // 10.22.21 BUILD RD102121
	unsigned long RELAY_UL[17]; // Relay values 1 thru 16, unsigned long
};
struct hwrelays HW_RELAYS;

typedef struct motorvars
{
	long CurrentStepPosition;
	float CurrentDelaySettingPS; // 10.27.21 BUT THIS DOESNT WORK FOR 100.0 NS AND ABOVE UNITS
	float CurrentStepSizePS;
	char RESPONSE_Text[25]; // CONTAINS ENTIRE RESPONSE STRING FROM MOTOR
	long RESPONSE_Value;
	unsigned long CurrentDelaySetting_UL; // BUILD RD102121 // 10.27.21
};
struct motorvars MOTOR;

//
// PARAMETERS
//

static const char swVERSION[] = "V1.17"; // VERSION 1.00 is for XT SYSTEM BOARD
										 // VERSION 1.10 FOR BUILD_2112 // 10.18.21
										 // VERSION 1.11 FOR BUILD_2112_RD102121
										 // VERSION 1.12 FOR BUILD_2112_RD102121_RD111121
										 // VERSION 1.13 FOR BUILD_2203
										 // VERSION 1.14 FOR BUILD_2203 UPDATE
										 // VERSION 1.15 FOR BUILD_2203 UPDATE 02.16.22
										 // VERSION 1.16 FOR BUILD_2203 UPDATE 04.11.22
										 // VERSION 1.17 FOR BUILD_2203 UPDATED 08.17.22
typedef struct paramvars
{
	float deviceMAX_DELAY_PS;
	float deviceMAX_DELAY_NS; // for CPDL display startup message
	float deviceSTEP_SIZE_NS; // step size in NS (for display on startup) VER 1.7
};
struct paramvars PARAMETERS;

//
// BUFFERS
//

typedef struct buffervars
{
	char DISPLAY_LINE[INPUT_BUFFER_SIZE_MAX];		// used as output buffer to display on terminal
	char COMMAND_LINE[INPUT_BUFFER_SIZE_MAX];		// used to build Command Line display
	char tcpipBUFFER_IN[500];						// input buffer for chars received over TCPIP
	char tcpipBUFFER_OUT[500];						// output buffer for chars received over TCPIP
	char INPUT_COMMAND_LINE[INPUT_BUFFER_SIZE_MAX]; // buffer to hold rolling parsed command line 04.18.07
};
struct buffervars BUFFERS;

//
// GLOBAL_SETTINGS
//
typedef struct globalvars
{
	unsigned char LAST_RELAY_SECTION_ODD;		 // indicate whether last relay section is on even (FALSE) or odd (TRUE) boundary
	unsigned char AUTO_SET_PLUS, AUTO_SET_MINUS; // auto set to new delay value after specifying step size on +/- buttons on Microterminal
	unsigned char CALIBRATION_TEST_RESULT;		 // results of last calibration check (*CAL), *CAL? to get results
	float SET_OPTO_LOCN;						 // location of motor for special set opto detector voltage routine in DIAG menu
	unsigned char ENABLE_STEP_DIAG;				 // enables single step (full or half) to set voltage in DIAG menu
	long ELAPSED_DELAY_TIME;					 // elapsed time
	long START_DELAY_TIME;						 // start time before motor moves to new delay
	long END_DELAY_TIME;						 // end time after motor moves to new delay
	unsigned char userOVERSHOOT;				 // turn ON or OFF overshoot  added 10.04.06
	int tcpipSession;							 // The session that sent the command  // added 03.05.08 for multi-sessions
	short COMMAND_CONTINUE;						 // TRUE = semicolon in command line more command to process
	unsigned long SUM_RELAYS_LESS_1;
	char USE_CAL_TABLE; // 09.01.08 // 01.31.18 flag to indicate use NVRAM CAL TABLE OR NOT
	char COMMAND_LINE_COPY[256];
	char REMOTE_LOCAL_MODE; // INDICATE IN REMOTE MODE (TRUE) or LOCAL MODE (FALSE)
};
struct globalvars GLOBAL_SETTINGS;

//
// MOTOR
//

//---------------------------------------------------------------------------------------------------------------------//
//
// local variables for MAIN:
//

unsigned int _serial36;
short MAIN_i;
short MAIN_k;
int MAIN_charSER_PORT;
int MAIN_charSER_PORT_MOTOR;
unsigned char MAIN_IsKeyESC;
unsigned int MAIN_wait;

// 01.26.21 FOR DHCP_SEND_HOSTNAME FEATURE
static const char g_StaticMemHostName[17] = "COLBY_2203YYYY\0"; // EDIT HERE WITH SN # // DHCP_SEND_HOSTNAME feature
char g_DynamicMemHostName[17];
char *g_RetCode;

//
// GLOBAL ITEMS SPECIFIC TO EACH DEVICE BUILT
//
//---------------------------------------------------------------------------------------------------------------------//
// ENTER SERIAL NUMBER, MANUFACTURE DATE, AND MAXIMUM DELAY
//
// STEP#1 THESE MUST BE SET PER EACH DEVICE MANUFACTURED!!

static const char deviceNAME[] = "Programmable Delay Line"; // NAME

// SELECT THIS OPTION FOR XT-100 (DUAL TROMBONE UNIT, EACH CHANNEL WITH ONE 312.50 SINGLE TROMBONE
#ifdef DEVICE_XT100_312P
static const char deviceMODEL[] = "XT-100";						  // MODEL NAME XT-100
static const char versionString[] = "XT-100-312P,V1.17,2203XXXX"; //
static const char deviceOPTION[] = "000";						  // EDIT HERE // FOR PDL_100A OPTION # INSTALLED, e.g "000","OEM",or "010","020",...
static const char deviceMANUFACTURER[] = "Colby Instruments";	  // MANUFACTURER NAME
static const char deviceSN[] = "2203XXXX";						  // EDIT HERE  // ENTER YYMM and SERIAL NUMBER HERE e.g. "YYMMxxxx"
static const char deviceIDN_DISPLAY[] = "312P";					  // 10.05.21   // 312P
#endif
#ifdef DEVICE_XT100												  // AS SECONDARY TROMBONE,THIS IS A XT-100-625P FOR XT-200-312P AND XT-200-62P
static const char deviceMODEL[] = "XT-100";						  // MODEL NAME XT-100
static const char versionString[] = "XT-100-625P,V1.17,2203YYYY"; // EDIT HERE //
static const char deviceOPTION[] = "000";						  // EDIT HERE // FOR PDL_100A OPTION # INSTALLED, e.g "000","OEM",or "010","020",...
static const char deviceMANUFACTURER[] = "Colby Instruments";	  // MANUFACTURER NAME
static const char deviceSN[] = "2203YYYY";						  // EDIT HERE // ENTER YYMM and SERIAL NUMBER HERE e.g. "YYMMxxxx"
static const char deviceIDN_DISPLAY[] = "625P";					  // EDIT HERE // 625P OR 001N OR 002N OR 00
#endif

#ifdef DEVICE_XT200
static const char deviceMODEL[] = "XT-200"; // MODEL NAME XT-200
// 11.11.21 BUILD2112_RD102121_RD111121
#ifdef DEVICE_XT_200_312P
static const char versionString[] = "XT-200-312P,V1.17,2203XXXX"; // Used in WEB_SERVER
#else
static const char versionString[] = "XT-200-625P,V1.17,2203XXXX"; // Used in WEB_SERVER
#endif
static const char deviceOPTION[] = "OEM";
static const char deviceMANUFACTURER[] = "Colby Instruments";
#ifdef PRIMARY_TROMBONE
static const char deviceSN[] = "2203XXXX"; // EDIT HERE //ENTER YYMM and SERIAL NUMBER HERE e.g. "YYMMxxxx"
#else
static const char deviceSN[] = "NOTUSED";
#endif
	// 11.11.21 BUILD2112_RD102121_RD111121
#ifdef DEVICE_XT_200_312P
static const char deviceIDN_DISPLAY[] = "312P"; // FOR BASE MODEL 312.5PS
#else
static const char deviceIDN_DISPLAY[] = "625P";	  // FOR BASE MODEL 625.0PS
#endif
#endif

#ifdef DEVICE_XR100
static const char deviceMODEL[] = "XR-100";								  // MODEL NAME XT-100 or CPDL
static const char versionString[] = "XR-100-050N-010P-13,V1.XX,2203XXXX"; // EDIT HERE Used for ETH DOWNLOADER -- added for WEB_SERVER
static const char deviceMANUFACTURER[] = "Colby Instruments";			  // MANUFACTURER NAME
static const char deviceOPTION[] = "50.00";
static const char deviceSN[] = "2203XXXX";				// EDIT HERE //ENTER YYMM and SERIAL NUMBER HERE e.g. "YYMMxxxx"
static const char deviceIDN_DISPLAY[] = "050N-010P-13"; // EDIT HERE
#define MAX_DELAY_SETTING 50000.0
#if MAX_DELAY_SETTING > 65535.0
#define TEN_X
#endif
#endif

#ifdef ENABLE_WEB_SERVER
static const char deviceHOMEPAGE[] = "http://www.colbyinstruments.com";
#endif

//---------------------------------------------------------------------------------------------------------------------//

// FUNCTION DEFINITIONS USED IN MAIN.C

void MAIN_Initialize_RelaySettings(void)
{
#ifdef DEVICE_XR100
	int _Index; // INDEX TO ARRAYS TO SET TEN_X DIVISION
#endif

	// MOVE THIS CODE TO MAIN SO CAN HAVE EACH SOURCE CODE PER MACHINE SHIPPED

	HW_RELAYS.SETTINGS = 0x0000;				  // HARDWARE RELAY SETTINGS
	HWIO_REL_SetRelays_X_SER(HW_RELAYS.SETTINGS); // turn them all OFF
	HWIO_msDelay(250);

	HW_RELAYS.SETTINGS = 0xFFFF;				  // turn them all ON
	HWIO_REL_SetRelays_X_SER(HW_RELAYS.SETTINGS); // turn them all ON
	HWIO_msDelay(250);

	HW_RELAYS.SETTINGS = 0x0000;				  // turn them all OFF
	HWIO_REL_SetRelays_X_SER(HW_RELAYS.SETTINGS); // turn them all OFF
	HWIO_msDelay(250);

	//***********************************************************************************************************************
	// MUST DEFINE FOR EACH DEVICE MANUFACTURED
	// DEFINE EACH RELAY SECTION HERE WHETHER FOR XT-100 OR XR-100 MODELS
	//---------------------------------------------------------------------------------------------------------------------//
	//
	// # OF PS DELAY FOR EACH RELAY SECTION MUST BE DEFINED
	//

	HW_RELAYS.RELAY_DELAY_VALUE[0] = 625; // # OF PS OF DELAY FOR EACH RELAY SECTION
	HW_RELAYS.RELAY_DELAY_VALUE[1] = 0;	  // STEP SIZES ... SPECIFY ACCORDING TO CONFIGURATION
	HW_RELAYS.RELAY_DELAY_VALUE[2] = 0;
	HW_RELAYS.RELAY_DELAY_VALUE[3] = 0;
	HW_RELAYS.RELAY_DELAY_VALUE[4] = 0;
	HW_RELAYS.RELAY_DELAY_VALUE[5] = 0;
	HW_RELAYS.RELAY_DELAY_VALUE[6] = 0;
	HW_RELAYS.RELAY_DELAY_VALUE[7] = 0;
	HW_RELAYS.RELAY_DELAY_VALUE[8] = 0;
	HW_RELAYS.RELAY_DELAY_VALUE[9] = 0;
	HW_RELAYS.RELAY_DELAY_VALUE[10] = 0;
	HW_RELAYS.RELAY_DELAY_VALUE[11] = 0;
	HW_RELAYS.RELAY_DELAY_VALUE[12] = 0;
	HW_RELAYS.RELAY_DELAY_VALUE[13] = 0;
	HW_RELAYS.RELAY_DELAY_VALUE[14] = 0;
	HW_RELAYS.RELAY_DELAY_VALUE[15] = 0;
	HW_RELAYS.RELAY_DELAY_VALUE[16] = 0;
	HW_RELAYS.NUM_OF_SECTIONS = 0;

	// 10.21.21 FOR BUILD2112_RD102121
	// 11.07.21 INCLUDE THIS TABLE FOR ALL BUILDS BUILD2112_RD102121

	HW_RELAYS.RELAY_UL[0] = 625; // LOGICAL REPRESENTATION OF DELAY VALUES IN # OF PICOSECONDS //
	HW_RELAYS.RELAY_UL[1] = 0;	 // STEP SIZES ... SPECIFY ACCORDING TO CONFIGURATION
	HW_RELAYS.RELAY_UL[2] = 0;
	HW_RELAYS.RELAY_UL[3] = 0;
	HW_RELAYS.RELAY_UL[4] = 0;
	HW_RELAYS.RELAY_UL[5] = 0;
	HW_RELAYS.RELAY_UL[6] = 0;
	HW_RELAYS.RELAY_UL[7] = 0;
	HW_RELAYS.RELAY_UL[8] = 0;
	HW_RELAYS.RELAY_UL[9] = 0;
	HW_RELAYS.RELAY_UL[10] = 0;
	HW_RELAYS.RELAY_UL[11] = 0;
	HW_RELAYS.RELAY_UL[12] = 0;
	HW_RELAYS.RELAY_UL[13] = 0;
	HW_RELAYS.RELAY_UL[14] = 0;
	HW_RELAYS.RELAY_UL[15] = 0;
	HW_RELAYS.RELAY_UL[16] = 0;
	HW_RELAYS.NUM_OF_SECTIONS = 0;

	//#endif

#ifdef DEVICE_XR100
#ifdef TEN_X

	//
	// DIVIDE ALL VALUES IN TABLE BY 10 (ONE ORDER OF MAGNITUDE) SO CAN HANDLE TOTAL DEVICE RANGE > 65525 PS
	//

	for (_Index = 1; _Index <= 16; _Index++)
	{
		if (HW_RELAYS.RELAY_DELAY_VALUE[_Index] != 0)
		{
			HW_RELAYS.RELAY_DELAY_VALUE[_Index] = HW_RELAYS.RELAY_DELAY_VALUE[_Index] / 10;
		}
	}

#endif
#endif

	//---------------------------------------------------------------------------------------------------------------------//

	GLOBAL_SETTINGS.SUM_RELAYS_LESS_1 = 0; // MUST COMPUTE FOR XR-100 AND XT-100
	for (MAIN_i = 1; MAIN_i < HW_RELAYS.NUM_OF_SECTIONS; MAIN_i++)
	{
		GLOBAL_SETTINGS.SUM_RELAYS_LESS_1 = GLOBAL_SETTINGS.SUM_RELAYS_LESS_1 + HW_RELAYS.RELAY_DELAY_VALUE[MAIN_i];
	}

	INSTRUMENT.stateDEVICE_DISPLAY_NS = TRUE; // INITIAL DISPLAY IN NS (DEFAULT)

#ifdef DEVICE_XT100_312P
	INSTRUMENT.stateDEVICE_DISPLAY_NS = FALSE; // INITIAL DISPLAY IN PS (DEFAULT)
#endif
// 11.11.21 BUILD2112_RD102121_RD111121
#ifdef DEVICE_XT_200_312P
	INSTRUMENT.stateDEVICE_DISPLAY_NS = FALSE; // INITIAL DISPLAY IN PS (DEFAULT)
#endif

	//
	// GLOBAL_SETTINGS.LAST_SECTION_ODD == TRUE indicates that the last relay section delay
	// is LESS than the next to last relay delay because total delay
	// range does not fall on an even Binary Step Size boundary.
	//

	GLOBAL_SETTINGS.LAST_RELAY_SECTION_ODD = FALSE;

	if (HW_RELAYS.NUM_OF_SECTIONS != 0)
	{ // don't need to count for TROMBONE ONLY XT-100
		if (HW_RELAYS.RELAY_DELAY_VALUE[HW_RELAYS.NUM_OF_SECTIONS] < HW_RELAYS.RELAY_DELAY_VALUE[HW_RELAYS.NUM_OF_SECTIONS - 1])
		{
			GLOBAL_SETTINGS.LAST_RELAY_SECTION_ODD = TRUE;
		}
	}

	for (MAIN_i = 0; MAIN_i <= 16; MAIN_i++)
	{
		HW_RELAYS.RELAY_ON_OFF[MAIN_i] = FALSE; // HW_RELAYS.RELAY_ON_OFF reflects the current relay switch status
	}											// CLEAR OUT TO ALL OFF (FALSE)

} // void MAIN_Initialize_RelaySettings(void) //

char MAIN_CheckFactoryReset()
{
	//
	// CHECK IF THE FACTORY RESET BUTTON IS PRESSED
	//

	char _ResetButtonPressed;
	char _Bit;

	_ResetButtonPressed = FALSE;

	_Bit = BitRdPortI(PBDR, 2);
	if (_Bit == 0)
	{
		HWIO_msDelay(500);
		if ((BitRdPortI(PBDR, 2)) == 0)
		{
			return TRUE;
		}
		else
		{
			return FALSE;
		}
	}
	else
	{
		return FALSE;
	}

	return FALSE;
}

void MAIN_Initialize_MainXT(void)
{

	HWIO_Initialize_Variables();
	HWIO_Initialize_BarGraphXT();

	// CHECK TO SEE IF RESET TO FACTORY BUTTON IS PRESSED
	if (MAIN_CheckFactoryReset() == TRUE)
	{
		// FLASH THE BAR GRAPH OFF - ON - OFF
		for (MAIN_i = 0; MAIN_i < 5; MAIN_i++)
		{
			INSTRUMENT_SETTINGS.CURRENT_BAR_GRAPH = 0x000FFFFF;
			HWIO_ShiftRegBarGraphOutputXT(INSTRUMENT_SETTINGS.CURRENT_BAR_GRAPH);
			HWIO_msDelay(200);

			INSTRUMENT_SETTINGS.CURRENT_BAR_GRAPH = 0x00000000;
			HWIO_ShiftRegBarGraphOutputXT(INSTRUMENT_SETTINGS.CURRENT_BAR_GRAPH);
			HWIO_msDelay(100);
		}
		INSTRUMENT.stateFACTORY_DEFAULT_PRESSED = TRUE; // FLAG THIS CONDITION
	}

// 05.27.21 SET THE TTL DIRECTION BIT
#ifndef SECONDARY_TROMBONE
	// SEND MASTER BIT ON FOR TTL DIRECTION
	BitWrPortI(PADR, &PADRShadow, TRUE, 4); // HIGH FOR PA4
#else
	// MASTER BIT IS LOW SINCE WE ARE THE SECONDARY
	// DE-ASSERT THIS PORT LINE HIGH (PA4) SINCE WE ARE NOT THE MASTER
	BitWrPortI(PADR, &PADRShadow, FALSE, 4); // LOW FOR PA4
#endif

	// 04.30.21 moved here because calls LoadNVParameters()
	// 04.30.21 calls to loadNVParameters use Serial Port B (between trombones)
	// Start up the Ethernet Connection
	HWIO_Initialize_Ethernet();

	// Initialize the Serial Ports
	// 04.30.21 make sure to re-initialize serial ports after calling Load_NVParameters
	HWIO_Initialize_SerialPortsXT();

	// Initialize the I2C and all Relay Boards for OUTPUT
	// INITIALIZE THE I2C INTERFACE
	I2C_Init();					// initialize the I2C
	HWIO_Initialize_RelaysXT(); // Set all relay boards for OUTPUT

	MAIN_Initialize_RelaySettings(); // SPECIFIC DEVICE SETTINGS

	// display interrupt and see if can set debug breakpoints
	// Init_XIRQ(_XIRQ_EDGE_NONE);  // disable the interrupts by edge to none
	// Test_EXT_IRQ();

#ifndef DEVICE_XR100
	HWIO_msDelay(1000); // WAIT TIME for the motor to startup
						// No motor in XR100
	// Initialize Motor through RS485 serial port
	MOTOR_Initialize();
	MOTOR.CurrentDelaySettingPS = 0;  // 02.05.18 -- ensure starting point is at ZERO
	MOTOR.CurrentDelaySetting_UL = 0; // 10.27.21 -- added
#endif

	//***********************************************************************************************************************
	// MUST DEFINE FOR EACH DEVICE MANUFACTURED
	//
	// THIS VALUE MUST BE SET FOR EACH DEVICE TYPE.  THIS IS THE MAX DELAY IN PS
	//---------------------------------------------------------------------------------------------------------------------//

#ifdef DEVICE_XT100_312P
	PARAMETERS.deviceMAX_DELAY_PS = (float)625.00; // MAX DELAY IN NUMBER OF PICOSECONDS, E.G. "XXXXX.XX"  // 10.14.21 was 625.00
												   // XT100_312P OPERATES IN PARALLEL MODE SO MAX DELAY IS 625.0 PS
	PARAMETERS.deviceMAX_DELAY_NS = (float)0.3125; // for STARTUP DISPLAY PURPOSES, MAX DELAY IN NUMBER OF NANOSECONDS
												   // 0.312 for XT-100-312PS HALF TROMBONE
												   // 0.625 for XT-100-625PS TROMBONE ONLY
												   // 10.00 for XT-100-10NS
												   // 20.00 for XT-100-20NS
	PARAMETERS.deviceSTEP_SIZE_NS = 0.00025;	   // 10.14.21 change for XT-100-312P (was 0.0005)
#endif

#ifdef DEVICE_XT100
	PARAMETERS.deviceMAX_DELAY_PS = (float)625.0; // EDIT HERE // MAX DELAY IN NUMBER OF PICOSECONDS, E.G. "XXXXX.XX"
												  // 625.00 for XT-100-000 TROMBONE ONLY
												  // 10000.00 for XT-100-010 for 10 NS Version
	PARAMETERS.deviceMAX_DELAY_NS = (float)0.625; // EDIT HERE // for STARTUP DISPLAY PURPOSES, MAX DELAY IN NUMBER OF NANOSECONDS
												  // 0.312 for XT-100-312PS HALF TROMBONE
												  // 0.625 for XT-100-625PS TROMBONE ONLY
												  // 10.00 for XT-100-10NS
												  // 20.00 for XT-100-20NS
	PARAMETERS.deviceSTEP_SIZE_NS = 0.0005;
#endif

#ifdef DEVICE_XT200
	PARAMETERS.deviceMAX_DELAY_PS = (float)625.0; // MAX DELAY IN NUMBER OF PICOSECONDS, E.G. "XXXXX.XX"

// 11.11.21 BUILD2112_RD102121_RD111121
#ifdef DEVICE_XT200_312P
	PARAMETERS.deviceMAX_DELAY_NS = (float)0.3125; // for STARTUP DISPLAY PURPOSES, MAX DELAY IN NUMBER OF NANOSECONDS
#else
	PARAMETERS.deviceMAX_DELAY_NS = (float)0.625; // for STARTUP DISPLAY PURPOSES, MAX DELAY IN NUMBER OF NANOSECONDS
#endif
#endif

	// MUST DEFINE FOR XR-100 UNITS	-- XR-100 -- SPECIFY HERE -- for EACH instrument
#ifdef DEVICE_XR100
	PARAMETERS.deviceMAX_DELAY_PS = (float)50000.0; // MAX DELAY IN NUMBER OF PICOSECONDS, E.G. "XXXXX.XX"
	PARAMETERS.deviceMAX_DELAY_NS = (float)50.0;	// for STARTUP DISPLAY PURPOSES, MAX DELAY IN NUMBER OF NANOSECONDS

	PARAMETERS.deviceSTEP_SIZE_NS = (float)0.010; // for startup display of step size and range in XR-100 model
												  // NOT USED in XT-100 // 0.010 == 10 PS step size
#endif

	// INITIALIZE ALL INSTRUMENT VARIABLES AND SETTINGS
	HWIO_Initialize_InstrumentVariables();

} // void MAIN_Initialize_MainXT(void)

void MAIN_WhileLoop_XT(void)
{
	//
	// MAIN Code Loop
	//

	while (1)
	{ // MAIN() program while loop

		////////////////////////////////////////////////////////////////////////////////

		ENET_Handler(); // Service the Ethernet

#ifdef ENABLE_WEB_SERVER
		http_handler(); // HTTP server // RD01 added 02.06.21 WEB_SERVER
#endif

#ifdef DEVICE_XT200
#ifdef PRIMARY_TROMBONE
		// PRIMARY TROMBONE LISTENS ON SERIAL PORT B FOR RESPONSES FROM SECONDARY
		// SERIAL PORT B
		if ((MAIN_charSER_PORT = serBgetc()) != -1)
		{ // ANY CHARS FROM THE SECONDARY?
			if (MAIN_charSER_PORT != 0)
			{
				INSTRUMENT.stateSER_PORT_B_CHAR = TRUE; // check Serial Port B
				INSTRUMENT.charSER_PORT_B_ONLY = MAIN_charSER_PORT;
			}
		}
#endif
#endif

#ifdef SECONDARY_TROMBONE
		// SECONDARY TROMBONE LISTENS ON SERIAL PORT B FOR COMMANDS FROM PRIMARY
		// SERIAL PORT B
		if ((MAIN_charSER_PORT = serBgetc()) != -1)
		{ // ANY CHARS FROM THE PRIMARY?
			if (MAIN_charSER_PORT != 0)
			{
				INSTRUMENT.stateSER_PORT_B_CHAR = TRUE; // check Serial Port B
				INSTRUMENT.charSER_PORT_B_ONLY = MAIN_charSER_PORT;
			}
		}
#endif

// 04.19.18 add for DEVICE_XR100 - Any MOTOR related code is NOT needed
#ifndef DEVICE_XR100
		// SERIAL PORT C MOTOR
		if ((MAIN_charSER_PORT_MOTOR = serCgetc()) != -1) // ANY CHARS FROM MOTOR?
			INSTRUMENT.stateSER_PORT_C_CHAR = TRUE;		  // CHECK SERIAL PORT C
#endif

		// SERIAL PORT E MT-100A
		if ((MAIN_charSER_PORT = serEgetc()) != -1) // ANY CHARS FROM RS-232 PORT?
		{
			INSTRUMENT.stateSER_PORT_E_CHAR = TRUE; // CHECK SERIAL PORT E
			INSTRUMENT.charSER_PORT_E_ONLY = MAIN_charSER_PORT;
		}

		costate
		{
			waitfor(INSTRUMENT.stateTCPIP_DATA_IN);		  // ANY CHARS FROM TCPIP?
			INSTRUMENT.stateTCPIP_DATA_IN = FALSE;		  // RESET THE FLAG
			memset(cmdCOMMAND, 0x00, sizeof(cmdCOMMAND)); // CLEAR OUT THE BUFFER
			if (strlen(BUFFERS.tcpipBUFFER_IN) > INPUT_BUFFER_SIZE_MAX)
			{
				// potential OVERFLOW PROBLEM ... too many characters received over ETHERNET
				// therefore cut it off by making it an end of string character at the end of it
				BUFFERS.tcpipBUFFER_IN[INPUT_BUFFER_SIZE_MAX - 1] = 0x00; // NULL CHAR
			}
			strcpy(BUFFERS.INPUT_COMMAND_LINE, BUFFERS.tcpipBUFFER_IN); // copy into global buffer
			GLOBAL_SETTINGS.tcpipSession = g_ENETactiveSession;			// record the current session
			SYSTEM_ExtractOneCommand();
			if (strlen(cmdCOMMAND) != 0)		 // see if command that needs parsing
				INSTRUMENT.statePARSE = TRUE;	 // set this flag to TRUE to trigger action!
			INSTRUMENT.stateCMD_FROM_LAN = TRUE; // indicate the source of the command was from LAN
		}										 // end costate stateTCPIP_DATA_IN

		costate
		{
			// statePARSE triggered when data in is cmdCOMMAND[] to be parsed
			waitfor(INSTRUMENT.statePARSE); // statePARSE == TRUE to trigger
			INSTRUMENT.statePARSE = FALSE;	// reset the flag
			// use SYSTEM_ParseInputCommand to parse cmdCOMMAND[] into 3 components cmdARG1,2,3
			if (strlen(cmdCOMMAND) != 0)
			{
				SYSTEM_ParseInputCommand(cmdCOMMAND);
			}

			// SPECIAL CASE -- ESCAPE KEY CLEAR HIT?
			if (strcmp(cmdARG1, "\x1B") == 0)
			{
				INSTRUMENT.stateMENU_MODE = 0;
				INSTRUMENT.stateERROR_CODE = NO_ERROR;
				sprintf(cmdARG1, "");
				// 11.18.21 BUILD2203
				// 11.18.21 ESCAPE KEY TRIGGERS THE TERMINAL MODE MEANING MT-100A IS ATTACHED
				INSTRUMENT.stateDEVICE_MODE_MT100A = TRUE;
			}
			// SCAN FOR ESC CHAR IS IN cmdARG1
			MAIN_IsKeyESC = FALSE;
			for (MAIN_k = 0; MAIN_k <= strlen(cmdARG1); MAIN_k++)
			{
				if (cmdARG1[MAIN_k] == '\x1B')
				{
					MAIN_IsKeyESC = TRUE;
					break;
				}
			} // end for
			if (MAIN_IsKeyESC == TRUE)
			{
				INSTRUMENT.stateMENU_MODE = 0;
				INSTRUMENT.stateERROR_CODE = NO_ERROR;
				sprintf(cmdARG1, "");
			}

			// CHECK IF KEYS ENTERED ARE DURING READING OF NETWORK ADDRESS SETTING
			if (INSTRUMENT.stateMENU_MODE != 0)
			{
				// a network address was entered into cmdARG1, so call SYSTEM_HandleMenuMode directly
				SYSTEM_HandleMenuMode();
			}
			else
			{
				// Command is parsed into cmdARG1,cmdARG2,cmdARG3.  Decode and process.
				SYSTEM_ExecuteCommand();
			} // end else-if

			//
			// POST-PROCESSING ... Command has been completed
			// cmdCOMMAND[] was processed so issue a prompt only if previous command was from TERMINAL
			// and the Microterminal is NOT in MENU MODE.
			// Check also to see if there are multiple commands so those need to be processed too.
			//
			// if the COMMAND[] came from the MT-100A, then only ONE command is possible to have
			// been processed.  Issue a command prompt if COMMAND[] came from MT-100A.
			//

			if ((INSTRUMENT.stateCMD_FROM_TERM) && (INSTRUMENT.stateMENU_MODE == FALSE))
			{
				INSTRUMENT.stateCMD_FROM_TERM = FALSE;
				memset(cmdARG1, 0x00, sizeof(cmdARG1)); // clear out this buffer for next time
				memset(cmdARG2, 0x00, sizeof(cmdARG2));
				memset(cmdARG3, 0x00, sizeof(cmdARG3));
			} // end if

			// added 02.21.07 don't reset the stateCMD_FROM_LAN until LAST command is finished
			if ((INSTRUMENT.stateCMD_FROM_LAN) && (!GLOBAL_SETTINGS.COMMAND_CONTINUE))
			{
				INSTRUMENT.stateCMD_FROM_LAN = FALSE;
				INSTRUMENT.stateCMD_FROM_TERM = FALSE;
				memset(cmdARG1, 0x00, sizeof(cmdARG1)); // 11.19.21 CLEAR OUT THIS BUFFER FOR NEXT TIME
				memset(cmdARG2, 0x00, sizeof(cmdARG2));
				memset(cmdARG3, 0x00, sizeof(cmdARG3));

				// 11.19.21 WHY DO THIS AT ALL?
				// sprintf(BUFFERS.DISPLAY_LINE, "\r\n");
				// SYSTEM_OutputTerminal(BUFFERS.DISPLAY_LINE);
			}

			//
			// DISPLAY PROMPT ON MT-100A IF NOT IN MENU_MODE
			//

			if (INSTRUMENT.stateMENU_MODE == FALSE)
			{
				SYSTEM_OutputPrompt();
			}

			// if there are more commands to process, extract the next one and
			// set flag to indicate there is another command to parse

			if (GLOBAL_SETTINGS.COMMAND_CONTINUE)
			{
				SYSTEM_ExtractOneCommand();	  // get next command into cmdCOMMAND
				INSTRUMENT.statePARSE = TRUE; // indicate there are more commands
											  // to follow because of ;
			}								  // end-if
		}									  // end of costate

		costate
		{
			waitfor(INSTRUMENT.stateTCPIP_DATA_OUT);
			INSTRUMENT.stateTCPIP_DATA_OUT = FALSE;															   // reset the flag
			ENET_Send(GLOBAL_SETTINGS.tcpipSession, BUFFERS.tcpipBUFFER_OUT, strlen(BUFFERS.tcpipBUFFER_OUT)); // send
		}																									   // end costate stateTCPIP_DATA_IN

		costate
		{
			waitfor(INSTRUMENT.stateERROR);
			INSTRUMENT.stateERROR = FALSE; // toggle stateERROR

			if (INSTRUMENT.stateERROR_CODE == BUFFER_OVERFLOW)
				SYSTEM_OutputPrompt(); // send a new COMMAND prompt out
		}							   // end costate stateERROR;

#ifdef DEVICE_XT200
#ifdef PRIMARY_TROMBONE
		costate
		{											  // if we are PRIMARY_TROMBONE monitor Serial Port B for input from SECONDARY
			waitfor(INSTRUMENT.stateSER_PORT_B_CHAR); // char in serial port B from PRIMARY TROMBONE
			INSTRUMENT.stateSER_PORT_B_CHAR = FALSE;  // toggle stateSER_PORT_CHAR;
			SYSTEM_ServiceSerialPortB_Char();
		} // end costate stateSER_PORT_CHAR

		costate
		{
			waitfor(INSTRUMENT.stateOPC_QueryResponseReceived_CH2); // *OPC? reply CHAR char in serial port B from SECONDARY TROMBONE
			INSTRUMENT.stateOPC_QueryResponseReceived_CH2 = FALSE;	// toggle stateSER_PORT_CHAR;
			SYSTEM_ServiceOPC_Response_CH2();						// SEND the *OPC? response back to whoever asked us !
		}
#endif
#endif

#ifdef SECONDARY_TROMBONE
		costate
		{											  // if we are SECONDARY_TROMBONE monitor Serial Port B for input from Primary
			waitfor(INSTRUMENT.stateSER_PORT_B_CHAR); // char in serial port B from PRIMARY TROMBONE
			INSTRUMENT.stateSER_PORT_B_CHAR = FALSE;  // toggle stateSER_PORT_CHAR;
			SYSTEM_ServiceSerialPortB_Char();
		} // end costate stateSER_PORT_CHAR
#endif
		costate
		{
			waitfor(INSTRUMENT.stateSER_PORT_E_CHAR); // char in serial port E from MT-100A
			INSTRUMENT.stateSER_PORT_E_CHAR = FALSE;  // toggle stateSER_PORT_CHAR;
			SYSTEM_ServiceSerialPortE_Char();
		} // end costate stateSER_PORT_CHAR

		// NO MOTOR IN DEVICE_XR100
#ifndef DEVICE_XR100
		costate
		{
			waitfor(INSTRUMENT.stateSER_PORT_C_CHAR); // char in serial port from MOTOR
			INSTRUMENT.stateSER_PORT_C_CHAR = FALSE;  // toggle stateSER_PORT_C_CHAR;
			//
			// for each char from the MOTOR, add into MOTOR_Response until a \r
			// is received to signal to process the entire response line
			//
			if (MAIN_charSER_PORT_MOTOR != 0x0D)
			{
				// build the response line string by adding each character
				// strcat(MOTOR_Response,MAIN_charSER_PORT_MOTOR);
				strCharFromSerialPortC[0] = MAIN_charSER_PORT_MOTOR;
				strCharFromSerialPortC[1] = 0; // null
				strcat(MOTOR.RESPONSE_Text, strCharFromSerialPortC);
			}
			else
			{
				// 0x0D terminates a line of response from the Motor
				// decode the response line into corresponding values
				MOTOR_ParseResponse(MOTOR.RESPONSE_Text);
				memset(MOTOR.RESPONSE_Text, 0x00, sizeof(MOTOR.RESPONSE_Text)); // clear out buffer
			}
		} // end costate stateSER_PORT_C_CHAR
#endif
		costate
		{
			waitfor(INSTRUMENT.stateEXT_HW_INT_TRIGGERED); // EXTERNAL HW INT TRIGGERED
			INSTRUMENT.stateEXT_HW_INT_TRIGGERED = FALSE;  // reset flag
														   // do processing based on EXT HW INT TRIGGERED ...
		}
	} // end MAIN() while (1)

} // void MAIN_WhileLoop_XT(void) //

//////////////////////////////////////////////////////////////////////////////
////////////////////////////    MAIN    //////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

void main(void)
{
	// =====>>> START HERE
	//
	// SHOULD PRE INITIALIZE ALL GLOBAL VARIABLES //
	//

	MAIN_i = MAIN_k = 0;
	MAIN_charSER_PORT = 0;
	MAIN_IsKeyESC = 0;
	MAIN_wait = 0;

	for (MAIN_i = 0; MAIN_i < INPUT_BUFFER_SIZE_MAX; MAIN_i++)
	{
		BUFFERS.DISPLAY_LINE[MAIN_i] = 0;
		BUFFERS.COMMAND_LINE[MAIN_i] = 0;
		BUFFERS.INPUT_COMMAND_LINE[MAIN_i] = 0;
	}
	for (MAIN_i = 0; MAIN_i < 500; MAIN_i++)
	{
		BUFFERS.tcpipBUFFER_IN[MAIN_i] = 0;
		BUFFERS.tcpipBUFFER_OUT[MAIN_i] = 0;
	}
	for (MAIN_i = 0; MAIN_i < sizeof(MOTOR.RESPONSE_Text); MAIN_i++)
	{
		MOTOR.RESPONSE_Text[MAIN_i] = 0;
	}
	MOTOR.CurrentStepPosition = 0;
	// END PRE-INITIALIZATION GLOBAL VARIABLES

	HWIO_PreInit_XT_HW();	  // FOR XT-100 SYSTEM BOARD // 04.27.21
	MAIN_Initialize_MainXT(); // FOR XT SYSTEM BOARD	05.25.21
	cmdRST(1);				  // MUST DO THIS TO HAVE ETHERNET PORTS COME UP CORRECTLY
	SYSTEM_OutputPrompt();	  // send out FIRST COMMAND: prompt

#ifdef ENABLE_WEB_SERVER
	Web_Init(); // RD01 - initialize web variables // RD01 added 02.06.21 WEB_SERVER
#endif

	///////////////////////////////////////////////////////////////////////////////
	while (1)
	{ // MAIN() program while loop
		MAIN_WhileLoop_XT();
	} // end MAIN() while (1)
	  //////////////////////////////////////////////////////////////////////////////

} // end main