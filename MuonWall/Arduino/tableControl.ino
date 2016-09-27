// *** Muon Wall Controler ***

// Lukas Fiala
// Institute of Physics
// fialal@fzu.cz

#include <EEPROMex.h>
#include <CmdMessenger.h>  // CmdMessenger

struct ConfigurationStruct {
  char control[4];
  short downLimit;
  short upLimit;
};
#define CONFIGCONTROL "ls1"

// Global variables
const byte INTERNALLEDPIN             = 13;  // Pin of internal Led
const byte MOTORDOWNPIN               = 7;   // Pin of the motor control - downwards
const byte MOTORUPPIN                 = 8;   // Pin of the motor control - upwards
const byte POSITIONPIN                = 0;   // Pin of the position analog sensor
const short DEFAULTPOSITIONDOWNLIMIT  = 0;   // Defualt low limit of the position sensor
const short DEFAULTPOSITIONUPLIMIT    = 400; // Default high limit of the position sensor

int     mConfigAddress             = 0;     // EEPROM address of the configuration block
boolean mIsRequestedPositionNew    = false; // Indicates if user request new position
short   mRequestedPosition         = -1;    // Value indicating requested position
short   mActualPosition            = -1;    // Value indicating current position
boolean mIsMotorMoveDownInternal   = false;
boolean mIsMotorMoveUpInternal     = false;
short   mPositionDownLimit;
short   mPositionUpLimit;

// Attach a new CmdMessenger object to the default Serial port
CmdMessenger cmdMessenger = CmdMessenger(Serial);

// List of the the recognized commands. These can be either sent or received.
// In order to receive, attach a callback function to these events
enum {
  kError,                 // Command to report errors
  kAcknowledge,           // Command to acknowledge that cmd was received
  kAreYouReady,           // Command to ask if other side is ready
  kPosition,              // Command to report current position
  kMoveToPosition,        // Command to request move to new position
  kMotorStop,             // Command to request stop
  kMotorUp,               // Command to request move up
  kMotorDown,             // Command to request move down
  kConfigure,             // Command to configure move limits
};

// Callbacks define on which received commands we take action
void attachCommandCallbacks() {
  cmdMessenger.attach(OnUnknownCommand);
  cmdMessenger.attach(kAreYouReady, OnAreYouReady);
  cmdMessenger.attach(kMoveToPosition, OnMoveToPosition);
  cmdMessenger.attach(kMotorStop, OnMotorStop);
  cmdMessenger.attach(kMotorUp, OnMotorUp);
  cmdMessenger.attach(kMotorDown, OnMotorDown);
  cmdMessenger.attach(kConfigure, OnConfigure);
}

// Called when a received command has no attached function
void OnUnknownCommand() {
  cmdMessenger.sendCmd(kError, "cmdUnknown");
}

// Callback function that response to the AreYouReady request
void OnAreYouReady() {
  cmdMessenger.sendCmd(kAcknowledge, "sysReady");
  cmdMessenger.sendCmdStart(kConfigure);
  cmdMessenger.sendCmdArg(mPositionDownLimit);
  cmdMessenger.sendCmdArg(mPositionUpLimit);
  cmdMessenger.sendCmdEnd();
  mActualPosition = getCurrentPosition();
  cmdMessenger.sendCmd(kPosition, mActualPosition);
  if (mIsMotorMoveDownInternal) cmdMessenger.sendCmd(kAcknowledge, "motDown");
  else if  (mIsMotorMoveUpInternal) cmdMessenger.sendCmd(kAcknowledge, "motUp");
  else cmdMessenger.sendCmd(kAcknowledge, "motIdle");
}

// Callback function that sets variables to move table to the specified position
void OnMoveToPosition() {
  //read requested position
  short requestedPosition = cmdMessenger.readInt16Arg();
  // validate requested position
  if (requestedPosition < mPositionDownLimit) {
    cmdMessenger.sendCmd(kError, "posToLow");
    return;
  }
  if (requestedPosition > mPositionUpLimit) {
    cmdMessenger.sendCmd(kError, "posToHigh");
    return;
  }
  // store requested position
  mRequestedPosition = requestedPosition;
  mIsRequestedPositionNew = true;
  // send back acknowledge
  cmdMessenger.sendCmd(kAcknowledge, "cmdSuccess");
}

// Callback function that stop the table
void OnMotorStop() {
  mIsRequestedPositionNew = false;
  // send back acknowledge
  cmdMessenger.sendCmd(kAcknowledge, "cmdSuccess");
}

// Callback function that move the table up
void OnMotorUp() {
  mRequestedPosition = mPositionUpLimit;
  mIsRequestedPositionNew = true;
  // send back acknowledge
  cmdMessenger.sendCmd(kAcknowledge, "cmdSuccess");
}

// Callback function that move the table down
void OnMotorDown() {
  mRequestedPosition = mPositionDownLimit;
  mIsRequestedPositionNew = true;
  // send back acknowledge
  cmdMessenger.sendCmd(kAcknowledge, "cmdSuccess");
}

