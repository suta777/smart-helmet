import cv2

async def w_p(yolo_image,frame):

    piv =0
    y, x = frame.shape[0], frame.shape[1]
    #cv2.rectangle(frame, (2 * x // 5, y//3), (3 * x // 5, y), (255, 255, 255, 255), 2)  # 디택할 영상에 사각형 그리기
    for result in yolo_image:
        boxes = result.boxes.cpu().numpy()
        for box in boxes:  # 객체 하나하나에 접근
            if result.names[int(box.cls[0])] == 'Pedestrian_Pedestrian':  # 만약에 사람이라면
                r = box.xyxy[0].astype(int)
                if (2 * x // 5 <= r[0] <= 3 * x // 5) and (2 * x // 5 <= r[2] <= 3 * x // 5) and y//3<r[1]:
                    cv2.rectangle(frame, r[:2], r[2:], (0, 0, 255, 255), 2)  # 사람 빨강색 그리기
                    piv = 1
                else:
                    cv2.rectangle(frame, r[:2], r[2:], (255, 255, 255, 255), 2)  # 사람 하얀색 그리기
            else:
                r = box.xyxy[0].astype(int)
                cv2.rectangle(frame, r[:2], r[2:], (255, 255, 255, 255), 2)  # 다른것도 하얀색 그리기
    return piv, frame