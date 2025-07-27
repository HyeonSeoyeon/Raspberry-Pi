import time
import threading
from flask import Flask, request
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
import board
import adafruit_dht

# --- 글로벌 변수 ---
latest_temp = None
latest_hum = None

# --- GPIO 설정 ---
BLUE_PIN = 17  # 파랑
RED_PIN = 24   # 빨강
GPIO.setmode(GPIO.BCM)
GPIO.setup(BLUE_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)

# --- LED 상태 저장용 변수 ---
led_enabled = False  # 웹에서 ON일 때 True

# --- Flask-SocketIO 설정 ---
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# --- DHT22 센서 설정 ---
dht_device = adafruit_dht.DHT22(board.D18)

# --- LED 제어 처리 ---
@socketio.on("led_control")
def control_led(data):
    global led_enabled
    state = data.get("state")
    if state == "on":
        led_enabled = True
    elif state == "off":
        led_enabled = False
        GPIO.output(BLUE_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.LOW)
    
    state = "on" if led_enabled else "off"
    print(f"led 상태 : {state}")
    socketio.emit("led_status", {"state": state})

# --- LED 상태 요청 처리 ---
@socketio.on("get_led_status")
def handle_status_request():
    state = "on" if led_enabled else "off"
    print(f"led 상태 : {state}")
    socketio.emit("led_status", {"state": state}, room=request.sid)

# --- 온습도 상태 요청 처리 (유니캐스트) ---
@socketio.on("get_temperature_humidity_status")
def send_temperature_humidity_status():
    if latest_temp is not None and latest_hum is not None:
        socketio.emit("temperature_humidity_status", {
            "temp": latest_temp,
            "hum": latest_hum
        }, room=request.sid)
    else:
        socketio.emit("temperature_humidity_status", {
            "temp": "N/A",
            "hum": "N/A"
        }, room=request.sid)

# --- 센서 측정 스레드 ---
def temperature_monitor_thread():
    global latest_temp, latest_hum
    while True:
        try:
            temp = dht_device.temperature
            hum = dht_device.humidity
            if hum is not None and temp is not None:
                latest_temp = round(temp, 1)
                latest_hum = round(hum, 1)
                print(f"센서 측정: {latest_temp}℃ / {latest_hum}%")

                # RGB LED 자동 제어 로직
                if led_enabled:
                    if latest_temp >= 27:
                        GPIO.output(RED_PIN, GPIO.HIGH)
                        GPIO.output(BLUE_PIN, GPIO.LOW)
                    else:
                        GPIO.output(RED_PIN, GPIO.LOW)
                        GPIO.output(BLUE_PIN, GPIO.HIGH)
            else:
                print("센서 데이터 없음")
        except RuntimeError as e:
            print("센서 에러:", e.args[0])
        except Exception as e:
            dht_device.exit()
            raise e
        time.sleep(2)

# --- 센서 스레드 시작 ---
def start_sensor_thread():
    t = threading.Thread(target=temperature_monitor_thread) # 쓰레드 만들기
    t.daemon = True # 안해도 됩니다 (조건에 의해서 메인이 죽을 일이 없어서)
    t.start() # 쓰레드 시작 -> 무한반복 (프로그램 죽을때까지)

# --- 메인 ---
if __name__ == "__main__":
    print("서버 시작")
    start_sensor_thread()
    socketio.run(app, host="0.0.0.0", port=5000)