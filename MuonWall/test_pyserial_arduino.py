#! /usr/bin/env python
import serial
import time
import sys

# Main script
def main():

    port = '/dev/tty.usbmodem1411'
    baudrate = 115200 # bits (the baudrate must be the same value as for the Arduino)
    timeout = 1 # seconds
    position = 120

    ser = serial.Serial(port, baudrate, timeout=timeout)
    time.sleep(timeout)
    if ser.isOpen():
        print "Port open:", ser

    while True:
        sys.stdout.write(ser.readline())
        sys.stdout.flush()

#    # Print status from Arduino
#    print "--> Initialize Arduino"
#    wait_time = time.time() + 10 # 10 seconds from now
#    while True:
#        #time.sleep(timeout)
#        print ser.readlines()
#        if time.time() > wait_time:
#            break
#
#    print "--> Testing to send a command"
#    ser.write('%d,%d;' % (Cmd.move_to_position, position))
#    #ser.flush()
#    time.sleep(timeout)
#    print ser.readline()
#    time.sleep(timeout)
#    ser.close()
#    print "Done!"

class Cmd:
    error = 0             # Report errors (only Arduino -> PC)
    acknowledge = 1       # Acknowledge that cmd was received (only Arduino -> PC)
    are_you_ready = 2     # Ask if other side is ready (only PC -> Arduino)
    position = 3          # Report current position (only Arduino -> PC)
    move_to_position = 4  # Request move to new position (only PC -> Arduino)
    motor_stop = 5        # Request motor stop (only PC -> Arduino)
    motor_up = 6          # Request motor move up (only PC -> Arduino)
    motor_down = 7        # Request motor move down (only PC -> Arduino)
    configure = 8         # configure limits (bi-directional)

if __name__ == '__main__':
    main()
