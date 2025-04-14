# 초음파 센서 (Ultrasonic Sensor)

## HC-SRO4 초음파 모듈
- <mark>**초음파 파동을 발사하여 목표물에 부딪힌 후 반사되어 돌아오는 시간을 측정함으로써 거리 산출**</mark>
- 로봇, 장애물 회피 시스템, 자동 주차 시스템 등에 사용
- 기본 사양
  - 전원 공급: **5V** DC
  - 소비 전류: **15mA**
  - 작동 주파수: **<mark>40kHz (40000Hz)</mark>**
  - 최대 범위: 약 **4m**
  - 최소 범위: **2cm**
  - 측정 각도: 약 **15도**
  - 인터페이스: **<mark>VCC, Trig(Trigger), Echo, GND</mark>**
 
## HC-SRO4 초음파 모듈 작동원리
- 사용자가 트리거 핀에 10µs(0.00001초) 이상 HIGH 상태의 펄스 신호를 입력하여 초음파 파동 발사 준비 (지금 초음파를 쏴라 명령)
- 초음파 발사: 센서에서 40kHz(40000kHz)의 초음파 파동을 8개 연속으로 200µs(0.0002초)동안 발사함.
- 1번 진동하는 데 걸리는 시간: ```1초 / 40,000 = 0.000025초 = 25µs (마이크로초)```
- 8번 진동 (8개 파동을 송신)하는 데 걸리는 시간: ```25µs × 8 = 200µs = 0.0002초```
- <mark>즉, 트리거 핀에 10µs(0.00001초) 이상 HIGH가 되면 센서는 40kHz 초음파를 연속으로 8번 200µs 동안 송신한다</mark>
- Echo 신호: 초음파 파동이 목표물에 반사되어 센서로 돌아오면, 에코핀이 HIGH 상태가 됨.
- 즉, <mark>Echo의 HIGH 상태의 지속 시간 = 왕복 시간</mark>과 직접적인 연관이 있음.
- 거리 계산: 거리 = (왕복 시간 × 소리의 속도) / 2
  - 소리의 속도 = 34300 cm/s (단위 맞춰서 사용!)
  - 갔다가 돌아오는 데 걸린 시간을 재기 때문에 나누기 2를 해야함.

## 거리 측정 결과에 따라 LED의 밝기를 조절하는 코드 (멀수록 밝다!)
- 초음파 센서 (TRIG, ECHO): 거리 측정
- LED (핀 17번): PWM으로 밝기 조절
- get_distance(): 시간 기반 거리(cm) 계산 함수
- 측정된 거리 → 밝기(Duty Cycle)로 변환 ```pwm.ChangeDutyCycle(dist)```
  - 거리 dist가 0~99 사이일 때, 그 값을 PWM 듀티 사이클로 사용
  - 거리값이 클수록(멀수록) 듀티 사이클이 커지고, LED에 인가되는 평균 전압이 커져서 LED 밝기가 밝아짐
  - 최대 99로 제한됨 ```if dist > 100: dist = 99```
```
import RPi.GPIO as GPIO
import time

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# 핀 번호 할당
TRIG = 23
ECHO = 24
LED = 17

# 입출력 설정
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

# PWM 설정
pwm = GPIO.PWM(LED, 100)  # 100Hz
pwm.start(0)  # 초기 듀티 사이클 0

# 센서로부터 거리 정보를 측정하고 그 값을 반환하는 함수
def get_distance():
    GPIO.output(TRIG, GPIO.LOW) # TRIG 핀을 False(0V)로 설정해 초기화. 측정 전에 트리거 핀을 정리
    time.sleep(0.5) # 이전 측정의 잔여 신호에서 완전히 안정화되기 위한 대기 시간

    # 신호 송신부에서 40kHz 신호 8개 송신(200µs 동안)
    GPIO.output(TRIG, GPIO.HIGH) # TRIG 핀을 True(3.3V 또는 5V)로 설정해 트리거 핀에 10μs(0.00001초) 동안의 고전압 신호를 보낸다. 초음파 파동을 발생한다
    time.sleep(0.00001) # 초음파 펄스를 발생시키기 위한 대기시간. 10μs시간 동안의 펄스는 센서로 하여금 충분한 에너지를 가진 초음파 파동을 발생
    GPIO.output(TRIG, GPIO.LOW) # TRIG 핀을 다시 False로 설정해 트리거 신호를 종료

    # 초음파 파동이 발사되고 반사되어 돌아온 첫 신호와 마지막 신호의 시간 측정
    while GPIO.input(ECHO) == GPIO.LOW:  # ECHO 핀이 HIGH 상태로 전환되기를 기다림림
        pulse_start = time.time()  # 초음파 펄스가 ECHO에 처음 도착한 시간 기록
    while GPIO.input(ECHO) == GPIO.HIGH:  #  ECHO 핀이 LOW 상태로 돌아갈 때까지 기다림
        pulse_end = time.time()  # 초음파 펄스 ECHO에 마지막 도착한 시간 기록록

    pulse_duration = pulse_end - pulse_start  # 초음파 파동이 발사되어 돌아오는 데 걸린 전체 시간을 계산
    distance = pulse_duration * (34300 / 2) # 소리속도 34300 cm/s
    distance = round(distance, 2)  # 거리를 소수점 둘째 자리까지 반올림
    return distance

try:
    while True:
        dist = get_distance()
        print("Distance:", dist, "cm")

        if dist > 100: # 최대 99로 제한
            dist = 99

        pwm.ChangeDutyCycle(dist) # 측정된 거리 → 밝기(Duty Cycle)로 변환
        time.sleep(0.1)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
```
