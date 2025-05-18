from vex import *



brain = Brain()

# The controller
controller = Controller()

# Drive motors
left_drive = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
right_drive = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)

arm_motor = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)

