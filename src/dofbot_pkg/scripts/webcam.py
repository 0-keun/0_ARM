import cv2
import color_detect
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("can not open webcam")
    exit()

frame_index = 0

while True:
    # 비디오 프레임 캡처
    ret, frame = cap.read()

    # print(np.shape(frame))

    # 프레임 캡처 성공 여부 확인
    if not ret:
        print("can not capture the video")
        break

    # 캡처된 이미지를 창에 표시
    desired_goal, goal_img, count = color_detect.main(frame)
    cv2.imshow('webcam',goal_img) 
    key = cv2.waitKey(1)
    if count == 1:
        print(desired_goal)

    # 'q' 키를 누르면 루프에서 빠져나옵니다
    if key == ord('q'):
        break

# 루프 종료 후, 카메라 장치를 해제
cap.release()

# 모든 OpenCV 창을 파괴
cv2.destroyAllWindows()
