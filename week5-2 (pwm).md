## <mark>PWM(Pulse Width Modulation, 펄스폭 변조)</mark>
- <mark>**디지털 핀에서 출력 신호의 ON/OFF 비율을 조절하여 아날로그처럼 동작하게 하는 방식**</mark>
- 전압을 **0V 또는 5V(3.3V)로만 출력하는 디지털 신호를 이용해, 평균 전압을 조절하는 기법**
- **부저 소리 제어, LED 밝기 조절, 모터 속도 조절 등에 사용됨**

---

## `pwm = None` → 변수 초기화
- Python에서 변수를 미리 선언하고 싶을 때 None을 할당
```python
pwm = None  # PWM 객체를 미리 선언
```

## `pwm = GPIO.PWM(BUZZER_PIN, 100)` → PWM 객체 생성
```python
pwm = GPIO.PWM(BUZZER_PIN, 100)  # PWM 인스턴스 생성, 초기 주파수 100Hz로 설정
```

## `pwm.start(0)` → PWM 시작하는 함수
- start(0)의 0은 초기 Duty Cycle(%)을 설정하는 값으로, 0이면 처음에는 OFF 상태.
- 이후 ChangeDutyCycle()을 호출하면 PWM 신호가 출력됨.
```python
pwm.start(0)  # 초기 Duty Cycle을 0%로 설정하여 OFF 상태로 시작
```

---

## <mark>`pwm.ChangeFrequency(Hz)` → 주파수 조절</mark>
- <mark>**1초 동안 반복되는 PWM 신호의 주파수(Hz)를 설정**</mark>
```python
pwm.ChangeFrequency(261.63)  # C4 음을 출력
```

---

## <mark>`pwm.ChangeDutyCycle(%)` → ON/OFF 비율 조절</mark>
- <mark>**Duty Cycle(%)**: 한 주기에서 **HIGH(ON) 상태가 차지하는 비율**</mark>
- 소리, 밝기, 전력 조절 등에 사용됨
- 50%면 ON/OFF 비율이 1:1, 75%면 High:Low 비율이 3:1
- 듀티 사이클을 조절하면 음색이 미세하게 달라진다.
  - 10%는 얇고 날카로운 소리
  - 90%는 두껍고 탁한 소리
```python
pwm.ChangeDutyCycle(50)  # ON:OFF = 1:1 (켜짐)
pwm.ChangeDutyCycle(0)   # ON:OFF = 0:1 (꺼짐, 진동하지 않음)
pwm.ChangeDutyCycle(100) # ON:OFF = 1:0 (항상 HIGH, 진동하지 않음)
```

---

## PWM을 활용한 부저 소리 예제
```python
pwm.ChangeFrequency(440)  # 440Hz → 1초에 440번 진동
pwm.ChangeDutyCycle(50)   # ON:OFF 비율 1:1 → 1초 동안 HIGH 220번, LOW 220번 진동
time.sleep(1.0)           # 1초 동안 소리 유지
pwm.ChangeDutyCycle(0)    # 소리를 끔
```

---

## `pwm.stop()` → PWM 중지
- PWM 출력을 중지하는 함수.
- 부저나 LED 등 PWM을 이용한 출력 장치를 끌 때 사용됨.
```python
pwm.stop()  # PWM 신호 출력을 완전히 중지함
```

## `del pwm` → PWM 객체 삭제
- del pwm은 변수 자체를 삭제하는 Python의 명령어.
- pwm 객체를 삭제하여 이후 pwm을 참조하려고 하면 오류가 발생함.
```python
del pwm  # PWM 객체 삭제
```
📌 **주의:** `del pwm`은 필수는 아니며, `pwm.stop()`만 해도 충분한 경우가 많음.

---

## <mark>PWM으로 할 수 있는 것 (시험에 나올 수 있다!)</mark>

### <mark>1️⃣ 주파수 조절 → 부저 음정 제어 가능 🎵</mark>
```python
pwm.ChangeFrequency(440)  # A4 (440Hz)
pwm.ChangeFrequency(261.63)  # C4 (261.63Hz)
```

