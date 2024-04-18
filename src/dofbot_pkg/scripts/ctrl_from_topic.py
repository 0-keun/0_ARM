# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import JointState
from ctrl_from_angle import default_mode, move_to

default_mode()

class Ctrl_Arm_By_Topic():
    def __init__(self):
        rospy.init_node('ctrl_arm_by_topic', anonymous=True)

        ### sub ###
        rospy.Subscriber('/joint_states', JointState, self.jointstate_callback)

        #############
        self.init_callback_time = rospy.get_time()
        self.last_callback_time = rospy.get_time()  
        self.callback_interval = 5  # [s]

        self.joints = [0,0,0,0,0]
        self.prev_data = [0,0,0,0,0]

    def jointstate_callback(self, data):
        if self.prev_data != data.position:
            self.prev_data = data.position
            self.joints = list(data.position)
            self.joints.append(0)
            print("joints: ", self.joints)

            if self.last_callback_time - rospy.get_time() < self.callback_interval:
                move_to(self.joints) # default s_time is 500
                self.last_callback_time = rospy.get_time()

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        cabt = Ctrl_Arm_By_Topic()
        cabt.run()
    except rospy.ROSInterruptException:
        pass
