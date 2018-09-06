import os
import time
import datetime
import threading
from pyowm import OWM
import RPi.GPIO as GPIO

def weather():

    # 날씨정보 받아오기
    API_key = '0d2f0a799c84678504d2e5b90c0f776a'
    owm = OWM(API_key)
    obs = owm.weather_at_place('Seoul')
    w = obs.get_weather()

    # 날씨정보 출력
    print('시 간 : ', datetime.datetime.now())
    print('날 씨 : ', w.get_status())
    print('온 도 : ', int(w.get_temperature(unit='celsius')['temp']))
    print('습 도 : ', w.get_humidity())

    # 라즈베리파이 'GPIO' 신호
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    temperature = str(w.get_temperature(unit='celsius')['temp'])
    humidity_str = str(w.get_humidity())
    weather_now = str(w.get_status())

    # 날씨가 'Rain'일 경우 LED 점등, GPIO 9번 핀 사용
    if weather_now == 'Rain':
        GPIO.setup(9, GPIO.OUT)
        GPIO.output(9, 1)
    else :
        GPIO.setup(9, GPIO.OUT)
        GPIO.output(9, 0)

    # 'espeak' 모듈로 날씨 정보 읽어주기
    os.system("espeak -v ko -a 200 '날씨는'")
    os.system("espeak -a 200 '" + w.get_status()+ "'")
    os.system("espeak -a 200 '온도는'")
    
    # 온도가 0도 이하일 경우 '영하'로 읽어주기
    if temperature[0] == '-':
        temperature_modify = temperature.replace("-","")
        temperature_int_str = str(int(float(temperature_modify))) # 실수로 표시된 온도를 정수로 표시
        os.system("espeak -a 200 '영하'")
        os.system("espeak -v ko -a 200 '" + temperature_int_str + "'")
        os.system("espeak -a 200 '도'")
    else :
        temperature_int_str = str(int(float(temperature)))
        os.system("espeak -v ko -a 200 '" + temperature_int_str + "'")
        os.system("espeak -a 200 '도'")
        
    os.system("espeak -a 200 '습도는'")
    os.system("espeak -v ko -a 200 '" + humidity_str + "'")
    os.system("espeak -a 200 '입니다'")

    # 10초 후 함수 재실행
    timer = threading.Timer(10, weather)
    timer.start()
    
    
    # 세그먼트 설정
    segments = (11, 14, 23, 8, 7, 10, 18, 25)
    for segment in segments :
        GPIO.setup(segment, GPIO.OUT)
        GPIO.output(segment, 0)


    num = {
           '0' : (0,0,0,0,0,0,1,1),
           '1' : (1,0,0,1,1,1,1,1),
           '2' : (0,0,1,0,0,1,0,1),
           '3' : (0,0,0,0,1,1,0,1),
           '4' : (1,0,0,1,1,0,0,1),
           '5' : (0,1,0,0,1,0,0,1),
           '6' : (0,1,0,0,0,0,0,1),
           '7' : (0,0,0,1,1,0,1,1),
           '8' : (0,0,0,0,0,0,0,1),
           '9' : (0,0,0,0,1,0,0,1)}

    # 습도 1의 자리와 10의 자리 수를 번갈아가며 점등
    humidity_unit = int(humidity_str[0])
    humidity_ten = int(humidity_str[1])
    while 1:
    # 습도 1의 자리 출력
        GPIO.setup(27, GPIO.OUT)
        GPIO.output(27, 0)
        GPIO.setup(22, GPIO.OUT)
        GPIO.output(22, 1)
        for i in range(0, 10) :
            if humidity_unit == i :
                s = str(i)
                for loop in range(0, 8):
                    GPIO.output(segments[loop], num[s][loop])
        time.sleep(0.005)

    # 습도 10의 자리 출력
        GPIO.setup(22, GPIO.OUT)
        GPIO.output(22, 0)
        GPIO.setup(27, GPIO.OUT)
        GPIO.output(27, 1)
        for i in range(0, 10) :
            if humidity_ten == i :
                s = str(i)
                for loop in range(0, 8):
                    GPIO.output(segments[loop], num[s][loop])
        
        time.sleep(0.005)

weather()