
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

