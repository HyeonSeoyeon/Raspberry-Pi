```py
import RPi.GPIO as GPIO
import time

# 핀 번호 설정
BLUE_PIN = 17
GREEN_PIN = 22
RED_PIN = 27

# GPIO 핀의 번호 모드 설정 및 LED 핀의 모드를 출력으로 설정
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BLUE_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(RED_PIN, GPIO.OUT)

# GPIO 설정 초기화
def cleanup_gpio():
    GPIO.cleanup()

# LED를 순차적으로 켜고 끄는 함수
def cycle_leds():
    # 파란색 LED 켜기
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(BLUE_PIN, GPIO.LOW)
   
    # 초록색 LED 켜기
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(GREEN_PIN, GPIO.LOW)
   
    # 빨간색 LED 켜기
    GPIO.output(RED_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(RED_PIN, GPIO.LOW)

# 메인 프로그램
def main():
    setup_gpio()
    try:
        while True:
            cycle_leds()
    except KeyboardInterrupt:
        # Ctrl+C 눌렀을 때 실행 종료
        pass
    finally:
        cleanup_gpio()  # GPIO 설정 초기화

# 실행 진입점
if __name__ == "__main__":
    main()
```
