#! /usr/bin/env python
import serial
import sys
import time
import datetime
import re

# Joakim Olsson (joakim.olsson@cern.ch)
# Created 2015-10-12

#####
# NOTE!! the program can only control the MuonWall position when the *red switch* is down on the Arduino 
#####

# This script is executed remotely
def main(argv):
    if argv[1] == '-z':
        move_muon_wall(argv[2], sMode='number')
    else:
        move_muon_wall(argv[1])


# Define commands understood by the Arduino software (CmdMessenger)
class Cmd:
    iError = 0          # Report errors (only Arduino -> PC)
    iAcknowledge = 1    # Acknowledge that cmd was received (only Arduino -> PC)
    iAreYouReady = 2    # Ask if other side is ready (only PC -> Arduino)
    iPosition = 3       # Report current position (only Arduino -> PC)
    iMoveToPosition = 4 # Request move to new position (only PC -> Arduino)
    iMotorStop = 5      # Request motor stop (only PC -> Arduino)
    iMotorUp = 6        # Request motor move up (only PC -> Arduino)
    iMotorDown = 7      # Request motor move down (only PC -> Arduino)
    iConfigure = 8      # configure limits (bi-directional)


# Communicates with the Arduino
class ArduinoControl:

    ser = None      # Serial port

    #Calibration offset between the true value and that returned by the arduino
    rCal = 0.06
    rCalSend = 1-rCal
    rCalGet = 1+rCal


    # Note that the baud rate must be set to the same value for the PC and Arduino
    def __init__(self, sPort, iBaudRate = 115200, rTimeout = 1):
        self.sPort = sPort
        self.iBaudRate = iBaudRate
        self.rTimeout = rTimeout
        from subprocess import Popen, PIPE
        Popen('stty -F /dev/ttyACM0 cs8 115200 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts', stdin=PIPE, stdout=PIPE, shell=True)

    def open_serial_port(self):
        self.ser = serial.Serial(self.sPort, self.iBaudRate, timeout=self.rTimeout)
        time.sleep(self.rTimeout)
        if not self.ser.isOpen():
            print 'muon_wall_controller.py: ArduinoControl.open_serial_port()'
            print 'Unable to connect to the Arduino, please check \'sPort\''
            print 'sPort =', sPort
            print 'Serial port status:', self.ser, '\n'

    def read_all_lines(self):
        read_all_lines_str = ''
        for line in self.ser.readlines():
            read_all_lines_str += line + '\n'
        return read_all_lines_str

    def read_line(self):
        #return self.ser.read()
        return self.ser.readline()

    def send_command(self, cmd_list):
        cmd_format = ','.join(['%d']*len(cmd_list))
        cmd = cmd_format % tuple (cmd_list)
        cmd += ';' # commands must end with semicolon
        #print 'muon_wall_controller.py: ArduinoControl.send_command(): \''+cmd+'\''
        self.ser.write(cmd)

    def are_you_ready(self):
        self.send_command([Cmd.iAreYouReady])
        return self.read_all_lines()

    def move_to_pos(self, pos):
        pos = int(self.rCalSend * pos)
        self.send_command([Cmd.iMoveToPosition, pos])
        time.sleep(self.rTimeout)

    def get_pos(self):
        self.send_command([Cmd.iAreYouReady])
        rTimeOut = time.time() + 1 # break while loop after 1 second
        sPos = None
        while True:
            #print 'In while...'
            sReadOut = self.read_line()
            #print sReadOut
            if re.search('^3,', sReadOut):
                sPos = re.search('(?<=3,)\d+', sReadOut).group()
                #break
            if time.time() > rTimeOut:
                if sPos is None:
                    print 'ERROR: get_pos() timeout'
                    sPos='0'
                break
        return str(int(int(sPos) * self.rCalGet))

    def at_pos(self, iNewPos, iError = 3):
        rTimeOut = time.time() + 60*5 # break while loop after 5 min
        while True:
            sReadOut = self.read_line()
            if re.search('^3,', sReadOut):
                iCurrentPos = int(re.search('(?<=3,)\d+', sReadOut).group())
                iCurrentPos = int(self.rCalGet * iCurrentPos)
                #print iNewPos,iCurrentPos
                if (abs(iNewPos - iCurrentPos) < iError):
                    time.sleep(3) # wait a few extra seconds, just in case
                    return True
            if time.time() > rTimeOut:
                print 'ERROR: at_pos() timeout'
                break
        return False

    def close_serial_port(self):
        if self.ser.isOpen():
            self.ser.close()


