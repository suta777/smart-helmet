'''
    딥소트 적용 파일
'''

import os
import random
import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort
colors = [(random.randint(0, 255), random.randint(0, 255),
           random.randint(0, 255)) for j in range(10)]


def deepsort_start(yolo_frame, frame):

    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'  # 라이브러리 충돌 방지

    tracker = DeepSort(max_age=3)

    # 박스 색상 10개

    # 스코어 임계값
    detection_threshold = 0.5

    results = yolo_frame

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

        tracks = tracker.update_tracks(
            detections, frame=frame)  # 딥소트 알고리즘 적용
        for track in tracks:
            # if not track.is_confirmed():
            #     continue
            # print('asdfasdfsadasdf')

            track_id = track.track_id  # 딥소트 알고리즘이 적용된 오브젝트의 아이디
            ltrb = track.to_ltrb()  # left-top, right-bottom

            color = colors[int(track_id) % len(colors)]

            # x1,y1,x2,y2
            cv2.rectangle(frame, (int(ltrb[0]), int(ltrb[1])), (int(
                ltrb[2]), int(ltrb[3])), color, 3)

            cv2.putText(frame, str(track_id), (
                int(ltrb[0]), int(ltrb[1])-5), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    return frame
