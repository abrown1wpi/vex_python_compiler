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
ALIGN = 4
RETURNINGHOME = 5
DISPENSING = 6

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
                dir = abs(error)/error * 100
                move.drive(0, -dir, 0, min(error + 15, 50))
            else:
                if (pickingRot == 180):
                    move.rotateToHeading(90)
                    currentState = ALIGN
                elif (pickingRot == 0 or pickingRot == 360):
                    move.rotateToHeading(-90)
                    currentState = ALIGN
                elif (pickingRot == 90):
                    move.rotateToHeading(180)
                    currentState = ALIGN
                elif (pickingRot == 270):
                    currentState = ALIGN
    
    if (currentState == ALIGN):
        if (pickingRot == 180):
            move.alignToLine(-1)
            currentState = RETURNINGHOME
        elif (pickingRot == 0 or pickingRot == 360):
            move.alignToLine(1)
            currentState = RETURNINGHOME
        elif (pickingRot == 90):
            rotError = (270 - devices.getHeading() + 180) % 360 - 180
            curDist = 30
            if devices.ultrasonic_back is not None:
                curDist = devices.ultrasonic_back.distance(MM)
            error = (curDist - 30)/2
            move.drive(-100 + min(rotError * 2 + 5, 25) + error, -error, min(rotError * 2, 25), 35)
            if (devices.isBothPos):
                currentState = RETURNINGHOME
        elif (pickingRot == 270):
            currentState = DISPENSING
    
    if (currentState == RETURNINGHOME):
        move.followLine(1, 270)
    
            