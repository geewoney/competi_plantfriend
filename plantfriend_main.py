# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import requests
import json
# import speech_recognition
import speech_recognition as sr
from random import randint
import time
from playsound import playsound
import os
import pygame

rest_api_key = '***'

tts_list = ["부르셨나요?", "잔잔한 노래가 재생됩니다.", "노래를 종료합니다.",
            "몇초 동안 물을 주면 될까요?", "식물의 상태를 파악합니다.",  "다시 한번 말씀해주시겠어요?",
            "다음 노래가 재생됩니다.", "물을 줍니다.", "잘 모르겠어요. 다시 한번 말씀해주세요.", "물주기를 취소합니다."]

KEYWORD_START = ["창우","창우야", "찬우", "차누", "찬우야", "차누야", "강우야", "상우야", "강호야","창호야"]
KEYWORD_WATER = ["물", "울", "불", "화분에 물 좀 줘", "물 좀 줘", "물 좀 줘라", "화분에 물 좀 줘라", "화분에 물 줘라", "물 줘"]
KEYWORD_MUSIC = ["노래", "노래 재생시켜줘", "노래 좀 재생시켜줘", "노래 좀 틀어줘", "노래 틀어줘", "음악", "음악 재생시켜줘", "음악 틀어줘"]
KEYWORD_STATE = ["상태", "정보", "화분 상태 알려줘", "상태 알려줘", "화분 상태 어때"]
KEYWORD_STOP_MUSIC = ["꺼", "종료", "끝", "꺼 줘", "노래 꺼 줘", "음악 꺼 줘", "노래 꺼줘", "음악 꺼줘", "노래꺼줘", "음악꺼줘"]


# kakao api
def kakao_stt(audio):
    kakao_speech_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
    headers = {
        "Content-Type": "application/octet-stream",
        "X-DSS-Service": "DICTATION",
        "Authorization": "KakaoAK " + rest_api_key,
    }

    res = requests.post(kakao_speech_url, headers=headers, data=audio)
    if res.status_code != 200:
        text = ""
        print("error! because ", res.json())
    else:  # 성공했다면,
        result = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}') + 1]
        text = json.loads(result).get('value')

    return text



'''
kakao_tts(num, keyword, temp, humid, sec)
num
0 : 부르셨나요?
1 : 잔잔한 노래가 재생됩니다.
2 : 노래를 종료합니다.
3 : 몇 초 동안 물을 주면 될까요?
4 : 식물의 상태를 파악합니다.
5 : 다시 한 번 말씀해주시겠어요?
6 : 다음 노래가 재생됩니다.
7 : 물을 줍니다.
8 : 잘모르겠어요. 다시 말씀해 주세요.
9 : 물주기를 취소합니다.  

keyword
: 화분 상태(온도, 습도)에 대해 브리핑하는 음성 메시지를 합성할 때 쓰는 키워드.
현재는 화분 상태 확인용 state 밖에 없음(나중에 부가 기능 넣을 때 추가할듯)
 
 temp, humid(온도, 습도)
 : temp 랑 humid 값을 받아서 음성 메시지를 합성하기 위해 받음
 
 sec
 : 스프링쿨러 개방 시간. 그에 따라 음성 메시지 출력
 ex) kakao_tts(7, sec=text) -> {text} 초 동안 물을 줍니다.
'''


def kakao_tts(num, keyword=None, temp=None, humid=None, sec=None):
    kakao_speech_url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
    headers = {
        "Content-Type": "application/xml",
        "X-DSS-Service": "DICTATION",
        "Authorization": "KakaoAK " + rest_api_key,
    }

    message = ""
    if not(keyword):
        message = tts_list[num]
    elif (keyword=="state"):
        message = f"현재 온도는 {temp} 도 이며 습도는 {humid} % 입니다. "
        if humid < 30:
            message = message + f"화분의 흙이 너무 건조해요. 물을 줘야할 것 같아요."
        if temp < 5:
            message = message + f"날씨가 너무 추워요. 화분을 실내에 보관해주세요."
        if temp > 40:
            message = message + f"날씨가 너무 더워요. 화분을 실내에 보관해주세요."
    if sec:
        message = str(sec) + " 초 동안" + tts_list[num]

    data = f"<speak>{message.encode('utf-8').decode('latin1')}</speak>"
    res = requests.post(kakao_speech_url, headers=headers, data=data)
    filename = f"tmp/hi{num}.mp3"
    f = open(filename, "wb")
    f.write(res.content)
    f.close()
    playsound(filename)
    # os.remove(filename)
    return filename




