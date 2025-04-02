# 1. 버저(Buzzer) 액츄레이터 모듈 설치
1. <mark>액티브 버저 모듈</mark>
  - 액티브 버저 모듈은 전기 신호를 받았을 때 소리를 내는 장치.
  - 내장된 발진 회로를 가지고 있어서 단순히 <mark>전원을 공급하면 특정 주파수로 소리</mark>를 낼 수 있음.
  - 액티브 버저는 로봇, 알람 시스템, 사용자 인터페이스 피드백 등 다양한 응용 프로그램에 사용됨.
2. 기본 사양
  - 전원 공급: 일반적으로 3.3V 또는 <mark>5V</mark> DC
  - 소비 전류: 약 30mA
  - 작동 주파수: 주로 <mark>2kHz</mark> 내외 (<mark>1초에 최대 2000번의 진폭(진동)</mark>)
    - <mark>Hz: 1초 안에 생기는 진폭을 헤르츠(Hz)라고 한다.</mark>
    - <mark>가정주파수: 20Hz~20kHz</mark>
    - 2kHz = 1초->2000번 진폭 = 0.5초->1000번 진폭 = 0.05초->100번 진폭 = 0.005초->10번 진폭
    - <mark>음의 높낮이는 주파수로 결정된다<mark>
      - 도레미파솔라시도 -> Hz가 다름 (ex.도: 261.63 Hz)
  - <mark>소리 크기: 약 85 dB 정도<mark>
    - <mark>db: 소리의 크고 작음<mark>
    - 2Hz의 음높이에서 소리를 크게 하고 싶다면 -> 1초에 진폭(봉우리)가 2개인데, <mark>봉우리의 높이가 커짐<mark>
  - GPIO 연결
    - VCC : 3.3V 또는 5V Power(<mark>핀 2</mark>)
    - GND : Ground 접지(<mark>핀 14</mark>)
    - <mark>IN : 입력 핀으로 LOW 또는 HIGH 신호에 따라 버저가 활성화 됨</mark> (<mark>GPIO 17(핀 11)</mark>)
---
# 2. 버저(Buzzer) 액츄레이터 구동 및 응용
## 기본 구동 프로그램 
- GPIO 17핀(핀 11)을 출력 모드로 설정
- GPIO 17핀을 순회하면 On/Off 코딩
- 키보드 인터럽트 발생까지 단순히 부저 HIGH, LOW가 반복, 터미널에 상태 출력
- <mark>GPIO.out() 사용하여 부저를 켜고 끔</mark>
<br>buzzer.py
```python
import RPi.GPIO as GPIO
import time

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# 사용할 GPIO 핀의 번호를 설정한다. 여기서는 17번 핀을 사용한다.
BUZZER_PIN = 17
GPIO.setup(BUZZER_PIN, GPIO.OUT)

try:
    while True:
        # 부저를 켠다.
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        print("Buzzer on")
        time.sleep(1) # 1초 동안 대기

        # 부저를 끈다.
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        print("Buzzer off")
        time.sleep(1) # 1초 동안 대기

except KeyboardInterrupt:
    # 프로그램 종료 시 GPIO 핀 상태를 초기화한다.
    GPIO.cleanup()
```

---
## 계이름 응용 구동 프로그램
- 주파수 대역과 음 지속 시간을 이용하여 계이름(도레미파...시도) 소리 출력
- 도(C4)가 0.5초동안 261.63/2번 진동 -> 0.1초동안 LOW -> 레(D4)가 0.5초동안 293.66/2번 진동 ->  0.1초동안 LOW -> ...
- <mark>PWM 인스턴스 생성하여 부저 제어 (GPIO.PWM())</mark>
<br>buzzer_melody.py
```python
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
```


## [문제: 부저를 이용한 동요 재생 실습]
buzzer_melody_star.py
```python
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
```


## [문제: 3Color LED와 부저를 이용한 동요 재생 실습]
buzzer_melody_led.py
- 3컬러 RGB LED는 아래와 같이 연결되어 있다.
  - 빨강: GPIO 18
  - 초록: GPIO 23
  - 파랑: GPIO 24
  - GND: 핀9
- 작은별 멜로디를 부저로 연주한다.
- 각 음이 재생될 때, 해당 음에 지정된 색상으로 RGB LED가 점등된다.
- 음이 끝나면 LED는 꺼진다.
```python
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
```
