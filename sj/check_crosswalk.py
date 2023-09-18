import cv2

async def Are_there_Crosswalk(results,frame):

    piv = 0
    y, x = frame.shape[0], frame.shape[1]
    for result in results:
        boxes = result.boxes.cpu().numpy()
        for box in boxes:  # 객체 하나하나에 접근
            if result.names[int(box.cls[0])] == 'RoadMark_Crosswalk':  # 만약에 초록불이라면
                r = box.xyxy[0].astype(int)  # 그 디택한 신호등의 사각형 위치
                mid_x, mid_y = (r[0]+r[2])//2 , (r[1]+r[3])//2
                #cv2.rectangle(frame, r[:2], r[2:], (0, 0, 255, 255), 2)  # 그리기
                #cv2.putText(frame, "Crosswalk", (200, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)
                if 2 * x // 7 < mid_x <  5 * x // 7 and y // 3 <mid_y <  y:
                    piv = 1

    return piv , frame
