from vex import *
from math import sin, cos


class Devices:
    heading : int
    controller : Controller
    
    front_left : Motor
    front_right : Motor
    back_left : Motor
    back_right : Motor
    claw : Motor
    arm : Motor
    inertial : Inertial
    camera : AiVision
    
    ultrasonic = None
    line_sensor_r = None
    line_sensor_l = None

    brain : Brain
    
    def __init__(self, inert = Ports.PORT17, fl=Ports.PORT14, fr=Ports.PORT18, bl=Ports.PORT12, br=Ports.PORT19, c=Ports.PORT20, a=Ports.PORT2, ultra=None, line_r=None, line_l=None, brain=Brain(), controller=Controller()):
        self.front_left = Motor(fl, GearSetting.RATIO_18_1, False)
        self.front_right = Motor(fr, GearSetting.RATIO_18_1, True)
        self.back_left = Motor(bl, GearSetting.RATIO_18_1, False)
        self.back_right = Motor(br, GearSetting.RATIO_18_1, True)
        self.claw = Motor(c, GearSetting.RATIO_36_1, False)
        self.arm = Motor(a, GearSetting.RATIO_36_1, False)
        self.inertial = Inertial(inert)
        
        self.controller = controller
        
        if ultra is not None:
            self.ultrasonic = Distance(ultra)
        if line_r is not None:
            self.line_sensor_r = Line(line_r)
        if line_l is not None:
            self.line_sensor_l = Line(line_l)
        if inert is not None:
            self.inertial = Inertial(inert)
            
        self.brain = brain
        
    def initCamera(self, color1, color2, color3, cam = Ports.PORT10):
        self.camera = AiVision(cam, color1, color2, color3)
    
    def getHeading(self):
        if self.inertial is not None:
            return self.inertial.heading()
        return 0
        
        

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