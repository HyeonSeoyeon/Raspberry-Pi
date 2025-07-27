import RPi.GPIO as GPIO
import time

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# Buzzer 핀 설정
BUZZER_PIN = 17
GPIO.setup(BUZZER_PIN, GPIO.OUT)
pwm = None

# PWM 인스턴스 생성 및 초기 주파수 설정
pwm = GPIO.PWM(BUZZER_PIN, 100) #부저의 경우 MAX 2000(2kHz), 출력 범위(약 1Hz ~ 10kHz)
pwm.start(0)  

# 주요 음표의 주파수 (단위: Hz)
notes = {
    'C4': 261.63, # 도
    'D4': 293.66, # 레
    'E4': 329.63, # 미
    'F4': 349.23, # 파
    'G4': 392.00, # 솔
    'A4': 440.00, # 라
    'B4': 493.88, # 시
    'C5': 523.25  # 추가된 높은 도 음표
}

# 간단한 멜로디 (음표와 지속 시간)
melody = [('C4', 0.5), ('C4', 0.5), ('G4', 0.5), ('G4', 0.5), ('A4', 0.5), ('A4', 0.5), ('G4', 1.0), #도도솔솔라라솔
          ('F4', 0.5), ('F4', 0.5), ('E4', 0.5), ('E4', 0.5), ('D4', 0.5), ('D4', 0.5), ('C4', 1.0), #파파미미레레도
          ('G4', 0.5), ('G4', 0.5), ('F4', 0.5), ('F4', 0.5), ('E4', 0.5), ('E4', 0.5), ('D4', 1.0), #솔솔파파미미레
          ('G4', 0.5), ('G4', 0.5), ('F4', 0.5), ('F4', 0.5), ('E4', 0.5), ('E4', 0.5), ('D4', 1.0), #솔솔파파미미레
          ('C4', 0.5), ('C4', 0.5), ('G4', 0.5), ('G4', 0.5), ('A4', 0.5), ('A4', 0.5), ('G4', 1.0), #도도솔솔라라솔
          ('F4', 0.5), ('F4', 0.5), ('E4', 0.5), ('E4', 0.5), ('D4', 0.5), ('D4', 0.5), ('C4', 1.0)] #파파미미레레도

def play(note, duration):
    pwm.ChangeFrequency(notes[note])
    pwm.ChangeDutyCycle(50)  # 켜짐
    time.sleep(duration)  # 음표 지속 시간
    pwm.ChangeDutyCycle(0)  # 꺼짐
    
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