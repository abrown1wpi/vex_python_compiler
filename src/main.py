# Library imports
from vex import *
from devices import Devices
from drive import Drive

# Brain should be defined by default
brain=Brain()
devices = Devices(brain=brain)
move = Drive(devices, 100)
controller = Controller()
 
SEARCHING = 0
DRIVE = 1

NOTSTATE = 0
AUTONOMOUS = 1

drivestate = SEARCHING
armstate = NOTSTATE

clawtate = False
yWasPressed = False
Geen = Colordesc(1, 77, 239, 118, 15, 0.43)
Pupple = Colordesc(2, 171, 113, 190, 10, 0.2)
Ormans = Colordesc(3, 244, 113, 133, 14, 0.25)
devices.initCamera(Geen, Pupple, Ormans)


while True:
    # yWasPressed = move.manualDrive(yWasPressed)
    devices.inertial.calibrate()
    if (devices.inertial.is_calibrating):
        while(devices.inertial.is_calibrating):
            wait(100, MSEC)
            brain.screen.clear_line()
            brain.screen.set_cursor(1,1)
            brain.screen.print("Calibrating")
        brain.screen.clear_line()
    devices.inertial.set_heading(0)
            
    
    if (drivestate == SEARCHING):
        brain.screen.clear_line()
        brain.screen.set_cursor(1,1)
        brain.screen.print(devices.getHeading())
        
        if(devices.getHeading() < 85 or devices.getHeading() > 95):
            move.drive(0, 0, -100, 30)
        else:
            move.drive(100, 0, 0, 10)
    
    if (drivestate == DRIVE and armstate is not AUTONOMOUS):
        # Look for biggest fruit
        # Go towards biggest fruit
        # If you loose the fruit go back to searching
        # If at picking parameters, go to claw
        pass
    
    if (drivestate == DRIVE and armstate == AUTONOMOUS):
        # Grab the fruit
        # Pluck the fruit
        # Turn around
        pass
    wait(20, MSEC)
