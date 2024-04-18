import cv2
import numpy as np

def morph(red_mask):
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(red_mask,cv2.MORPH_OPEN,kernel)
    dilation = cv2.dilate(opening,kernel,iterations = 2)

    # cv2.imshow('dilation', dilation)

    return dilation

def main(img):
    try:
        src = img
        hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HLS)

        lower_red = np.array([40, 70, 30])          ##
        upper_red = np.array([150, 150, 150])       ##
        # lower_red = np.array([69, 65, 34])          ##
        # upper_red = np.array([34, 129, 111])       ##


        red_mask = cv2.inRange(hsv, lower_red, upper_red)

        red_mask = morph(red_mask)

        cv2.imshow("111",red_mask)
        cv2.waitKey(1)

        circles = cv2.HoughCircles(red_mask, cv2.HOUGH_GRADIENT, 1, 100, param1 = 250, param2 = 10, minRadius = 20, maxRadius = 70)

        count = 0
        for circle in circles[0]:
            # circle[0] = center_x, circle[1] = center_y, circle[2] = r
            cv2.circle(src, (int(circle[0]), int(circle[1])), int(circle[2]), (0, 255, 255), 5)
            desired_goal= [int(circle[0]), int(circle[1])]
            count += 1
        goal_img = src

    except:
        desired_goal, goal_img, count = (0,0),img,0

    return desired_goal, goal_img, count