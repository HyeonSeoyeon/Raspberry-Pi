# 스위치를 이용한 3 Color LED 제어

### 준비물 & GPIO 연결
- YwRobot LED 버튼 액츄레이터 묘듈
  - 전원(VCC) : 5V Power (핀2)
  - 접지(GND) : Ground 접지 (핀14)
  - 신호(OUT) : GPIO 18 (핀12)
- SMD형 LED 액츄레이터 모듈
  - R : GPIO 27 (핀13)
  - G : GPIO 22 (핀15)
  - B : GPIO 17 (핀11)
  - - : Ground 접지 (핀14)
- ✅ GND 연결 정리
  - 1. 버튼의 GND → 브레드보드 GND(-) 레일에 연결
  - 2. LED의 음극(-) → 브레드보드 GND(-) 레일에 연결
  - 3. 브레드보드 GND(-) 레일 → Raspberry Pi GND (핀 14)와 연결
  - 즉, 브레드보드 GND(-) 레일이 Raspberry Pi의 GND(핀 14)와 연결되므로, 버튼과 LED의 GND도 자연스럽게 Raspberry Pi GND에 연결되는 구조가 됩니다.
 

### 프로그램의 주요 동작 흐름
1. 처음 실행하면 모든 LED가 꺼진 상태
2. 버튼을 누르면 색상이 변경됨 (파란색 → 초록색 → 빨간색 → 다시 파란색...)
3. 버튼을 1초 이상 길게 누르면 LED가 꺼짐
4. 다시 짧게 누르면 파란색부터 반복 시작

```python
import RPi.GPIO as GPIO
import time

# 핀 번호 설정
BUTTON_PIN = 18  # 버튼이 연결될 GPIO 핀 번호 (LED 버튼의 OUT)
RED_PIN = 27
GREEN_PIN = 22
BLUE_PIN = 17

# 글로벌 변수
led_state = 0  # LED 상태 (0: 모두 꺼짐, 1: 파란색, 2: 초록색, 3: 빨간색)

# GPIO 설정 함수
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 버튼이 눌리지 않은 상태가 high 신호, 버튼을 눌린 상태가 low 신호 (high 신호로 시작)
    GPIO.setup(BLUE_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(RED_PIN, GPIO.OUT)

# 모든 LED 끄는 함수 (이걸 안 하려면 위의 setup()에서 initial=GPIO.LOW로 해주면 된다.)
def turn_off_leds():
    global led_state # 지역변수
    led_state = 0
    GPIO.output(BLUE_PIN, GPIO.LOW) # 끄기
    GPIO.output(GREEN_PIN, GPIO.LOW) # 끄기
    GPIO.output(RED_PIN, GPIO.LOW) # 끄기

# LED 상태 변경 함수
def change_led_state():
    global led_state # 지역변수
    led_state += 1
    if led_state > 3:
        led_state = 1 # 다시 파란색으로 돌아옴
    if led_state == 1: # 파
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.LOW)
    elif led_state == 2: # 초
        GPIO.output(BLUE_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(RED_PIN, GPIO.LOW)
    elif led_state == 3: # 빨
        GPIO.output(BLUE_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.HIGH)

# 버튼 이벤트 콜백 함수
def button_callback(channel):
    start_time = time.time() # time.time()은 현재의 second 타임을 제공

    # 버튼이 눌린 상태 유지 확인
    while GPIO.input(BUTTON_PIN) == GPIO.LOW:
        # 눌린 상태는 LOW, 뗀 상태는 HIGH
        # 버튼이 눌린 상태이면 무한반복 -> 버튼이 뗀 상태이면 반복문 빠짐
        # GPIO.FALLING 상태로 눌린 순간 이벤트가 발생하지만 GPIO.RISING 처럼 움직임(버튼을 뗀 순간 다음 로직 실행).
        time.sleep(0.01)  # 디바운싱 대기

    button_press_duration = time.time() - start_time # 누른 시간을 빼기로 계산
    if button_press_duration >= 1:  # 1초 이상 누르면 LED 끄기
        turn_off_leds() # 모든 LED 끄느 함수수
    else:  # 짧게 누르면 LED 색상 변경
        change_led_state() # LED 상태 변경 함수

# GPIO 종료 함수
def cleanup_gpio():
    GPIO.cleanup()

# 메인 함수
def main():
    setup_gpio()
    # 프로그램 시작 시 모든 LED 끄기
    turn_off_leds()
    # 버튼 이벤트 감지 설정
    # GPIO.FALLING 는 누르는 순간(LOW) 이벤트 발생
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)
    # GPIO 18번 핀(BUTTON_PIN)에 Falliing 이벤트가 붙는다.
    # GPIO.FALLING은 high(안누름)에서 low(누름)가 되면 이벤트를 발생시켜라는 뜻.
    # 이벤트가 감지될 때 콜백 함수가 실행된다.
    # bouncetime은 이벤트 콜백 호출 사이에 적용될 디바운스(신호안정) 시간(밀리초 단위)이다.

    try:
        while True: # 프로그램적으로 자동으로 종료되지 않기 위해서 무한반복
            time.sleep(0.1) 
    except KeyboardInterrupt: # 키보드 인터럽트가 발생될 경우(^C) finally가 발생하여 gpio를 cleanup해줌.
        pass
    finally:
        cleanup_gpio()

# 실행 진입점
if __name__ == "__main__":
    main()
```

