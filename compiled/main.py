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
        
        self.claw.set_max_torque(15, PERCENT)
        
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
    
    def imageInfo(self, colorTag):
        image = self.camera.take_snapshot(colorTag, 1)
        if image[0].score < 50:
            return None

        return {"width" : image[0].width, "height" : image[0].height, "pos" : {"x" : image[0].centerX, "y" : image[0].centerY}, "id" : image[0].id}
    
    def getLineDif(self):
        if (self.line_sensor_r is not None and self.line_sensor_r is not None):
            pass
        
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
    
    def drive(self, x, y, rot = 0, speed : int = 100):               
        tl = (-y - x - rot)
        tr = (-y + x + rot)
        bl = (-y + x - rot)
        br = (-y - x + rot)
        
        speed = int(speed / self.max_speed)
    
        self.devices.front_left.spin(self.backAndForth(tl), abs(tl)*speed/100, PERCENT)
        self.devices.front_right.spin(self.backAndForth(tr), abs(tr)*speed/100, PERCENT)
        self.devices.back_left.spin(self.backAndForth(bl), abs(bl)*speed/100, PERCENT)
        self.devices.back_right.spin(self.backAndForth(br), abs(br)*speed/100, PERCENT)
        
    def rotateToHeading(self, heading, speed : int = 65):
        goal = self.devices.getHeading() + heading
        while(True):
            rot = (goal - self.devices.getHeading() + 180) % 360 - 180
                
            if abs(rot) < 1.5:
                break
                
            if abs(rot) < 20:
                rot = 40
            
            tl = -rot
            tr = rot
            bl = -rot
            br = rot
                
                # speed = int(speed / self.max_speed)
            
            self.devices.front_left.spin(self.backAndForth(tl), abs(tl)*speed/100, PERCENT)
            self.devices.front_right.spin(self.backAndForth(tr), abs(tr)*speed/100, PERCENT)
            self.devices.back_left.spin(self.backAndForth(bl), abs(bl)*speed/100, PERCENT)
            self.devices.back_right.spin(self.backAndForth(br), abs(br)*speed/100, PERCENT)
        self.stopDrive()
        
        
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
    
    def manualDrive(self, yWasPressed, field_oriented = False, heading = None):
        x = self.squareProportional(self.devices.controller.axis4.value())
        y = self.squareProportional(self.devices.controller.axis3.value())
        rot = self.squareProportional(self.devices.controller.axis1.value())
        
        if field_oriented and heading is not None and self.devices.inertial is not None:
            angle_rad = (heading - self.devices.inertial.heading()) * (3.14159 / 180)
            temp = y * cos(angle_rad) + x * sin(angle_rad)
            x = -y * sin(angle_rad) + x * cos(angle_rad)
            y = temp
        
        tl = (-y - x - rot)
        tr = (-y + x + rot)
        bl = (-y + x - rot)
        br = (-y - x + rot)
        speed = self.max_speed
    
        self.devices.front_left.spin(self.backAndForth(tl), abs(tl)*speed/100, PERCENT)
        self.devices.front_right.spin(self.backAndForth(tr), abs(tr)*speed/100, PERCENT)
        self.devices.back_left.spin(self.backAndForth(bl), abs(bl)*speed/100, PERCENT)
        self.devices.back_right.spin(self.backAndForth(br), abs(br)*speed/100, PERCENT)        
        
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