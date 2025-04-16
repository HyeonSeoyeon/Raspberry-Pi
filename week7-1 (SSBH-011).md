# 조도 센서(SSBH-011)

## 조도 센서
- <mark>빛의 강도를 측정</mark>하는 센서
- <mark>AO(사용하지 않음), DO, GND, VCC로 구성</mark>
- 연결하면 불이 들어오는게 정상. 조도를 가리면 하나의 불이 꺼지는 것이 정상.
- <mark>디지털 방식과 아날로그 방식</mark> 2가지를 지원
  - **아날로그(AO) 출력**
<img src="https://hull.kr/data/editor/2504/20250416111225_0fd1cf29e08b1daf969476e28323e046_gvky.png"/>
    - 빛의 강도에 따라 연속적으로 변하는 전압 신호를 출력함.
    - <mark>MCP3208 모듈 등의 아날로그-디지털 변환기(ADC)를 활용 함.</mark>
    - <mark>광이 측정되면 ADC값이 작게, 측정 안되면 ADC값이 크다!</mark>
    - 라즈베리파이에는 아날로그 입력 불가능. 따라서 SPI 인터페이스로 통신하는 외부 ADC 필요
  - **디지털(DO) 출력**
<img src="https://hull.kr/data/editor/2504/20250416105933_0fd1cf29e08b1daf969476e28323e046_t180.png"/>
    - <mark>조도가 설정된 임계값을 초과할 때 디지털 신호 LOW(밝을 때 LOW), 초과하지 않을 때 디지털 신호 HIGH(어두울때 HIGH)를 출력하는 방식.</mark>
    - <mark>센서 모듈에 있는 파란색 가변 저항(트리머)을 사용하여 임계값을 설정 가능. (시계 방향: 임계값을 높임 -> 더 높은 조도에서 LOW 출력 / 반시계 방향: 임계값을 낮춤 -> 더 낮은 조도에서 LOW 출력) => 조도센서가 어두움을 잘 감지 못한다면 반시계방향으로 돌려라? (이해안감...)</mark>
- 환경 모니터링, 스마트 홈 시스템, 자동화 시스템 등 다양한 분야에서 사용됨.
  - 예: 해가 지면 자동으로 켜지는 가로등에 사용된다. 어두워지면 high값을 줘서 동작하게 하고, 밝아지면 low값을 줘서 동작하지 않게 함. (디지털 출력)
  - 현관에 사용되는 센서는 적외선 센서임.
- 감도 조절: 내장된 가변 저항을 통해 감도 조절 가능
- 빛의 강도 측정 범위: 보통 0~2000 루멘 (lm) (센서에 따라 다를 수 있음)

### 조도 디지털 모드 센서 모듈 구동
- GND  : Ground 접지(핀 14)
- VCC : 5V Power(핀 2)
- DO : GPIO 17(핀 11)
<br>light_sensor_digital.py
```python
import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정 (조도 센서의 DO 핀 연결)
SENSOR_PIN = 17  # GPIO 17 (핀 번호 11)

# GPIO 설정
GPIO.setmode(GPIO.BCM)  # GPIO 번호 모드를 BCM 모드로 설정
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 내부 풀다운 저항 사용
# SENSOR_PIN을 입력 모드로 기본적으로 LOW(0) 상태(=조도 높음으로 초기 시작) 유지로 설정

print('조도 센서 값 읽기 시작...')

try:
    while True:
        sensor_value = GPIO.input(SENSOR_PIN) # 지정된 GPIO 핀의 현재 값을 읽음.
        if sensor_value == GPIO.HIGH: # 값이 HIGH(1)이면 조도가 임계값 미만
            print('조도가 낮습니다.')
        else:  # LOW(0)이면 임계값 이상임
            print('조도가 높습니다.')
        time.sleep(1)
        '''
        센서는 현재 조도 증가 → LOW, 조도 감소 → HIGH 출력
        조도가 없을 때, 즉 어두워 졌을 때(HIGH) 감지를 목표 (내부 풀다운 저항 활성화)
        '''

except KeyboardInterrupt:
    print("프로그램 종료")
finally:
    GPIO.cleanup()

```

---

## 왜 밝으면 LOW이고 어두우면 HIGH으로 출력되는가? (아날로그(AO) 출력 특성)
- 전압 측정은 ADC(아날로그-디지털 변환기)와 관련이 있다.
- 2가지 갈림길이 있다고 생각하면 된다. 소비전류와 측정전류. 
- 조도 센서의 AO 측정 출력 특성: <mark>일반형(반비례) 방식</mark> (일반적인 사용)
  - <mark>빛의 강도 측정(조도 증가, 밝아지면) -> LDR의 저항 감소 -> LDR 쪽으로 흐르는 전류가 많아짐 -> 의미없이 들어가는 전류. 즉, 소비 전류의 증가 -> 대신 AO 측정 전압 감소 -> 이것은 ADC와 관련이 있다 ->따라서 밝아지면 LOW</mark>
- 조도 센서의 AO 측정 출력 특성: <mark>역형(비례)</mark>
  - 반대로 우리가 알고있는 상식선의 장비로 바꾸려고 하면 <mark>리버스 회로를 구현</mark>해야하기 때문에 더 비싸다.
  - 조도 증가시 AO 측정 전압 증가 -> 따라서 밝아지면 HIGH

