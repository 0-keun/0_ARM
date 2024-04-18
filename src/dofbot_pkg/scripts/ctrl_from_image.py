#!/usr/bin/env python3
#coding=utf-8

import time
from Arm_Lib import Arm_Device
from dofbot_DH import DOFBOT
import rospy
from dofbot_pkg.msg import Pix_msg

Arm = Arm_Device()
time.sleep(.1)

class ctrl_image(DOFBOT):
    def __init__(self):
        rospy.init_node('ctrl_from_image')
        super().__init__()
        self.default_mode()
        self.desired_end = [0.01, 0.10]
        self.ROLL = 0
        theta = self.calculate_desired_joints(self.desired_end,self.ROLL,0,0)
        self.move_to(theta,1500)
        self.interval_time = 0.01 # 100[ms]
        self.last_cb_time = rospy.get_time()
        
        rospy.Subscriber('detected_pix', Pix_msg, self.image_callback)

    def ctrl_all_servo(self, angle, s_time = 500):
        Arm.Arm_serial_servo_write6(angle[0], angle[1], angle[2], angle[3], angle[4], angle[5], s_time)
        time.sleep(s_time/1000)

    def move_to(self, joint_angles_rad, s_time = 10):
        joint_angles_deg = [int(joint_angles_rad[i] * (180/3.141592) + 90) for i in range(len(joint_angles_rad))]
        print("desired_angle: ", joint_angles_deg)
        self.ctrl_all_servo(joint_angles_deg, s_time)

    def default_mode(self):
        self.ctrl_all_servo([90,90,90,90,90,90])
        time.sleep(1)

    def turn_right(self):
        self.ROLL += 0.01
        if self.ROLL >= 1.57:
            self.ROLL = 1.57

    def turn_left(self):
        self.ROLL -= 0.01
        if self.ROLL <= -1.57:
            self.ROLL = -1.57

    def go_up(self):
        print('go up')
        self.desired_end[1] += 0.001
        if self.desired_end[1] >= 0.14:
            self.desired_end[1] = 0.14

    def go_down(self):
        print('go down')
        self.desired_end[1] -= 0.001
        if self.desired_end[1] <= 0.06:
            self.desired_end[1] = 0.06

    def image_callback(self,data):
        current_time = rospy.get_time()
        if current_time - self.last_cb_time > self.interval_time:
            if data.y < 200:
                self.go_up()
            elif data.y > 280:
                self.go_down()

            if data.x < 290:
                self.turn_right()
            elif data.x > 350:    
                self.turn_left()

            print(self.desired_end)
            theta = self.calculate_desired_joints(self.desired_end,self.ROLL,0,0)
            self.move_to(theta,10)
            self.last_cb_time = rospy.get_time()
        
if __name__ == '__main__':
    try:
        CTRL_IMAGE = ctrl_image()
        rospy.spin()
        
    except rospy.ROSInterruptException:
        pass
