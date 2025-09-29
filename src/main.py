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
pickingI = 0
pickingRot = None
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
        if pickingI == 0:
            pickingRot = devices.getHeading()
            pickingRot = int(pickingRot/90) * 90
            pickingI = 1
            brain.screen.print(pickingRot)
        
        if (devices.ultrasonic_back is not None):
            if(devices.ultrasonic_back.distance(MM) > 25 and devices.ultrasonic_back.distance(MM) < 35):
                curDist = devices.ultrasonic_back.distance(MM)
                error = curDist - 30
                dir = error/error * 100
                move.drive(0, -dir, min(error + 15, 50))
            else:
                if (pickingRot == 180):
                    move.rotateToHeading(90)
                elif (pickingRot == 0 or pickingRot == 360):
                    move.rotateToHeading(-90)
                elif (pickingRot == 90):
                    move.rotateToHeading(180)
                elif (pickingRot == 270):
                    pass
            