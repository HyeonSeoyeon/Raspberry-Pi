import time             # 시간 관련 함수 (예: time.sleep) 사용
import threading        # 백그라운드에서 센서 데이터를 읽기 위한 스레드 사용
from flask import Flask, request # 웹 서버 구축을 위한 Flask
from flask_socketio import SocketIO # 실시간 양방향 통신을 위한 Flask-SocketIO
import RPi.GPIO as GPIO # 라즈베리파이 GPIO 핀 제어
import board            # Adafruit Blinka 라이브러리에서 보드 핀 정의 임포트
import adafruit_dht     # DHT 온습도 센서 라이브러리

# --- 글로벌 변수 ---
# DHT22 센서로부터 읽은 최신 온도와 습도 값을 저장하는 전역 변수
latest_temp = None
latest_hum = None

# --- GPIO 설정 ---
BLUE_PIN = 17           # 파란색 LED가 연결된 라즈베리파이 GPIO 핀 번호 (BCM 모드)
RED_PIN = 24            # 빨간색 LED가 연결된 라즈베리파이 GPIO 핀 번호 (BCM 모드)
GPIO.setmode(GPIO.BCM)  # GPIO 핀 번호 체계를 BCM 모드로 설정
GPIO.setup(BLUE_PIN, GPIO.OUT) # 파란색 LED 핀을 출력 모드로 설정
GPIO.setup(RED_PIN, GPIO.OUT)  # 빨간색 LED 핀을 출력 모드로 설정

# --- LED 상태 저장용 변수 ---
# 웹에서 LED 제어가 'ON' 상태일 때 True, 'OFF'일 때 False
# 이 변수가 True여야만 온도에 따른 LED 자동 제어가 작동합니다.
led_enabled = False

# --- Flask-SocketIO 설정 ---
app = Flask(__name__)   # Flask 애플리케이션 인스턴스 생성
# SocketIO 객체 생성: Flask 앱과 연결하고, 모든 출처(origins)에서의 접속을 허용하며,
# 'eventlet' 비동기 모드를 사용하여 높은 동시성을 지원합니다.
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# --- DHT22 센서 설정 ---
# DHT22 센서 객체 생성. 데이터 핀은 라즈베리파이 GPIO 18번 핀에 연결되어 있다고 가정합니다.
dht_device = adafruit_dht.DHT22(board.D18)

# --- Socket.IO 이벤트 핸들러: LED 제어 ---
# 클라이언트로부터 'led_control' 이벤트를 수신했을 때 실행됩니다.
@socketio.on("led_control")
def control_led(data):
    global led_enabled  # 전역 변수 led_enabled를 수정하기 위해 global 키워드 사용
    state = data.get("state") # 수신된 데이터에서 'state' 값을 가져옵니다.

    if state == "on":
        led_enabled = True  # LED 자동 제어 활성화
    elif state == "off":
        led_enabled = False # LED 자동 제어 비활성화
        # LED를 'OFF'하면, 현재 켜져 있던 모든 LED를 강제로 끕니다.
        GPIO.output(BLUE_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.LOW)
    
    # 현재 LED 제어 모드 상태를 클라이언트에 전송합니다.
    current_mode_state = "on" if led_enabled else "off"
    print(f"LED 제어 모드 상태 : {current_mode_state}") # 서버 콘솔에 상태 출력
    # 'led_status' 이벤트를 모든 연결된 클라이언트에게 브로드캐스트합니다.
    socketio.emit("led_status", {"state": current_mode_state})

# --- Socket.IO 이벤트 핸들러: LED 상태 요청 처리 ---
# 클라이언트로부터 'get_led_status' 이벤트를 수신했을 때 실행됩니다.
@socketio.on("get_led_status")
def handle_status_request():
    # 현재 LED 제어 모드 상태(led_enabled)를 기반으로 "on" 또는 "off"를 결정합니다.
    state = "on" if led_enabled else "off"
    print(f"클라이언트 요청: LED 제어 모드 상태 반환 - {state}") # 서버 콘솔에 요청 및 상태 출력
    # 요청한 특정 클라이언트에게만 'led_status' 이벤트를 전송합니다 (유니캐스트).
    socketio.emit("led_status", {"state": state}, room=request.sid)

