import spidev  # SPI 통신을 위한 spidev 라이브러리 임포트
import time    # 시간 관련 함수를 위한 time 라이브러리 임포트

# SPI 초기화
spi = spidev.SpiDev() # SpiDev 객체 생성
spi.open(0, 0)        # SPI 버스 0, CE0 (Chip Enable 0)을 사용하여 SPI 통신 오픈
spi.max_speed_hz = 1000000 # SPI 통신 속도를 1MHz로 설정
spi.mode = 0          # SPI 모드를 0으로 설정 (CPOL=0, CPHA=0)

# MCP3208 아날로그-디지털 컨버터(ADC)로부터 아날로그 데이터를 읽는 함수 (0~7 채널)
def read_adc(channel):
    # 유효한 채널 범위(0-7)를 벗어나면 -1 반환
    if not 0 <= channel <= 7:
        return -1

    # MCP3208 아날로그 값을 읽기 위한 명령 바이트 구성
    # 시작 비트(Start Bit)는 1로 설정
    # 단일 엔드 모드(Single-Ended Mode)는 1로 설정 (Differential Mode는 0)
    # 채널 비트의 최상위 1비트(D2)를 포함
    cmd1 = 0b00000110  # 예: 단일 입력 모드로 CH0 채널을 읽기 위한 명령의 첫 부분

    # 나머지 채널 비트 D1, D0을 구성하고 상위 6비트로 이동 (쉬프트)
    # (channel & 0x07)은 channel 값을 0~7 범위로 마스크하여 필요한 3비트만 추출
    cmd2 = (channel & 0x07) << 6 # 예: CH0의 경우 0b00000000이 되고, << 6하면 0b00000000이 됨

    # SPI 통신을 통해 3바이트를 전송하고 3바이트를 수신
    # 첫 번째 바이트: 명령의 첫 부분 (시작 비트, 모드, 채널 D2)
    # 두 번째 바이트: 명령의 두 번째 부분 (채널 D1, D0)
    # 세 번째 바이트: 더미 바이트 (데이터를 수신하기 위해 필요)
    adc = spi.xfer2([cmd1, cmd2, 0]) # 예: CH0을 읽으려면 [0b00000110, 0b00000000, 0b00000000] 전송
    print(f"Raw SPI response: {adc}") # SPI 응답의 원시 바이트 값 출력 (디버깅 용도)

    # 수신된 12비트 ADC 데이터를 조합
    # adc[1]의 하위 4비트(0x0F)와 adc[2]의 8비트를 사용하여 12비트 값을 만듦
    # adc[1]의 하위 4비트를 8비트 왼쪽으로 쉬프트하여 상위 4비트를 구성하고, adc[2]와 비트 OR 연산
    data = ((adc[1] & 0x0F) << 8) | adc[2]
    '''
    데이터 조합 과정 예시:
    adc[1] (예: 0b10101100) & 0x0F (0b00001111) = 0b00001100 (12, 10진수)
    0b00001100 << 8 = 0b00001100_00000000 (3072, 10진수)
    여기에 adc[2] (예: 0b11110000)를 비트 OR 연산하면
    결과: 0b00001100_11110000 (3312, 10진수)
    '''
    return data

try:
    print("조도센서 값 읽기 시작...")
    print("Ctrl+C로 종료")

    while True:
        # MCP3208의 0번 채널에서 조도 센서 값 읽기
        value = read_adc(0)
        # ADC 값(0-4095)을 전압 값으로 변환 (VREF=5V 기준)
        # 12비트 ADC는 0부터 4095까지의 값을 가짐 (2^12 - 1)
        voltage = value * 5.0 / 4095

        # 읽어온 조도 값과 계산된 전압 출력
        print(f"조도 값: {value}, 전압: {voltage:.2f}V")
        print("-" * 50) # 구분선 출력

        time.sleep(1) # 1초 대기 후 다시 값 읽기
except KeyboardInterrupt:
    # Ctrl+C 입력 시 프로그램 종료 메시지 출력
    print("\n프로그램 종료")
finally:
    # 프로그램 종료 시 SPI 연결 해제 (자원 반환)
    spi.close()
    print("SPI 연결 종료")