def set_mic():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(sample_rate=16000)
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    return recognizer, microphone


# mic input
def get_speech(recognizer, microphone):
    # 음성 수집
    with microphone as source:
        # print("Say something!")
        result = recognizer.listen(source, timeout=0, phrase_time_limit=3)
        audio = result.get_raw_data()
    return audio




def listening(recognizer, microphone):
    while True:
        audio_i = get_speech(recognizer, microphone)
        try:
            text = kakao_stt(audio_i)
            return text
        except (ValueError, TimeoutError):
            # print("리트")
            continue



def plant_state():
    humid = humid_sensor()
    temp = randint(20, 30)
    print(f"현재 수분 {humid }% ")
    return temp, humid



def humid_sensor():
	humidsensor = 16
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(humidsensor, GPIO.IN)
	cnt = 0

	for i in range(10):
		input_state = GPIO.input(humidsensor)
		if input_state == False:
			print("enough water")
			time.sleep(0.1)
			cnt += 1
		else:
			print("need water")
	time.sleep(0.1)
	if cnt > 1:
		return cnt * 10 + randint(0, 10)
	elif cnt == 10:
		return cnt
	else:
		return randint(0, 5)



def play_music(title):
    music_dir = "Music/"
    pygame.mixer.init()
    pygame.mixer.music.load(music_dir+title)
    pygame.mixer.music.play()
    recognizer, microphone = set_mic()
    pygame.mixer.music.set_volume(0.4)
    while pygame.mixer.music.get_busy():
        message = listening(recognizer, microphone)
        if message in KEYWORD_START:
            pygame.mixer.music.set_volume(0.1)
            kakao_tts(0)
            message2 = listening(recognizer, microphone)
            print(message2)

            if message2 in KEYWORD_STOP_MUSIC:
                kakao_tts(2)
                pygame.mixer.music.stop()
                return False

            elif message2 in KEYWORD_WATER:
                result = watering()

                if result:
                    kakao_tts(9)

            elif message2 in KEYWORD_STATE:
                temp, humid = humidity()
                kakao_tts(4, keyword="state", temp=temp, humid=humid)

            if "다음" in message2:
                kakao_tts(6)
                pygame.mixer.music.stop()
                return True

            time.sleep(1)
            pygame.mixer.music.set_volume(0.4)

    pygame.mixer.music.stop()
    return True



def watering():
    recognizer, microphone = set_mic()
    kakao_tts(3)
    text = listening(recognizer, microphone)

    if "취소" in text:
        return True

    if "초" in text:
        text = text.split("초")[0]
    while True:
        # print(text)
        if text in num_list:
            break
        kakao_tts(5)
        text = listening(recognizer, microphone)
        if "초" in text:
            text = text.split("초")[0]

    text = int(text)
    time.sleep(2)
    kakao_tts(7, sec=text)
    water_open()
    # n 초 동안 오픈
    time.sleep(text)
    water_close()

    return False




n_list = list(range(1,11))
num_list = list(map(str,n_list))

def water_open():
    print("스프링쿨러를 엽니다")
    ''''''''''''
    ''' 미구현 '''
    ''''''''''''

def water_close():
    print("스프링쿨러를 닫습니다")
    ''''''''''''
    ''' 미구현 '''
    ''''''''''''



# ------ MAIN ------ #

def main_ttstest():
    workdir = "/home/pi/Desktop/kakao_tts"
    # workdir = "C:/Users/LG/PycharmProjects/pythonProject/kakao_tts"
    # workdir = "F:/kakao_tts/kakao_tts"

    recognizer, microphone = set_mic()
    while True:
        text = listening(recognizer, microphone)
        print(text)
        if text in KEYWORD_START:
            kakao_tts(0)
            text = listening(recognizer, microphone)

            # 물주기 (1 ~ 10초)
            if text in KEYWORD_WATER:
                result = watering()

                if result:
                    kakao_tts(9)

            # 노래 켜기
            elif text in KEYWORD_MUSIC:
                kakao_tts(1)
                file_list = os.listdir("Music/")
                music_list = [file for file in file_list if file.endswith(".mp3")]
                state = True
                while (state):
                    for music in music_list:
                        play = play_music(music)
                        if not play:
                            state = False
                            break


            # 화분 상태 확인
            elif text in KEYWORD_STATE:
                temp, humid = humidity()
                kakao_tts(4, keyword="state", temp=temp, humid=humid)
            # 재질문

            else:
                kakao_tts(8)



if __name__ == "__main__":
    main_ttstest()
