from vex import *
from devices import Devices
from math import sin, cos

class Drive:
    devices : Devices 
    max_speed : int
    clawState = False
    
    def __init__(self, paraDev : Devices, max_speed: int = 50):
        self.devices = paraDev
        self.max_speed = max_speed
        
    def stopDrive(self):
        self.devices.front_left.stop()
        self.devices.front_right.stop()
        self.devices.back_left.stop()
        self.devices.back_right.stop()
        
    def setMaxSpeed(self, speed : int):
        self.max_speed = speed
    
    def drive(self, x, y, rot, speed : int = 100, heading=None, field_oriented=None):        
        x = self.squareProportional(x)
        y = self.squareProportional(y)
        rot = self.squareProportional(rot)
        
        if field_oriented and heading is not None and self.devices.inertial is not None:
            angle_rad = (heading - self.devices.inertial.heading()) * (3.14159 / 180)
            temp = y * cos(angle_rad) + x * sin(angle_rad)
            x = -y * sin(angle_rad) + x * cos(angle_rad)
            y = temp
        
        tl = (-y - x - rot)
        tr = (-y + x + rot)
        bl = (-y + x - rot)
        br = (-y - x + rot)
    
        self.devices.front_left.spin(self.backAndForth(tl), abs(tl)*speed/100, PERCENT)
        self.devices.front_right.spin(self.backAndForth(tr), abs(tr)*speed/100, PERCENT)
        self.devices.back_left.spin(self.backAndForth(bl), abs(bl)*speed/100, PERCENT)
        self.devices.back_right.spin(self.backAndForth(br), abs(br)*speed/100, PERCENT)
        
    def backAndForth(self, val):
        if val > 0:
            return REVERSE
        return FORWARD

    def moveArm(self, direction : DirectionType.DirectionType, speed : int = 50):
        self.devices.arm.spin(direction, speed, PERCENT)
        
    def switchClaw(self, clawState : bool):
        if clawState:
            self.devices.claw.spin(FORWARD, 50, PERCENT)
        else:
            self.devices.claw.spin(REVERSE, 50, PERCENT)
        
    def squareProportional(self, val : int):
        retVal = (val * abs(val)) / 100
        return retVal * self.max_speed / 100
    
    def manualDrive(self, yWasPressed):
        self.drive(self.devices.controller.axis4.position(), self.devices.controller.axis3.position(), self.devices.controller.axis1.position(), speed=75)
        if(self.devices.controller.buttonR1.pressing()):
            self.moveArm(DirectionType.FORWARD, 75)
        elif self.devices.controller.buttonR2.pressing():
            self.moveArm(DirectionType.REVERSE, 75)
        else:
            self.moveArm(DirectionType.FORWARD, 0)
        if (self.devices.controller.buttonY.pressing() and not yWasPressed):
            yWasPressed = True
            self.clawState = not self.clawState
            self.switchClaw(self.clawState)
        else:
            if not self.devices.controller.buttonY.pressing():
                yWasPressed = False
        if (not self.devices.controller.buttonY.pressing):
            return False
        
        