// Callback function that configure move limits
void OnConfigure() {
  mPositionDownLimit = cmdMessenger.readInt16Arg();
  mPositionUpLimit = cmdMessenger.readInt16Arg();
  ConfigurationStruct configuration = {CONFIGCONTROL, mPositionDownLimit, mPositionUpLimit};
  EEPROM.updateBlock(mConfigAddress, configuration);
  // send back acknowledge
  cmdMessenger.sendCmdStart(kConfigure);
  cmdMessenger.sendCmdArg(mPositionDownLimit);
  cmdMessenger.sendCmdArg(mPositionUpLimit);
  cmdMessenger.sendCmdEnd();
}

// Setup function
void setup() {
  // Listen on serial connection for messages from the PC
  Serial.begin(115200);
  // Adds newline to every command - enabled for debug
  cmdMessenger.printLfCr();

  // Attach my application's user-defined callback methods
  attachCommandCallbacks();

  // set pin for blink LED and engine control pins
  pinMode(INTERNALLEDPIN, OUTPUT);
  pinMode(MOTORDOWNPIN, OUTPUT);
  pinMode(MOTORUPPIN, OUTPUT);

  // set pin for input and enable pull-up resistor
  pinMode(POSITIONPIN, INPUT);
  digitalWrite(POSITIONPIN, HIGH);

  // get the configuration data from the EEPROM
  ConfigurationStruct configuration;
  EEPROM.setMemPool(32,EEPROMSizeUno);
  mConfigAddress = EEPROM.getAddress(sizeof(ConfigurationStruct));
  EEPROM.readBlock(mConfigAddress, configuration);
  if (!strcmp(configuration.control, CONFIGCONTROL)) {
    mPositionDownLimit = configuration.downLimit;
    mPositionUpLimit = configuration.upLimit;
  } else {
    mPositionDownLimit = DEFAULTPOSITIONDOWNLIMIT;
    mPositionUpLimit = DEFAULTPOSITIONUPLIMIT;
  }

  // Send the status to the PC that says the Arduino has booted
  OnAreYouReady();
}

void loop() {
  cmdMessenger.feedinSerialData();
  delay(100);
  motorControl();
}

// Main function to set motor control signals
void motorControl() {
  // get current position
  short currentPosition = getCurrentPosition();

  if (mActualPosition != currentPosition) {
    mActualPosition = currentPosition;
    // send current position to the PC
    cmdMessenger.sendCmd(kPosition, currentPosition);
  }

  // If no new position entered
  if (!mIsRequestedPositionNew) {     // no new requested position, keep motor idle
    motorStop();
  } else {  // new position entered
    if (mIsMotorMoveUpInternal) {     // motor is moving up
      if ((currentPosition >= mRequestedPosition) || (currentPosition >= mPositionUpLimit)) {      // position is equal or higher then requested
        mIsRequestedPositionNew = false; // requested position reached
        motorStop();                     // stop motor movement
      }
    } else if (mIsMotorMoveDownInternal) { // motor is moving down
      if ((currentPosition <= mRequestedPosition) || (currentPosition <= mPositionDownLimit)) {    // position is equal or lower then requested
        mIsRequestedPositionNew = false; // requested position reached
        motorStop();                     // stop motor movement
      }
    } else {                          // motor is not moving
      if ((currentPosition < mRequestedPosition) && (currentPosition < mPositionUpLimit)) {       // current position is lower then requested
        motorUp();
      } else if ((currentPosition > mRequestedPosition) && (currentPosition > mPositionDownLimit)) { // current position is higher then requested
        motorDown();
      } else { // current position is equal to requested
        mIsRequestedPositionNew = false;
      }
    }
  }
}

// get current position transformed to cm
short getCurrentPosition() {
  short internalPosition = analogRead(POSITIONPIN);
  float calculatedPosition = (float)internalPosition / 1023.0 * 500.0;
  return (short)calculatedPosition;
}

// set pins to motor stop
void motorStop() {
  digitalWrite(MOTORDOWNPIN, LOW);
  digitalWrite(MOTORUPPIN, LOW);
  digitalWrite(INTERNALLEDPIN, LOW);
  if (mIsMotorMoveDownInternal || mIsMotorMoveUpInternal) cmdMessenger.sendCmd(kAcknowledge, "motIdle");
  mIsMotorMoveDownInternal = false;
  mIsMotorMoveUpInternal = false;
}

// set pins to motor move up
void motorUp() {
  digitalWrite(MOTORDOWNPIN, LOW);
  digitalWrite(MOTORUPPIN, HIGH);
  digitalWrite(INTERNALLEDPIN, HIGH);
  if (!mIsMotorMoveUpInternal) cmdMessenger.sendCmd(kAcknowledge, "motUp");
  mIsMotorMoveDownInternal = false;
  mIsMotorMoveUpInternal = true;
}

//set pins to motor move down
void motorDown() {
  digitalWrite(MOTORUPPIN, LOW);
  digitalWrite(MOTORDOWNPIN, HIGH);
  digitalWrite(INTERNALLEDPIN, HIGH);
  if (!mIsMotorMoveDownInternal) cmdMessenger.sendCmd(kAcknowledge, "motDown");
  mIsMotorMoveUpInternal = false;
  mIsMotorMoveDownInternal = true;
}