# --- Socket.IO 이벤트 핸들러: 온습도 상태 요청 처리 (유니캐스트) ---
# 클라이언트로부터 'get_temperature_humidity_status' 이벤트를 수신했을 때 실행됩니다.
@socketio.on("get_temperature_humidity_status")
def send_temperature_humidity_status():
    # 전역 변수에 최신 온습도 데이터가 있으면 해당 데이터를 클라이언트에 전송합니다.
    if latest_temp is not None and latest_hum is not None:
        socketio.emit("temperature_humidity_status", {
            "temp": latest_temp,
            "hum": latest_hum
        }, room=request.sid) # 요청한 클라이언트에게만 전송 (유니캐스트)
    else:
        # 데이터가 아직 없으면 "N/A" (Not Available)를 전송합니다.
        socketio.emit("temperature_humidity_status", {
            "temp": "N/A",
            "hum": "N/A"
        }, room=request.sid)

# --- 센서 측정 및 LED 자동 제어 스레드 함수 ---
# 백그라운드에서 주기적으로 DHT22 센서 데이터를 읽고, 온도에 따라 LED를 제어합니다.
def temperature_monitor_thread():
    global latest_temp, latest_hum # 전역 변수를 수정하기 위해 global 키워드 사용
    while True: # 무한 루프를 돌며 계속 센서 값을 읽고 LED를 제어합니다.
        try:
            temp = dht_device.temperature # 센서에서 온도 읽기
            hum = dht_device.humidity     # 센서에서 습도 읽기
            if hum is not None and temp is not None:
                latest_temp = round(temp, 1) # 온도를 소수점 첫째 자리까지 반올림
                latest_hum = round(hum, 1)   # 습도를 소수점 첫째 자리까지 반올림
                print(f"센서 측정: {latest_temp}℃ / {latest_hum}%") # 콘솔에 측정값 출력

                # RGB LED 자동 제어 로직: led_enabled가 True일 때만 작동
                if led_enabled: # 웹에서 'ON' 상태로 설정되어 있을 때만 자동 제어
                    if latest_temp >= 27:
                        # 온도가 27도 이상이면 빨간색 LED 켜고 파란색 LED 끄기 (더움 표시)
                        GPIO.output(RED_PIN, GPIO.HIGH)
                        GPIO.output(BLUE_PIN, GPIO.LOW)
                    else:
                        # 온도가 27도 미만이면 빨간색 LED 끄고 파란색 LED 켜기 (정상/시원함 표시)
                        GPIO.output(RED_PIN, GPIO.LOW)
                        GPIO.output(BLUE_PIN, GPIO.HIGH)
                # led_enabled가 False이면 이 if 블록은 건너뛰고, control_led 함수에서 이미 LED가 꺼졌을 것입니다.
            else:
                print("센서 데이터 없음: 유효한 데이터를 읽지 못했습니다.")
        except RuntimeError as e:
            # 센서 읽기 오류 (예: CRC 에러, 타임아웃) 발생 시 오류 메시지 출력
            print(f"센서 에러: {e.args[0]}")
        except Exception as e:
            # 기타 예상치 못한 오류 발생 시 DHT 장치 종료 및 예외 다시 발생 (프로그램 종료)
            dht_device.exit()
            raise e
        time.sleep(2) # 2초마다 센서 값을 다시 읽도록 대기

# --- 센서 측정 스레드 시작 함수 ---
# `temperature_monitor_thread` 함수를 새로운 스레드에서 실행합니다.
def start_sensor_thread():
    t = threading.Thread(target=temperature_monitor_thread) # 새로운 스레드 객체 생성
    # 데몬 스레드 설정: 메인 프로그램이 종료되면 이 스레드도 함께 종료됩니다.
    # 이 경우 메인 프로그램(Flask 서버)은 계속 실행되므로 필수는 아니지만, 명시적으로 설정할 수 있습니다.
    t.daemon = True
    t.start() # 스레드 실행 시작 (temperature_monitor_thread 함수가 백그라운드에서 동작)

# --- 메인 실행 블록 ---
if __name__ == "__main__":
    print("서버 시작 중...")
    # 센서 모니터링 및 LED 자동 제어 스레드를 시작합니다.
    start_sensor_thread()
    # Flask-SocketIO 애플리케이션을 실행합니다.
    # host="0.0.0.0"은 모든 IP 주소에서 접속을 허용합니다.
    # port=5000은 5000번 포트로 서버를 엽니다.
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
    # `allow_unsafe_werkzeug=True`는 개발 서버에서 HTTPS 없이도 Socket.IO를 사용할 때 뜨는 경고를 제거합니다.
    # 프로덕션 환경에서는 WSGI 서버(Gunicorn 등)와 함께 사용하는 것이 좋습니다.
    # 프로그램이 종료될 때까지 Flask 서버는 계속 실행되며 클라이언트 요청을 대기합니다.