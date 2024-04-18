from math import cos, sin, atan2

def _2DOF_inverse_kinematics(x,y,l_1,l_2):
    # 2DOF Manipulator inverse kinematics
    c_2 = (x**2 + y**2 - l_1**2 - l_2**2) / (2*l_1*l_2)
    s_2 = -1 * (1-c_2**2) ** 0.5 # it can be +/-
    # if s_2 <= 0, it seems like "r"
    # if s_2 >= 0, it seems like "ㄴ"

    theta_2 = atan2(s_2,c_2)
    theta_1 = atan2(y,x)-atan2(l_2*s_2,l_1+l_2*c_2)

    return theta_1, theta_2
