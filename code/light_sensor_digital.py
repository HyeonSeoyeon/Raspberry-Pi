import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정 (조도 센서의 DO 핀 연결)
SENSOR_PIN = 17  # GPIO 17 (핀 번호 11)

# GPIO 설정
GPIO.setmode(GPIO.BCM)  # GPIO 번호 모드를 BCM 모드로 설정
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 내부 풀다운 저항 사용
print('조도 센서 값 읽기 시작...')

try:
    while True:
        sensor_value = GPIO.input(SENSOR_PIN) # 지정된 GPIO 핀의 현재 값을 읽음.
        if sensor_value == GPIO.HIGH: # 값이 HIGH(1)이면 조도가 임계값을 미만
            print('조도가 낮습니다.')
        else:  # LOW(0)이면 임계값 이상임
            print('조도가 높습니다.')
        time.sleep(1)
        '''
        센서는 현재 조도 증가 → LOW, 조도 감소 → HIGH 출력
        조도가 없을 때, 즉 어두워 졌을 때 감지를 목표
        '''

except KeyboardInterrupt:
    print("프로그램 종료")
finally:
    GPIO.cleanup()