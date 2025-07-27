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