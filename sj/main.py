from module import *
from sound import *
from accident import *
import requests
import mic
import client
from transformers import pipeline
import infer
import audio_predict

# video_path = os.path.join('videos_in', 'human_final.mp4')
model_path = os.path.join('models', 'best_yolo8n.pt')
audio_model_path = os.path.join('models', 'audio.pth')
video_cls = pipeline(model="lake-crimsonn/acc-dri-videomae-base")

# cap = cv2.VideoCapture(video_path)
cap = cv2.VideoCapture(0)

width = int(cap.get(3))
height = int(cap.get(4))
model = YOLO(model_path)
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 코덱 설정

pygame.init()
pygame.mixer.init()

last_road_time = 0
last_road = ''
last_person_time = 0
last_green_time = 0
last_red_time = 0
last_alarm1_time = 0
last_alarm2_time = 0
last_alarm3_time = 0
piv = 1
last = int(1e9)
video_piv = 1
video_start_time = 0

while True:
    ret, frame = cap.read()
    if frame is None:
        continue
    raw_time = time.time()
    current_time = int(raw_time)  # 현재시간
    if video_piv:
        yolo_frame = model(frame, verbose=False)
        # yolo그림 그릴거면
        # frame = yolo_frame[0].plot()

        # 딥소트
        # deep_frame = deepsort_start(yolo_frame, frame)  # yolo, frame

        # 로드워닝
        if current_time - last_road_time > 30:  # 30초에 한번씩 계산
            last_road_time = current_time  # 계산 후엔 시간 초기화
            current_road = asyncio.run(func_road.road(frame))  # 터미널에서 모드확인
            # 모드가 바뀌었을 때 한번만 알림 (ex road > road 알림 x)
            current_road = 'driveway'
            if piv and current_road == 'driveway' and last_road != current_road:
                road_piv = 1
                piv = 0
                last = current_time
                asyncio.run(playgo(driveway_sound()))
            if piv and current_road == 'sidewalk' and last_road != current_road:
                road_piv = 0
                piv = 0
                last = current_time
                asyncio.run(playgo(sidewalk_sound()))
            # 최근 로드 초기화
            last_road = current_road

        y, x = frame.shape[0], frame.shape[1]  # 추론에 사용한 부분만
        # cv2.rectangle(frame, (2 * x // 7, y // 3), (5 * x // 7, y), (0, 0, 255, 255), 2)

        if road_piv:  # 결과 가시화
            cv2.putText(frame, "driveway", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "sidewalk", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)

        # 사람워닝
        person_piv, frame = asyncio.run(warning_person.w_p(yolo_frame, frame))
        if piv and person_piv and current_time - last_person_time > 15:  # 안에 사람이 있고, 7초가 흘렀다면
            last_person_time = current_time  # 계산 후엔 시간 초기화
            piv = 0
            last = current_time
            asyncio.run(playgo(human_sound()))

        if last_road == 'driveway':  # 로드일때 신호등 판단
            # cv2.putText(frame, "driveway", (200, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2, cv2.LINE_AA)

            traffic_piv, frame = asyncio.run(check_traffic_lights.Are_there_traffic_lights(yolo_frame, frame))
            if piv and traffic_piv == 1 and current_time - last_green_time > 60:  # 안에 신호등이 있고, 60초가 흘렀다면
                piv = 0
                last = current_time
                last_green_time = current_time  # 계산 후엔 시간 초기화
                asyncio.run(playgo(green_sound()))

            if piv and traffic_piv == 2 and current_time - last_red_time > 60:  # 안에 신호등이 있고, 60초가 흘렀다면
                piv = 0
                last = current_time
                last_red_time = current_time  # 계산 후엔 시간 초기화
                asyncio.run(playgo(red_sound()))


        else:  # 인도일때 횡단보도 판단

            # cv2.putText(frame, "sidewalk", (200, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2, cv2.LINE_AA)

            corss_walk_piv, frame = asyncio.run(check_crosswalk.Are_there_Crosswalk(yolo_frame, frame))
            if piv and corss_walk_piv == 1 and current_time - last_green_time > 60:  # 안에 신호등이 있고, 60초가 흘렀다면
                piv = 0
                last = current_time
                last_green_time = current_time  # 계산 후엔 시간 초기화
                asyncio.run(playgo(crosswalk_sound()))

        # 바운더리 소리
        num, frame = asyncio.run(check_overlap.calculate_overlap_percentage(yolo_frame, frame))

        if cv2.waitKey(1) & 0xFF == ord('a'):
            # if current_time - last_alarm1_time > 2 and num == 'green':
            # 그린이라면 영상을 저장한다
            asyncio.run(playgo(alarm2_sound()))
            if video_piv:
                out = cv2.VideoWriter('output_video.avi', fourcc, 30, (width, height))
                print("video_start")
                video_piv = 0
                video_start_time = current_time
                mic.start()

            last_alarm1_time = current_time

        """
        if current_time - last_alarm2_time > 2 and num == 'yellow':
            last_alarm2_time = current_time
            asyncio.run(playgo(alarm2_sound()))
        if current_time - last_alarm3_time > 2 and num == 'red':
            last_alarm3_time = current_time
            asyncio.run(playgo(alarm3_sound()))
        """
        if piv == 0 and current_time - last > 2:
            piv = 1

    ########### 비디오를 저장해야해
    if video_piv == 0:
        if current_time - video_start_time < 6:  # 시작시간으로부터 아직 6초가 안지났어
            out.write(frame)
        else:  # 비디오를 저장하고 다시 비디오를 만들 준비를 해
            mic.stop()
            mic.split_audio()
            print("video_stop")
            out.release()
            video_piv = 1
            # 여기까가 저장

            # #여기서 부터 추론
            if infer.infer(video_cls, 'output_video.avi') == 'accident':  # 사고라면
                # 괜찮냐고 물어보기 >
                protocol()

            else:
                # 사고가 아니라면
                print('NOT ACCIDENT')

    ####################
    frame = cv2.resize(frame, (1280, 960))
    cv2.imshow('video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
from module import *
from sound import *
from accident import *
import requests
import mic
import client
from transformers import pipeline
import infer

# video_path = os.path.join('videos_in', 'human_final.mp4')
model_path = os.path.join('models', 'best_yolo8n.pt')
video_cls = pipeline(model="lake-crimsonn/acc-dri-videomae-base")

# cap = cv2.VideoCapture(video_path)
cap = cv2.VideoCapture(0)

width = int(cap.get(3))
height = int(cap.get(4))
model = YOLO(model_path)
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 코덱 설정

pygame.init()
pygame.mixer.init()

last_road_time = 0
last_road = ''
last_person_time = 0
last_green_time = 0
last_red_time = 0
last_alarm1_time = 0
last_alarm2_time = 0
last_alarm3_time = 0
piv = 1
last = int(1e9)
video_piv = 1
video_start_time = 0

while True:
    ret, frame = cap.read()
    if frame is None:
        continue
    raw_time = time.time()
    current_time = int(raw_time)  # 현재시간
    if video_piv:
        yolo_frame = model(frame, verbose=False)
        # yolo그림 그릴거면
        # frame = yolo_frame[0].plot()

        # 딥소트
        # deep_frame = deepsort_start(yolo_frame, frame)  # yolo, frame

        # 로드워닝
        if current_time - last_road_time > 30:  # 30초에 한번씩 계산
            last_road_time = current_time  # 계산 후엔 시간 초기화
            current_road = asyncio.run(func_road.road(frame))  # 터미널에서 모드확인
            # 모드가 바뀌었을 때 한번만 알림 (ex road > road 알림 x)
            current_road = 'driveway'
            if piv and current_road == 'driveway' and last_road != current_road:
                road_piv = 1
                piv = 0
                last = current_time
                asyncio.run(playgo(driveway_sound()))
            if piv and current_road == 'sidewalk' and last_road != current_road:
                road_piv = 0
                piv = 0
                last = current_time
                asyncio.run(playgo(sidewalk_sound()))
            # 최근 로드 초기화
            last_road = current_road

        y, x = frame.shape[0], frame.shape[1]  # 추론에 사용한 부분만
        # cv2.rectangle(frame, (2 * x // 7, y // 3), (5 * x // 7, y), (0, 0, 255, 255), 2)

        if road_piv:  # 결과 가시화
            cv2.putText(frame, "driveway", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "sidewalk", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)

        # 사람워닝
        person_piv, frame = asyncio.run(warning_person.w_p(yolo_frame, frame))
        if piv and person_piv and current_time - last_person_time > 15:  # 안에 사람이 있고, 7초가 흘렀다면
            last_person_time = current_time  # 계산 후엔 시간 초기화
            piv = 0
            last = current_time
            asyncio.run(playgo(human_sound()))

        if last_road == 'driveway':  # 로드일때 신호등 판단
            # cv2.putText(frame, "driveway", (200, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2, cv2.LINE_AA)

            traffic_piv, frame = asyncio.run(check_traffic_lights.Are_there_traffic_lights(yolo_frame, frame))
            if piv and traffic_piv == 1 and current_time - last_green_time > 60:  # 안에 신호등이 있고, 60초가 흘렀다면
                piv = 0
                last = current_time
                last_green_time = current_time  # 계산 후엔 시간 초기화
                asyncio.run(playgo(green_sound()))

            if piv and traffic_piv == 2 and current_time - last_red_time > 60:  # 안에 신호등이 있고, 60초가 흘렀다면
                piv = 0
                last = current_time
                last_red_time = current_time  # 계산 후엔 시간 초기화
                asyncio.run(playgo(red_sound()))


        else:  # 인도일때 횡단보도 판단

            # cv2.putText(frame, "sidewalk", (200, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2, cv2.LINE_AA)

            corss_walk_piv, frame = asyncio.run(check_crosswalk.Are_there_Crosswalk(yolo_frame, frame))
            if piv and corss_walk_piv == 1 and current_time - last_green_time > 60:  # 안에 신호등이 있고, 60초가 흘렀다면
                piv = 0
                last = current_time
                last_green_time = current_time  # 계산 후엔 시간 초기화
                asyncio.run(playgo(crosswalk_sound()))

        # 바운더리 소리
        num, frame = asyncio.run(check_overlap.calculate_overlap_percentage(yolo_frame, frame))

        if cv2.waitKey(1) & 0xFF == ord('a'):
            # if current_time - last_alarm1_time > 2 and num == 'green':
            # 그린이라면 영상을 저장한다
            asyncio.run(playgo(alarm2_sound()))
            if video_piv:
                out = cv2.VideoWriter('output_video.avi', fourcc, 30, (width, height))
                print("video_start")
                video_piv = 0
                video_start_time = current_time
                mic.start()

            last_alarm1_time = current_time

        """
        if current_time - last_alarm2_time > 2 and num == 'yellow':
            last_alarm2_time = current_time
            asyncio.run(playgo(alarm2_sound()))
        if current_time - last_alarm3_time > 2 and num == 'red':
            last_alarm3_time = current_time
            asyncio.run(playgo(alarm3_sound()))
        """
        if piv == 0 and current_time - last > 2:
            piv = 1

    ########### 비디오를 저장해야해
    if video_piv == 0:
        if current_time - video_start_time < 6:  # 시작시간으로부터 아직 6초가 안지났어
            out.write(frame)
        else:  # 비디오를 저장하고 다시 비디오를 만들 준비를 해
            mic.stop()
            mic.split_audio()
            print("video_stop")
            out.release()
            video_piv = 1
            # 여기까가 저장

            # #여기서 부터 추론
            vid_infer = infer.infer(video_cls, 'output_video.avi') == 'accident'
            audio_infer1 = audio_predict.audio_predict('output1.wav',audio_model_path)
            audio_infer2 = audio_predict.audio_predict('output2.wav', audio_model_path)
            audio_infer3 = audio_predict.audio_predict('output3.wav', audio_model_path)
            print('infer')
            print(audio_infer1)
            print(audio_infer2)
            print(audio_infer3)
            if vid_infer or audio_infer1 or audio_infer2 or audio_infer3:
                #비디오나 소리중 하나라도 사고라도 판단했다면
                protocol()

            else:
                # 사고가 아니라면
                print('NOT ACCIDENT')

    ####################
    frame = cv2.resize(frame, (1280, 960))
    cv2.imshow('video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