### <mark>2️⃣ Duty Cycle 조절 → 평균 전력 조절 -> LED 밝기 조절 가능 💡</mark>
```python
pwm.ChangeDutyCycle(10)  # 어두운 LED
pwm.ChangeDutyCycle(50)  # 중간 밝기
pwm.ChangeDutyCycle(90)  # 밝은 LED
```

---

## 추가 팁
✅ **부저 소리를 끄는 방법**
```python
pwm.ChangeDutyCycle(0)  # 진동을 멈춰서 소리를 끔
pwm.stop()  # PWM 자체를 중지
```

✅ **PWM을 완전히 종료할 때**
```python
pwm.stop()  # PWM 중지
GPIO.cleanup()  # GPIO 핀 정리
```

---

## <mark>PWM에서 LED 밝기 조절 공식</mark>
```
공급 전압 Vsupply = 5V, LED 순방향 전압 VLED = 3V, 저항 R = 220Ω, 듀티사이클 80%
```
- 듀티 사이클이 80%이면, 5V*0.8=4V 만큼의 전압으로 HIGH를 보냄.
- LED는 3V 이상의 전압이 들어와야 한다고 보고, LED가 가지고 있는 순수 저항을 220옴이라고 보면, 순간 전류, 평균 전류, 평균 전력이 계산된다.
- 1. <mark>순간 전류 (옴의 법칙): ```I(A) = (Vsupply − VLED) / R = (5 − 3) / 220 = 0.00909A = 9.09mA```</mark>
- 2. <mark>평균 전류 (옴의 법칙 × 듀티사이클): ```Iavg = 9.09mA × 0.8 = 7.27mA```</mark>
- 3. <mark>평균 전력 (전압 × 평균 전류): ```P = 2V × 7.27mA = 14.54mW```</mark>
- Duty Cicle에 따른 전류 및 전력 계산
| 듀티사이클 (%) | 순간 전류 (mA) I = (5V−3V)/220Ω | 평균 전류 (mA) Iavg = I × 듀티 | 평균 전력 (mW) P = 2V × Iavg |
|--------------|----------------------------|-------------------------|-------------------------|
| 10%          | 9.09                       | 9.09 × 0.1 = 0.91       | 2 × 0.91 = 1.82         |
| 20%          | 9.09                       | 9.09 × 0.2 = 1.82       | 2 × 1.82 = 3.64         |
| 30%          | 9.09                       | 9.09 × 0.3 = 2.73       | 2 × 2.73 = 5.45         |
| 40%          | 9.09                       | 9.09 × 0.4 = 3.64       | 2 × 3.64 = 7.27         |
| 50%          | 9.09                       | 9.09 × 0.5 = 4.55       | 2 × 4.55 = 9.09         |
| 60%          | 9.09                       | 9.09 × 0.6 = 5.45       | 2 × 5.45 = 10.91        |
| 70%          | 9.09                       | 9.09 × 0.7 = 6.36       | 2 × 6.36 = 12.73        |
| 80%          | 9.09                       | 9.09 × 0.8 = 7.27       | 2 × 7.27 = 14.54        |
| 90%          | 9.09                       | 9.09 × 0.9 = 8.18       | 2 × 8.18 = 16.36        |
| 100%         | 9.09                       | 9.09 × 1.0 = 9.09       | 2 × 9.09 = 18.18        |


## 소리의 원리
| 항목         | 설명 |
|-------------|--------------------------------|
| 진동수 (Hz) | 초당 공기의 압력이 몇 번 변화하는가 |
| 주파수 ↑    | 음의 높이가 높아짐 (예: 도 → 미 → 솔) |
| 주파수 ↓    | 음의 높이가 낮아짐 |
| 부저 (PWM)  | 전기적 ON/OFF로 진동을 만들어 공기를 흔듦 |
| 귀         | 공기 진동(파동)을 받아 음높이로 인식 |
| 가청 주파수 | 약 20Hz ~ 20,000Hz |
  
