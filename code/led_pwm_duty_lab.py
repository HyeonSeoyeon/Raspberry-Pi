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









