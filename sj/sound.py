import os
import asyncio
import pygame

sidewalk_path = os.path.join('voices', '05_인도_모드로_변경합니다.mp3')
driveway_path = os.path.join('voices', '06_차도_모드로_변경합니다.mp3')
human_path = os.path.join('voices', '09_주행경로에_사람이_있습니다_조심하세요.mp3')
green_path = os.path.join('voices', '07_초록불_입니다.mp3')
red_path = os.path.join('voices', '08_빨간불_입니다.mp3')
crosswalk_path = os.path.join('voices', '01_횡단보도다.mp3')
alarm1_path = os.path.join('voices', '경계_1단계.mp3')
alarm2_path = os.path.join('voices', '주의_2단계.mp3')
alarm3_path = os.path.join('voices', '위험_3단계.mp3')
gamji_path = os.path.join('voices', '사고를_감지했습니다_도움이_필요하십니까.mp3')
mueungdap_path = os.path.join('voices', '계속된_무응답으로_등록된_지인에게_문자를_발송하겠습니다.mp3')
dasi_path = os.path.join('voices', '다시_한번_말씀해주세요.mp3')
jiin_path = os.path.join('voices', '등록된_지인에게_문자를_발송하겠습니다.mp3')
alget_path = os.path.join('voices', '알겠습니다_안전_운행하세요.mp3')

async def gamji_sound():
    sc(gamji_path)

async def mueungdap_sound():
    sc(mueungdap_path)

async def dasi_sound():
    sc(dasi_path)

async def jiin_sound():
    sc(jiin_path)

async def alget_sound():
    sc(alget_path)

async def alarm1_sound():
    sc(alarm1_path)

async def alarm2_sound():
    sc(alarm2_path)

async def alarm3_sound():
    sc(alarm3_path)

async def crosswalk_sound():
    sc(crosswalk_path)

async def green_sound():
    sc(green_path)

async def red_sound():
    sc(red_path)

async def human_sound():
    sc(human_path)

async def sidewalk_sound():
    sc(sidewalk_path)

async def driveway_sound():
    sc(driveway_path)

async def playgo(sound_func):
    task1 = asyncio.create_task(sound_func)
    await task1

class SoundClass:
    def __call__(self, path):
        sd = pygame.mixer.Sound(path)
        sd.play()
        return None

sc = SoundClass()