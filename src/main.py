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
RETURNING = 3
DISPENSING = 4

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
print(devices.line_sensor_l)
print(devices.line_sensor_r)            
while True:

    if(devices.line_sensor_l is not None and devices.line_sensor_r is not None):
        print(str(devices.line_sensor_l.reflectivity()) + " " + str(devices.line_sensor_r.reflectivity()))
    if (currentState == RETURNING):
        roundHeading = round(devices.getHeading()/90) * 90 