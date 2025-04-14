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
```
Trigger에서 0.00001초만큼 주면  40kHz 만큼 8개 파형이 나간다. (근데 start 타임을 못잡음. 언제나갈지모름) : 0.00025*8
하지만 첫 신호가 오는 시점은 안다. 따라서 첫 신호가 오는 시점을 startTime으로 잡는다. 몇개오는지는 모르지만 마지막에 오는 파형 시간을 endTime으로 한다. 즉, 처음들어오는 시간과 마지막 파형이 들어오는 시간의 갭으로 거리를 계산한다. (거의 흡사하다. ) 이런 이론을 가지고 만들어진것이 이 장비임.
거리 계산: 거리는 에코 핀이 HIGH 상태를 유지한 시간을 측정하여 계산됨.
만약 startTime-endTime=0.2초라면 거리는 34.3m(3430cm)이다. 
그러나 이 장비는 4m까지밖에 측정 못함.
```

## 거리 측정 결과에 따라 LED의 밝기를 조절하는 코드 (멀수록 밝다!)
- 초음파 센서 (TRIG, ECHO): 거리 측정
- LED (핀 17번): PWM으로 밝기 조절
- get_distance(): 시간 기반 거리(cm) 계산 함수
- 측정된 거리 → 밝기(Duty Cycle)로 변환 ```pwm.ChangeDutyCycle(dist)```
  - 거리 dist가 0~99 사이일 때, 그 값을 PWM 듀티 사이클로 사용
  - 거리값이 클수록(멀수록) 듀티 사이클이 커지고, LED에 인가되는 평균 전압이 커져서 LED 밝기가 밝아짐
  - 최대 99로 제한됨 ```if dist > 100: dist = 99```
```python
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
    GPIO.output(TRIG, GPIO.LOW) # TRIG 핀을 False(0V)로한
            dist = 99

        pwm.ChangeDutyCycle(dist) # 측정된 거리 밝기(Duty Cycle)로 변환
        time.sleep(0.1)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
```
