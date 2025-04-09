# PWM DutyCycle을 이용한 LED 밝기 조절 프로그램

### 기본 구동 프로그램: led_pwm_duty.py
- LED의 R - GPIO 18핀(핀 12)을 출력 모드로 설정
- GPIO 18핀의 DutyCycle을 조절하여 LED 밝기 조절
- 빨간불이 0.1초 간격으로 밝아졌다가 dutycycle 100에서 2초 유지됨
- 빨간불이 0.1초 간격으로 어두워졌다가 꺼진 상태로 1초 유지됨

```python
import RPi.GPIO as GPIO
import time

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# LED 핀 설정
LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)

# PWM 인스턴스 생성 (주파수 1kHz)
pwm = None # PWM 객체를 미리 선언 (변수 초기화)
pwm = GPIO.PWM(LED_PIN, 10000)  # PWM 인스턴스 생성, 초기 주파수 10000Hz로 설정
pwm.start(0)  # DutyCycle 0으로 시작 (꺼진 상태), 초기 Duty Cycle을 0%로 설정하여 OFF 상태로 시작

try:
    while True:
        # 점점 밝아짐
        for dc in range(0, 101, 2):
            pwm.ChangeDutyCycle(dc)  # pwm.ChangeDutyCycle(%) → 전력 비율 조절
            print("밝아 짐", dc)
            time.sleep(0.1) # 0.1초 씩 밝기 변화
        time.sleep(2) # 2초 동안 밝은 상태 유지
        # 점점 어두워짐
        for dc in range(100, -1, -2):
            print("어두워 짐", dc)
            pwm.ChangeDutyCycle(dc)  # pwm.ChangeDutyCycle(%) → 전력 비율 조절
            time.sleep(0.1)  # 0.1초 씩 밝기 변화
        time.sleep(1)  # 1초 동안 어두운 상태 유지

except KeyboardInterrupt:
    # Ctrl+C 눌렀을 때 실행 종료
    pass  

finally:
    if pwm is not None:
        try:
            pwm.stop() # PWM 신호 출력을 완전히 중지함
        except:
            pass
        del pwm  # __del__ 호출 시 오류 방지, # PWM 객체 삭제
    GPIO.cleanup()
```

---

### 문제: RGB LED 색상 조합 제어 실습
- 3컬러 RGB LED는 아래와 같이 연결되어 있다.
  - 빨강: GPIO 18
  - 초록: GPIO 23
- PWM을 사용하여 빨강(R)과 초록(G) 색상의 듀티사이클을 조절한다.
- 색상은 주황 → 노랑 → 연두 → 갈색 순으로 서서히 변화한다.
  - R 100 고정 후 G 50→100 (주황→노랑)
  - G 100 고정 후 R 100→50 (노랑→연두)
  - R 50 고정 후 G 100→30 (연두→갈색)
  - G 30 고정 후 R 50→100 (갈색→주황) 
- 각 색상은 0.1초 간격으로 부드럽게 전환되도록 한다.
- 색상 전환은 무한 반복되도록 한다.

```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
R_PIN = 18
G_PIN = 23
GPIO.setup(R_PIN, GPIO.OUT)
GPIO.setup(G_PIN, GPIO.OUT)

pwm_r = None
pwm_g = None
pwm_r = GPIO.PWM(R_PIN, 1000)
pwm_g = GPIO.PWM(G_PIN, 1000)
pwm_r.start(0)
pwm_g.start(0)

try:
    while True:
        for g in range(50, 101, 5):      # 주황 → 노랑
            pwm_r.ChangeDutyCycle(100)
            pwm_g.ChangeDutyCycle(g)
            time.sleep(0.1)
        print("주황 -> 노랑")
        time.sleep(3)
        for r in range(100, 49, -5):     # 노랑 → 연두
            pwm_r.ChangeDutyCycle(r)
            pwm_g.ChangeDutyCycle(100)
            time.sleep(0.1)
        print("노랑 -> 연두")
        time.sleep(3)            
        for g in range(100, 29, -5):     # 연두 → 갈색
            pwm_r.ChangeDutyCycle(50)
            pwm_g.ChangeDutyCycle(g)
            time.sleep(0.1)
        print("연두 -> 갈색")
        time.sleep(3)  
        for r in range(50, 101, 5):      # 갈색 → 주황
            pwm_r.ChangeDutyCycle(r)
            pwm_g.ChangeDutyCycle(30)
            time.sleep(0.1)
        print("갈색 -> 주황")
        time.sleep(3)

except KeyboardInterrupt:
    # Ctrl+C 눌렀을 때 실행 종료
    pass        

finally:
    if pwm_r is not None:
        try:
            pwm_r.stop()
        except:
            pass
        del pwm_r  # __del__ 호출 시 오류 방지
    if pwm_g is not None:
        try:
            pwm_g.stop()
        except:
            pass
        del pwm_g  # __del__ 호출 시 오류 방지
    GPIO.cleanup()
```