---

### <mark>GPIO.add_event_detect()</mark>
- GPIO 핀에 이벤트 감지(callback) 기능을 추가하는 데 사용된다.
- 특정 핀의 상태 변경(예: <mark>라이징 엣지, 폴링 엣지)을 비동기적</mark>으로 감지한다.
- 변경이 감지될 때마다 지정된 <mark>콜백 함수를 자동으로 호출</mark>할 수 있다.
```
GPIO.add_event_detect(버튼 핀 번호, 폴링 또는 엣지, callback=함수, bouncetime은 선택적)
```
- channel: int형, 이벤트 감지를 추가할 GPIO 핀의 번호.
- GPIO.RISING, GPIO.FALLING, GPIO.BOTH:	감지할 이벤트의 종류를 지정.
  - RISING: 0에서 1로의 변화 (GPIO 핀의 신호가 LOW에서 HIGH로 변할 때)
    - GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 일 때, 버튼을 누르면 LOW->HIGH 변할 시의 이벤트 종류 지정 가능
  - FALLING: 1에서 0으로의 변화 (GPIO 핀의 신호가 HIGH에서 LOW로 변할 때)
    - GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 일 때, 버튼을 누르면 HIGH->LOW 변할 시의 이벤트 종류 지정 가능
  - BOTH: 둘 다 감지. (GPIO 핀의 신호가 변화할 때(LOW에서 HIGH 또는 HIGH에서 LOW)
- callback: function, 이벤트가 감지될 때 호출될 콜백 함수.
- bouncetime: int형, 선택적, 이벤트 콜백 호출 사이에 적용될 디바운스(신호안정) 시간(밀리초 단위).

### 스위치 제어 프로그램 정리
1. 핀 번호 설정
2. GPIO 설정 함수
3. 모든 LED 끄는 함수, LED 상태 변경 함수, 버튼 이벤트 콜백 함수
4. GPIO 종료 함수
5. 메인 함수 (GPIO 설정, 시작 시 LED 끄기, 버튼 이벤트 감지 설정, 프로그램 정상 종료 등)
6. 실행 진입점

---

## 문제: RGB LED 색상 조합 제어 실습
- 하나의 공통형 RGB LED를 사용하여, 버튼을 누를 때마다 LED 색상이 아래 순서대로 변경되도록 하시오.
- 3_color_led_switch_ranibow.py 파일 생성
- 버튼 누를 때마다 색상 변경 순서
1. 빨강
2. 초록
3. 파랑
4. 노랑
5. 하늘
6. 보라
7. 흰색
8. OFF
- 버튼은 짧게 누를 때만 반응, 길게 눌렀을 때는 무시.
- 버튼은 GPIO.FALLING 이벤트로 감지.
- LED 색의 정보는 배열을 0~7 활용함.

### 아이디어

```python
import RPi.GPIO as GPIO
import time
# 핀 설정
BUTTON_PIN = 18
RED_PIN = 27
GREEN_PIN = 22
BLUE_PIN = 17

# 상태 변수
led_state = 0  # 0: OFF, 1~7: 색 조합
# GPIO 설정
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RED_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(GREEN_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(BLUE_PIN, GPIO.OUT, initial=GPIO.LOW)
# LED 색상 설정
def set_color(state):
    colors = (
        (0, 0, 0),  # off
        (1, 0, 0),  # 빨강
        (0, 1, 0),  # 초록
        (0, 0, 1),  # 파랑
        (1, 1, 0),  # 노랑
        (0, 1, 1),  # 하늘
        (1, 0, 1),  # 보라
        (1, 1, 1),  # 흰색
    )
    r, g, b = colors[state]
    #GPIO.output(RED_PIN, GPIO.HIGH if r else GPIO.LOW) # r == 1 ? GPIO.HIGH : GPIO.LOW
    #GPIO.output(GREEN_PIN, GPIO.HIGH if g else GPIO.LOW)
    #GPIO.output(BLUE_PIN, GPIO.HIGH if b else GPIO.LOW)
    #GPIO.output(RED_PIN, r) # r == 1 ? GPIO.HIGH : GPIO.LOW
    #GPIO.output(GREEN_PIN, g)
    #GPIO.output(BLUE_PIN, b)
    GPIO.output([RED_PIN, GREEN_PIN, BLUE_PIN], [r,g,b])

# 버튼 콜백
def button_callback(channel):
    global led_state
    start = time.time()
    while GPIO.input(BUTTON_PIN) == GPIO.LOW:
        time.sleep(0.01)
    duration = time.time() - start
    if duration < 1:
        led_state += 1
        if led_state > 7:
            led_state = 0
        set_color(led_state)
# 메인
def main():
    setup_gpio()
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
if __name__ == "__main__":
    main()
```

---
