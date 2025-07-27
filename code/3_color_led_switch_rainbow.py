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