또는는

```python
import RPi.GPIO as GPIO
import time

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# LED 핀 설정
Red_LED_PIN = 18
Green_LED_PIN = 23
GPIO.setup(Red_LED_PIN, GPIO.OUT)
GPIO.setup(Green_LED_PIN, GPIO.OUT)

# PWM 인스턴스 생성 (주파수 1kHz)
pwm_r = None # PWM 객체를 미리 선언 (변수 초기화)
pwm_g = None # PWM 객체를 미리 선언 (변수 초기화)
pwm_r = GPIO.PWM(Red_LED_PIN, 10000)  # PWM 인스턴스 생성, 초기 주파수 10000Hz로 설정
pwm_g = GPIO.PWM(Green_LED_PIN, 10000)  # PWM 인스턴스 생성, 초기 주파수 10000Hz로 설정
pwm_r.start(0)  # DutyCycle 0으로 시작 (꺼진 상태), 초기 Duty Cycle을 0%로 설정하여 OFF 상태로 시작
pwm_g.start(0)  # DutyCycle 0으로 시작 (꺼진 상태), 초기 Duty Cycle을 0%로 설정하여 OFF 상태로 시작

def change(pwm, start, end, step=2, delay=0.1): #step=2 부드럽게 전환
    # 밝아짐
    if start < end:
        for dc in range(start, end+1, step):
            pwm.ChangeDutyCycle(dc)
            time.sleep(delay) # 0.1초 간격 전환
    # 어두워짐
    else:
        for dc in range(start, end-1, -step):
            pwm.ChangeDutyCycle(dc)
            time.sleep(delay) # 0.1초 간격 전환

# 색상은 주황 → 노랑 → 연두 → 갈색 순으로 서서히 변화
try:
    while True: # 색상 전환 무한 반복
        pwm_r.ChangeDutyCycle(100) # R 100 고정
        change(pwm_g, 50, 100) # G 50->100(주황→노랑)
        print("주황->노랑")
        time.sleep(3) # 노란색 3초

        pwm_g.ChangeDutyCycle(100) # G 100 고정
        change(pwm_r, 100, 50) # R 100→50 (노랑→연두)
        print("노랑->연두")
        time.sleep(3) # 연두색 3초

        pwm_r.ChangeDutyCycle(50) # R 50 고정
        change(pwm_g, 100, 30) #G 100→30 (연두→갈색)
        print("연두->갈색")
        time.sleep(3) # 갈색 3초

        pwm_g.ChangeDutyCycle(30) # G 30 고정
        change(pwm_r, 50, 100) # R 50→100 (갈색→주황)
        print("갈색->주황")
        time.sleep(3) # 주황색 3초

except KeyboardInterrupt:
    # Ctrl+C 눌렀을 때 실행 종료
    pass  

finally:
    if pwm_r is not None:
        try:
            pwm_r.stop() # PWM 신호 출력을 완전히 중지함
        except:
            pass
        del pwm_r  # __del__ 호출 시 오류 방지
   
    if pwm_g is not None:
        try:
            pwm_g.stop() # PWM 신호 출력을 완전히 중지함
        except:
            pass
        del pwm_g  # __del__ 호출 시 오류 방지
    GPIO.cleanup()
```
