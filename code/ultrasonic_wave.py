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
    GPIO.output(TRIG, GPIO.LOW) # TRIG 핀을 False(0V)로 설정해 초기화. 측정 전에 트리거 핀을 정리
    time.sleep(0.5) # 이전 측정의 잔여 신호에서 완전히 안정화되기 위한 대기 시간

    # 신호 송신부에서 40kHz 신호 8개 송신(200µs 동안)
    GPIO.output(TRIG, GPIO.HIGH) # TRIG 핀을 True(3.3V 또는 5V)로 설정해 트리거 핀에 10μs(0.00001초) 동안의 고전압 신호를 보낸다. 초음파 파동을 발생한다
    time.sleep(0.00001) # 초음파 펄스를 발생시키기 위한 대기시간. 10μs시간 동안의 펄스는 센서로 하여금 충분한 에너지를 가진 초음파 파동을 발생
    GPIO.output(TRIG, GPIO.LOW) # TRIG 핀을 다시 False로 설정해 트리거 신호를 종료

    # 초음파 파동이 발사되고 반사되어 돌아온 첫 신호와 마지막 신호의 시간 측정
    while GPIO.input(ECHO) == GPIO.LOW:  # ECHO 핀이 HIGH 상태로 전환되기를 기다림
        pulse_start = time.time()  # 초음파 펄스가 ECHO에 처음 도착한 시간 기록
    while GPIO.input(ECHO) == GPIO.HIGH:  #  ECHO 핀이 LOW 상태로 돌아갈 때까지 기다림
        pulse_end = time.time()  # 초음파 펄스 ECHO에 마지막 도착한 시간 기록

    pulse_duration = pulse_end - pulse_start  # 초음파 파동이 발사되어 돌아오는 데 걸린 전체 시간을 계산
    distance = pulse_duration * (34300 / 2) # 소리속도 34300 cm/s
    distance = round(distance, 2)  # 거리를 소수점 둘째 자리까지 반올림
    return distance

try:
    while True:
        dist = get_distance()
        print("Distance:", dist, "cm")

        if dist > 100: # 최대 99로 제한
            dist = 99

        pwm.ChangeDutyCycle(dist) # 측정된 거리 → 밝기(Duty Cycle)로 변환
        time.sleep(0.1)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()