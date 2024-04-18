import math
from math import pi
import numpy as np

class ROBOT_DH:
    def __init__(self, count):
        self.joint_count = count             # 5
        self.DHparams = np.zeros((4,count))  #[[a],[alpha],[d],[theta]]
        # np.array([[0,0.08,0.08,0.08,0],[1.57,0,0,0,1.57],[0.12,0,0,0,0.05],[0,0,0,0,0]])
    
    # Homogeneous_Transform based on DH
    def get_Homogeneous_Transform(self,a_i,alpha_i,d_i,theta_i):
        T = np.array([[math.cos(theta_i), -1*math.sin(theta_i)*math.cos(alpha_i),    math.sin(theta_i)*math.sin(alpha_i), a_i*math.cos(theta_i)],
                        [math.sin(theta_i),    math.cos(theta_i)*math.cos(alpha_i), -1*math.cos(theta_i)*math.sin(alpha_i), a_i*math.sin(theta_i)],
                        [0                ,    math.sin(alpha_i)                  ,    math.cos(alpha_i)                  , d_i                  ],
                        [0                ,    0                                  ,    0                                  , 1                    ]])
            
        return T
    
    # Homogeneous_Transform of baselink to endlink
    def get_0_T_n(self):
        for i in range(self.joint_count):
            if i == 0:
                self.T = self.get_Homogeneous_Transform(self.DHparams[0,i],self.DHparams[1,i],self.DHparams[2,i],self.DHparams[3,i])
            else:
                self.T = self.T @ self.get_Homogeneous_Transform(self.DHparams[0,i],self.DHparams[1,i],self.DHparams[2,i],self.DHparams[3,i])
        return self.T
    
    # constant variables
    def set_params(self,a,alpha,d):
        self.DHparams[0] = a
        self.DHparams[1] = alpha
        self.DHparams[2] = d

    # theta is the list of joint angles
    def estimate_endpose(self, theta):
        self.DHparams[3] = theta

        return self.get_0_T_n()



###########################################################################################

# a =     [0,0.08,0.08,0.08,0]
# alpha = [pi/2,0,0,0,pi/2]
# d =     [0.12,0,0,0,0.05]

# theta = [0,-pi/2+(+pi/2),pi/2,pi/2,0]

# dofbot = ROBOT_DH(5)
# dofbot.set_params(a,alpha,d)
# print(dofbot.estimate_endpose(theta))
