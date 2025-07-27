from flask import Flask
from flask_socketio import SocketIO
from flask import request

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    from mockgpio import GPIO  # 인스턴스를 직접 가져옴

# GPIO 초기화
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Flask 및 SocketIO 설정
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# 현재 LED 상태 반환 함수
def get_led_state():
    return "on" if GPIO.input(LED_PIN) else "off"

# 클라이언트로부터 제어 요청 수신
@socketio.on("led_control")
def control_led(data):
    state = data.get("state")
    if state == "on":
        GPIO.output(LED_PIN, GPIO.HIGH)
    elif state == "off":
        GPIO.output(LED_PIN, GPIO.LOW)
    # 상태 응답
    state = get_led_state()
    print(f"led 상태 : {state}")
    socketio.emit("led_status", {"state": state}) # 브로드캐스트
    #socketio.emit("led_status", {"state": state}, room=request.sid) # 유니캐스트

# 초기 상태 요청 처리
@socketio.on("get_led_status")
def handle_status_request():
    state = get_led_state()
    print(f"led 상태 : { get_led_state()}")
    socketio.emit("led_status", {"state": state}) # client 응답

# 서버 실행
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
