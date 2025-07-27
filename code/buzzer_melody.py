import RPi.GPIO as GPIO
import time

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# Buzzer 핀 설정
BUZZER_PIN = 17
GPIO.setup(BUZZER_PIN, GPIO.OUT)
pwm = None

# PWM 인스턴스 생성 및 초기 주파수 설정
#부저의 경우 MAX 2000(2kHz), 출력 범위(약 1Hz ~ 10kHz)
pwm = GPIO.PWM(BUZZER_PIN, 100) # 초기값을 100Hz로 설정
pwm.start(0)

# 주요 음표의 주파수 (단위: Hz)
notes = {
    'C4': 261.63,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 493.88,
    'C5': 523.25  # 높은 도 음표
}

# 작은별 멜로디 (음표와 지속 시간)
melody = [('C4', 0.5), ('D4', 0.5), ('E4', 0.5), ('F4', 0.5),
          ('G4', 0.5), ('A4', 0.5), ('B4', 0.5), ('C5', 0.5)]

def play(note, duration):
    pwm.ChangeFrequency(notes[note])
    pwm.ChangeDutyCycle(50)  # 켜짐, High와 Low를 1:1 비율로 보냄
    time.sleep(duration)  # 음표 지속 시간
    pwm.ChangeDutyCycle(0)  # 꺼짐, High 신호를 안 보냄

try:  
    for note, duration in melody:
        play(note, duration)
        time.sleep(0.1)  # 음표 사이의 간격, 다음 음 사이에 Low가 0.1초 동안 감.
finally:
    if pwm is not None:
        try:
            pwm.stop()
        except:
            pass
        del pwm  # __del__ 호출 시 오류 방지
    GPIO.cleanup()