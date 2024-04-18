#!/usr/bin/env python3
#coding=utf-8

import time
from Arm_Lib import Arm_Device
from dofbot_DH import DOFBOT

Arm = Arm_Device()
time.sleep(.1)

# Control the motion of six steering gears at the same time and gradually change the angle
def ctrl_all_servo(angle, s_time = 500):
    Arm.Arm_serial_servo_write6(angle[0], angle[1], angle[2], angle[3], angle[4], angle[5], s_time)
    time.sleep(s_time/1000)
		
def default_mode():
    ctrl_all_servo([90,90,90,90,90,90])
    time.sleep(1)

'''
!! Warn you !!
-1.57 <  joint_angle_rad  < 1.57
   0  <  joint_angle_deg  < 180
'''
def move_to(joint_angles_rad, s_time = 10):
    joint_angles_deg = [int(joint_angles_rad[i] * (180/3.141592) + 90) for i in range(len(joint_angles_rad))]

    print("desired_angle: ", joint_angles_deg)

    ctrl_all_servo(joint_angles_deg, s_time)

# joint_angles = [0.47, -0.12, -1.33, -0.93, 2.46, 0]

dofbot = DOFBOT()

default_mode()

theta = [-1.57,0,0,0,0,-1.57]
move_to(theta,500)

end = [0.01,0.06]
theta = dofbot.calculate_desired_joints(end,-1.57,0,0)
move_to(theta,1500)

'''
while True:

    for i in range(80):
        end_x = 0.04
        end_y = (0.13/100)*(10+i)

        end = [end_x,end_y]

        theta = dofbot.calculate_desired_joints(end)

        # x,y,z = dofbot.estimate_endpose(theta)
        # print("(x, y, z)")
        # print(x, "\t", y, "\t", z )
        # theta = [int(theta[i] * (180/3.141592)) for i in range(len(theta))]
        # # joint_angles_deg = [int(theta[i] * (180/3.141592) + 90) for i in range(len(theta))]
        # # print("theta_2, theta_3")
        if i == 0:
            move_to(theta,500)
        else:
            move_to(theta)
        # print(joint_angles_deg)
    
    for i in range(80):
        end_x = 0.04
        end_y = (0.13/100)*(90-i)
    
        end = [end_x,end_y]
    
        theta = dofbot.calculate_desired_joints(end)
    
        # x,y,z = dofbot.estimate_endpose(theta)
        # print("(x, y, z)")
        # print(x, "\t", y, "\t", z )
        # theta = [int(theta[i] * (180/3.141592)) for i in range(len(theta))]
        # joint_angles_deg = [int(theta[i] * (180/3.141592) + 90) for i in range(len(theta))]
        # print("theta_2, theta_3")
        if i == 0:
            move_to(theta,500)
        else:
            move_to(theta)
        # print(joint_angles_deg)    
'''
