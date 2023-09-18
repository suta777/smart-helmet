import cv2
import os
import time
#from function_py import play_sound as ps

async def calculate_overlap_percentage(results, frame):
    y, x = frame.shape[0], frame.shape[1]
    box1 = [x // 3, y//3, (x // 3)*2, y]
    #cv2.rectangle(frame, (box1[0], box1[1]), (box1[2], box1[3]), (0, 255, 0), 2)

    target = []
    target_name = []
    overlap_percentage = []
    target.clear()
    target_name.clear()
    overlap_percentage.clear()

    for result in results:
        boxes = result.boxes.cpu().numpy()
        for box in boxes:  # 객체 하나하나에 접근
            if result.names[int(box.cls[0])] != 'TrafficLight_Red' and result.names[int(box.cls[0])] != 'TrafficLight_Yellow' and result.names[int(box.cls[0])] != 'TrafficLight_Green' and result.names[int(box.cls[0])] != 'RoadMark_StopLine'and result.names[int(box.cls[0])] != 'RoadMark_Crosswalk':
                target_name.append(result.names[int(box.cls[0])])
                target.append(box.xyxy[0])
    
    for box2 in target:
        x_overlap = max(0, min(box1[2], box2[2]) - max(box1[0], box2[0]))# 겹치는 영역 좌표 계산
        y_overlap = max(0, min(box1[3], box2[3]) - max(box1[1], box2[1]))
        overlap_area = x_overlap * y_overlap
        box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])# 박스1과 겹치는 전체 영역 계산
        overlap_percentage.append((overlap_area / box1_area) * 100)# 겹치는 영역의 크기를 백분율로 계산

    start_time = time.time()
    frame_time = start_time + 0

    green = 30 #10%이상 탐지
    yellow = 40 #20%이상 탐지
    red = 50 #30%이상 탐지
    
    #player_noti = None
    #video_path = ''

    if len(overlap_percentage) != 0: #값이 없을 때 제외
        for temp in overlap_percentage:
            current_time = time.time()
            if current_time >= frame_time:
                #ps.pause(mv.player)
                if temp<green:
                    return "",frame
                if green <= temp and yellow > temp:
                    # print("Green Warning")
                    # print("   name    : ", target_name)
                    # print("percentage : ", overlap_percentage)
                    # print("===============================")
                    return "green", frame
                elif yellow <= temp and red > temp:
                    # print("Yellow Warning")
                    # print("   name    : ", target_name)
                    # print("percentage : ", overlap_percentage)
                    # print("===============================")
                    #cv2.rectangle(frame, (box1[0], box1[1]), (box1[2], box1[3]), (0, 255, 255), 2)
                    return "yellow", frame
                elif red <= temp:
                    # print("Red Warning")
                    # print("   name    : ", target_name)
                    # print("percentage : ", overlap_percentage)
                    # print("===============================")
                    #cv2.rectangle(frame, (box1[0], box1[1]), (box1[2], box1[3]), (0, 0, 255), 2)
                    return "red", frame
                #ps.play_sound_notification(player_noti, video_path)
                #ps.resume(mv.player, player_noti, video_path)
    else:
        return "" ,frame