# Positions the muon wall based on the coordinates of the table and saves meta data to log file
def move_muon_wall(sTableSetup, sMode='predefined'):
    '''Moves the wall to a precalculated position based on the predefined table setup
    sMode can be predefined or number
    '''

    sPath = '/home/table/TileMoveTable/logBookMuonWall.txt'
    with open(sPath, 'a') as f:

        # Setup arduino
        sPort = '/dev/ttyACM0' # Hardcoded (For more info: http://playground.arduino.cc/Interfacing/LinuxTTY)
        iBaudRate = 115200 # bits (the iBaudRate must be the same value as for the Arduino)
        rTimeout = 1 # seconds (a time out is needed for the Arduino to have time to resond)
        oArduino = ArduinoControl(sPort, iBaudRate, rTimeout)
        #print 'Opening serial port...'
        try:
            oArduino.open_serial_port()
        except OSError:
            print '---> Do:'
            print 'sudo chmod 777 /dev/ttyACM0'
            exit()
        #print 'Serial port open'
        # Write start position to log file
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        # Get current position from the Arduino
        #print 'Getting current position from Arduino...'
        sCurrentPos = oArduino.get_pos()
        if (sCurrentPos == None):
            print 'ERROR Unable to obtain position from Arduino'
            exit()
        print '\nBefore moving:'
        print 'sCurrentPos:', sCurrentPos

        # Get the coordinates of the table
        if sMode=='predefined':
            from calculate_uwall_position import get_muon_position
            iNewPos = get_muon_position(sTableSetup)
            sSetupLog = sTableSetup
        elif sMode=='number':
            iNewPos=int(sTableSetup)
	    if (iNewPos > 400 or iNewPos < 0):
		print 'The z-coordinate needs to be an integer between 0 and 400'
		exit()
            sSetupLog = 'z={0}'.format(sTableSetup)

        sNewPos = str(iNewPos)
        print 'sNewPos:', sNewPos

        # Log the start of movement, current and target position
        sLogStart = '{0}  Start  {1}  {2}  Moving to  {3}\n'.format(st, sSetupLog, sCurrentPos, sNewPos)

        if (isinstance(iNewPos, (int, long)) and should_move(iNewPos, int(sCurrentPos))):

            # Tell Arduino to move the muon wall to new position
            oArduino.move_to_pos(iNewPos)

            # Wait until the Muon Wall has stopped moving, then get its position
            bSuccessBeforeTimeout = oArduino.at_pos(iNewPos)
            sCurrentPos = oArduino.get_pos()
            iCurrentPos = int(sCurrentPos)
            sDeviation = str(iNewPos-iCurrentPos)

            print '\nAfter moving:'
            print 'sNewPos', sNewPos
            print 'sCurrentPos', sCurrentPos
            print 'sDeviation', sDeviation
            print 'bSuccessBeforeTimeout', bSuccessBeforeTimeout

        else:

            print '\nDo not move to new position:'
            print 'sNewPos', sNewPos
            print 'sCurrentPos', sCurrentPos
	    sDeviation = 'None'

        # Log the new position and the deviation from the target position
        sLogStop = '{0}  Stop  {1}  {2}  Deviation is  {3}\n'.format(st, sSetupLog, sCurrentPos, sDeviation)
        f.write(sLogStart)
        f.write(sLogStop)

def should_move(iNewPos, iCurrentPos, iError=5):
	# do not move if already close to the physical boundary
	if (iCurrentPos < 0 + iError):
		return  False
	if (iCurrentPos > 400 - iError):
		return  False
	# do not move if already close to the new position
	if (abs(iNewPos-iCurrentPos) < iError):
		return False
	# otherwise, good to go
	return True

if __name__ == '__main__':
    main(sys.argv)
