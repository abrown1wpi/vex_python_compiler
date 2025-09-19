from vex import *

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
        
        