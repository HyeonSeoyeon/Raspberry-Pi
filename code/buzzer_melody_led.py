import RPi.GPIO as GPIO
import time

# LED 핀 번호 설정
RED_PIN = 18
GREEN_PIN = 23
BLUE_PIN = 24

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup([RED_PIN, GREEN_PIN, BLUE_PIN], GPIO.OUT)

# Buzzer 핀 설정
BUZZER_PIN = 17
GPIO.setup(BUZZER_PIN, GPIO.OUT)
pwm = GPIO.PWM(BUZZER_PIN, 100)  # 초기 주파수 설정
pwm.start(0)

# 주요 음표의 주파수 (단위: Hz)
notes = {
    'C4': 261.63, #도
    'D4': 293.66, #레
    'E4': 329.63, #미
    'F4': 349.23, #피
    'G4': 392.00, #솔
    'A4': 440.00, #라
    'B4': 493.88, #시
    'C5': 523.25 #높은 도
}

# RGB 상태(GPIO)
colors = {
    'C4': (1, 0, 0), # 도, 빨
    'D4': (0, 1, 0), # 레, 초
    'E4': (0, 0, 1), # 미, 파
    'F4': (1, 1, 0), # 파, 노
    'G4': (0, 1, 1), # 솔, 하
    'A4': (1, 0, 1), # 라, 보
    'B4': (1, 1, 1), # 시, 흰
    'C5': (1, 0, 0) # 도, 빨
}

# 작은 별 멜로디
melody = [
    ('C4', 0.5), ('C4', 0.5), ('G4', 0.5), ('G4', 0.5), ('A4', 0.5), ('A4', 0.5), ('G4', 1.0), #빨빨하하보보하
    ('F4', 0.5), ('F4', 0.5), ('E4', 0.5), ('E4', 0.5), ('D4', 0.5), ('D4', 0.5), ('C4', 1.0), #노노파파초초빨
    ('G4', 0.5), ('G4', 0.5), ('F4', 0.5), ('F4', 0.5), ('E4', 0.5), ('E4', 0.5), ('D4', 1.0), #하하노노파파초
    ('G4', 0.5), ('G4', 0.5), ('F4', 0.5), ('F4', 0.5), ('E4', 0.5), ('E4', 0.5), ('D4', 1.0), #하하노노파파초
    ('C4', 0.5), ('C4', 0.5), ('G4', 0.5), ('G4', 0.5), ('A4', 0.5), ('A4', 0.5), ('G4', 1.0), #빨빨하하보보하
    ('F4', 0.5), ('F4', 0.5), ('E4', 0.5), ('E4', 0.5), ('D4', 0.5), ('D4', 0.5), ('C4', 1.0) #노노파파초초빨
]

def play(note, duration):
    r, g, b = colors[note]
    GPIO.output([RED_PIN, GREEN_PIN, BLUE_PIN], [r, g, b])  # LED 켜기
    pwm.ChangeFrequency(notes[note])
    pwm.ChangeDutyCycle(50) # 부저 켜짐
    time.sleep(duration) # 음표 지속 시간
    pwm.ChangeDutyCycle(0)  # 부저 끄기
    GPIO.output([RED_PIN, GREEN_PIN, BLUE_PIN], (0, 0, 0))  # LED 끄기
    
try:  
    for note, duration in melody:
        play(note, duration)
        time.sleep(0.1)  # 음표 사이의 간격
finally:
    if pwm is not None:
        try:
            pwm.stop()
        except:
            pass
        del pwm  # __del__ 호출 시 오류 방지
    GPIO.cleanup()








