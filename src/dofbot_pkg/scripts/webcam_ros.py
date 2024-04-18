import cv2
import color_detect
import rospy
from dofbot_pkg.msg import Pix_msg

class color_detector:
    def __init__(self):
        rospy.init_node('color_detect',anonymous=True)

        self.pix_pub = rospy.Publisher("detected_pix",Pix_msg, queue_size=1)
        self.goal_pix = Pix_msg()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("can not open webcam")
            exit()
        self.frame_size = [640,480]
        self.desired_goal = [self.frame_size[0]/2, self.frame_size[1]/2]

    def pix_publish(self):
        self.goal_pix.x = int(self.desired_goal[0])
        self.goal_pix.y = int(self.desired_goal[1])
        self.pix_pub.publish(self.goal_pix)

    def main(self,frame):
        desired_goal, goal_img, count = color_detect.main(frame)
        cv2.imshow('webcam',goal_img) 
        
        if count == 1:
            self.desired_goal = desired_goal
            self.pix_publish()
        else:
            self.desired_goal = [self.frame_size[0]/2, self.frame_size[1]/2]
            self.pix_publish()

    def run(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            self.main(frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break


if __name__ == '__main__':
    try:
        COLOR_DETECTOR = color_detector()
        COLOR_DETECTOR.run()
    except rospy.ROSInterruptException:
        COLOR_DETECTOR.cap.release()
        cv2.destroyAllWindows()
