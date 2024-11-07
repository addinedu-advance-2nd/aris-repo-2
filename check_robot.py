from xarm.wrapper import XArmAPI
import time
arm = XArmAPI('192.168.1.167')
arm.connect('connect!')
pos = arm.get_position()
p0 = arm.get_servo_angle()
p1 = arm.get_version()
p2 = arm.get_state()
print('pos =', pos)
print('angle =', p0)
print('version =', p1)
print('state =', p2)
