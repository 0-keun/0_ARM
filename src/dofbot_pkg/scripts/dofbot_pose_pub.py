from dofbot_DH import DOFBOT

dofbot = DOFBOT()

for i in range(80):
    end_x = 0.04
    end_y = (0.1549/100)*(10+i)

    end = [end_x,end_y]

    theta_2, theta_3 = dofbot.inverse_kinematics_arm(end)
    theta = [0,theta_2, theta_3, -(theta_2+theta_3), 0]