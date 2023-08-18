import cv2
import numpy as np
import os
from deepsort_module import deepsort_start
from ultralytics import YOLO

video_path = os.path.join('videos_in', 'test_1.mp4')
model_path = os.path.join('models', 'yolov8n.pt')

cap = cv2.VideoCapture(video_path)
model = YOLO(model_path)

while True:
    ret, frame = cap.read()
    yolo_frame = model(frame)

    # 딥소트
    deep_frame = deepsort_start(yolo_frame, frame)

    """
        각자 함수 넣어서 되는지 확인요망
        프레임 리턴 받을시 'frame'이라고 쓰지 않기, 이름 지어주기.
    """

    cv2.imshow('video', deep_frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
