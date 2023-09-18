import speech_recognition as sr
import playsound
import time
import os
import asyncio
import requests
from sound import *
import client


def protocol():
    #time.sleep(1)
    asyncio.run(playgo(gamji_sound()))
    r = sr.Recognizer()
    cnt = 0
    print('>>> 사고가 감지되었습니다. 도움이 필요하신가요?')
    while True:
        time.sleep(0.5)

        with sr.Microphone() as source:
            audio = r.listen(source, phrase_time_limit=2)
            try:
                # 소리 인식
                audio_text = r.recognize_google(audio, language='ko-KR')
                print('[사용자] ' + audio_text)
                # 사고가 났을 때
                if '도와줘' in audio_text:
                    asyncio.run(playgo(jiin_sound()))
                    time.sleep(0.2)
                    print('등록된 지인에게 문자를 발송하겠습니다.')
                    # 문자보내기
                    #response = requests.get('http://192.168.0.106:5000/sms/send')
                    #화상채팅
                    #client.start_video_call('http://192.168.0.106:5000/wc')
                    break
                # 사고가 나지 않았을 때
                elif '아니' in audio_text:
                    asyncio.run(playgo(alget_sound()))
                    time.sleep(0.2)
                    print('네. 안전운행하세요.')
                    break
            except:
                pass

            # 무응답일 때
            cnt += 1
            if cnt == 3:
                asyncio.run(playgo(mueungdap_sound()))
                time.sleep(0.2)
                print('>>> 계속된 무응답으로 등록된 지인에게 문자를 발송하겠습니다.')
                # 문자보내기
                #response = requests.get('http://192.168.0.106:5000/sms/send')
                #화상채팅
                #client.start_video_call('http://192.168.0.106:5000/wc')
                break

            # 조건에 해당되지 않으면 다시 물어본다.
            asyncio.run(playgo(dasi_sound()))
            time.sleep(0.2)
            print('>>> 다시 한번 말씀해주세요.')
