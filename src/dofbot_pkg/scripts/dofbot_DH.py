from DH import ROBOT_DH
from math import pi
from math import cos, sin, atan2
from dofbot_kinematics import _2DOF_inverse_kinematics

class DOFBOT(ROBOT_DH):
    def __init__(self):
        joint_count = 5
        super().__init__(joint_count)

        self.DHparams[0] = [0,0.08,0.08,0.08,0]
        self.DHparams[1] = [pi/2,0,0,0,pi/2]
        self.DHparams[2] = [0.12,0,0,0,0.05]

    def estimate_endpose(self, theta):
        self.DHparams[3] = theta
        self.DHparams[3,2] += pi/2 # dofbot 좌표 변환

        T = self.get_0_T_n()

        (x,y,z) = (T[0,3],T[1,3],T[2,3])

        return x, y, z
    
    def arm_inverse_kinematics(self,xz_plane):
        # each theta are based on each link's coordinate
        theta_2, theta_3 = _2DOF_inverse_kinematics(xz_plane[0],xz_plane[1],self.DHparams[0,1],self.DHparams[0,2])
        theta_2 = theta_2-pi/2
        if theta_2+theta_3 > 0:
            theta_4 = (pi/2)-(theta_2+theta_3) # phi = 0 case
        else:
            theta_4 = -(pi/2)-(theta_2+theta_3)
    
        return theta_2,theta_3,theta_4

    def calculate_desired_joints_closed(self,end):
        theta_2,theta_3,theta_4 = self.arm_inverse_kinematics(end)
        theta_1,theta_5,theta_6 = 1.57, 0, 1.57
        theta = [theta_1,theta_2,theta_3,theta_4,theta_5,theta_6]
        
        return theta

    def calculate_desired_joints(self,end,theta_1=1.57,theta_5=0,theta_6=0):
        theta_2,theta_3,theta_4 = self.arm_inverse_kinematics(end)

        theta = [theta_1,theta_2,theta_3,theta_4,theta_5,theta_6]
        
        return theta

'''                   
dofbot = DOFBOT()

for i in range(80):
    end_x = 0.14
    end_y = (0.0774/100)*(10+i)

    end = [end_x,end_y]

    theta = dofbot.calculate_desired_joints(end)

    # x,y,z = dofbot.estimate_endpose(theta)
    # print("(x, y, z)")
    # print(x, "\t", y, "\t", z )
    theta = [int(theta[i] * (180/3.141592)) for i in range(len(theta))]
    # # joint_angles_deg = [int(theta[i] * (180/3.141592) + 90) for i in range(len(theta))]
    # # print("theta_2, theta_3")
    print(theta)
    # print(joint_angles_deg)

for i in range(80):
    end_x = 0.14
    end_y = (0.0774/100)*(90-i)

    end = [end_x,end_y]

    theta = dofbot.calculate_desired_joints(end)

    x,y,z = dofbot.estimate_endpose(theta)
    # print("(x, y, z)")
    # print(x, "\t", y, "\t", z )
    theta = [int(theta[i] * (180/3.141592)) for i in range(len(theta))]
    # joint_angles_deg = [int(theta[i] * (180/3.141592) + 90) for i in range(len(theta))]
    # print("theta_2, theta_3")
    print(theta)
    # print(joint_angles_deg)
'''
