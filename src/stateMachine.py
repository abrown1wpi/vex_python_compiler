class driveState():
    IDLE = 0
    DRIVE = 1
    LINNUP = 2
    AUTONOMOUS = 3
    SEARCHING = 4
    
class clawState():
    OPEN = 0
    CLOSED = 1
    HOLDING = 2
    
class armState():
    LEVEL1 = 1
    LEVEL2 = 2
    LEVEL3 = 3
    LEVEL4 = 4
    LEVEL5 = 5
    LEVEL6 = 6
    LEVEL7 = 7
    OPERATED = 0
    AUTONOMOUS = 9
    
class stateMachine():
    arm : armState
    claw : clawState
    drive : driveState
    
    def __init__(self, drive=driveState.IDLE, claw=clawState.CLOSED, arm=armState.OPERATED):
        arm = arm
        claw = claw
        drive = drive
    
    def setDriveState(self, drive):
        drive = drive
    
    def setClawState(self, claw):
        claw = claw
    
    def setArmState(self, arm):
        arm = arm

    def getDriveState(self):
        return self.drive
    
    def getClawState(self):
        return self.claw
    
    def getArmState(self):
        return self.arm