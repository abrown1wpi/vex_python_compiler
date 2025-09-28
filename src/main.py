# Library imports
from vex import *
from devices import Devices
from drive import Drive

# Brain should be defined by default
brain=Brain()
devices = Devices(line_l= brain.three_wire_port.g, line_r=brain.three_wire_port.h, brain=brain)
move = Drive(devices, 100)
controller = Controller()

IDLE = 0
FINDING = 1
PICKING = 2
RETURNINGTOLINE = 3
RETURNINGHOME = 4
DISPENSING = 5

currentState = IDLE

clawtate = False
yWasPressed = False
Geen = Colordesc(1, 77, 239, 118, 15, 0.43)
Pupple = Colordesc(2, 171, 113, 190, 10, 0.2)
Ormans = Colordesc(3, 244, 113, 133, 14, 0.25)

devices.initCamera(Geen, Pupple, Ormans)

devices.inertial.calibrate()

move.switchClaw(True)


while(devices.inertial.is_calibrating()):
    wait(100, MSEC)
    brain.screen.clear_line()
    brain.screen.set_cursor(1,1)
    brain.screen.print("Calibrating")
brain.screen.clear_line()    
devices.inertial.set_heading(0)

aWasPressed = False

while True:
    if(currentState == RETURNINGTOLINE):
        move.drive(0, -100, 0, 20)
        if (devices.isBothPos()):
            currentState = RETURNINGHOME
