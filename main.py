import os
import random
import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'  # 라이브러리 충돌 방지

video_path = os.path.join('videos_in', 'cctv3.mp4')
video_out_path = os.path.join('videos_out', 'cctv_out.mp4')

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()

# 영상 저장하기
"""
cv2.VideoWriter_fourcc(*'MP4V'): mpeg-4 코덱(압축방식)
cap.get(cv2.CAP_PROP_FPS): 오리지널 비디오의 fps
"""
cap_out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(
    *'MP4V'), cap.get(cv2.CAP_PROP_FPS), (frame.shape[1], frame.shape[0]))

model = YOLO("yolov8n.pt")

tracker = DeepSort(max_age=3)

# 박스 색상 10개
colors = [(random.randint(0, 255), random.randint(0, 255),
           random.randint(0, 255)) for j in range(10)]

# 스코어 임계값
detection_threshold = 0.5

rows, cols, _ = frame.shape

while ret:

    ret, frame = cap.read()
    results = model(frame)

    # 프레임마다 모델이 읽어오는 정보 사용하기 위해서 언랩
    for result in results:
        detections = []
        for r in result.boxes.data.tolist():  # 박스에 대한 정보, 텐서가 아니라 리스트로 사용하기
            x1, y1, x2, y2, score, class_id = r  # coco데이터셋의 class_id
            w = x2-x1
            h = y2-y1
            class_id = int(class_id)
            if score > detection_threshold:  # 스코어가 0.5 이상인 객체만 딥소트 적용
                detections.append([[x1, y1, w, h], score, class_id])

        tracks = tracker.update_tracks(detections, frame=frame)  # 딥소트 알고리즘 적용

        for track in tracks:
            if not track.is_confirmed():  # 트래킹할 오브젝트가 없어도 계속 진행
                continue

            track_id = track.track_id  # 딥소트 알고리즘이 적용된 오브젝트의 아이디
            ltrb = track.to_ltrb()  # left-top, right-bottom

            color = colors[int(track_id) % len(colors)]

            # x1,y1,x2,y2
            cv2.rectangle(frame, (int(ltrb[0]), int(ltrb[1])), (int(
                ltrb[2]), int(ltrb[3])), color, 3)

            cv2.putText(frame, str(track_id), (
                int(ltrb[0]), int(ltrb[1])-5), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    frame = cv2.resize(frame, (384, 384))
    # cap_out.write(frame)  # 녹화
    cv2.imshow('video', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cap_out.release()
cv2.destroyAllWindows()
