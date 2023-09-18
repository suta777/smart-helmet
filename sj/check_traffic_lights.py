import cv2
async def Are_there_traffic_lights(results,frame):

    piv = 0

    for result in results:
        boxes = result.boxes.cpu().numpy()
        for box in boxes:  # 객체 하나하나에 접근
            #print(result.names[int(box.cls[0])])  # 그 접근한 객체 하나하나의 이름
            if result.names[int(box.cls[0])] == 'TrafficLight_Green':  # 만약에 초록불이라면
                r = box.xyxy[0].astype(int)  # 그 디택한 신호등의 사각형 위치
                cv2.rectangle(frame, r[:2], r[2:], (0, 255, 0, 255), 2)  # 그리기
                cv2.putText(frame, "TrafficLight_Green", (200, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, cv2.LINE_AA)
                piv = 1
            if result.names[int(box.cls[0])] == 'TrafficLight_Red':  # 만약에 빨간불이라면
                r = box.xyxy[0].astype(int)  # 그 디택한 신호등의 사각형 위치
                cv2.putText(frame, "TrafficLight_Red", (200, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.rectangle(frame, r[:2], r[2:], (0, 0, 255, 255), 2)  # 그리기
                piv = 2

    return piv , frame
    