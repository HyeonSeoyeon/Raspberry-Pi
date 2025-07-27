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