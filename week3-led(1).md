# 라즈베리파이 RGB Color 액츄레이터 모듈 구동하기

## 빵판(Breadboard)
- 전자회로의 시제품(시작품)을 만드는 데 사용하는 무땜납 장치
- 천공 아래에 많은 납이 도금된 인청동 스프핑 클립이 있는 플라스틱 천공 블록

## SMD형 LED 모듈
- 표면 실장 디자인(Surface-Mount Device, SMD)을 채택한 LED 모듈이다.
- Keyes SMD LED 모듈 작고, 설치가 간편하며, 다양한 전자 프로젝트와 실험에서 광원이나 지시등으로 사용된다.
- SMD LED는 전통적인 스루홀(Through-Hole) 타입 LED보다 작고, 발열이 적으며, 에너지 효율이 좋다는 특징이 있다.
- GPIO 연결
```
- : Ground 접지(핀 14)
G : GPIO 22(핀 15)
R : GPIO 27(핀 13)
B : GPIO 17(핀 11)
```

## 3_color_led.py
```py
import RPi.GPIO as GPIO   # GPIO 패키지 설치
import time

# 핀 번호 설정
BLUE_PIN = 17
GREEN_PIN = 22
RED_PIN = 27

# GPIO 핀의 번호 모드 설정 및 LED 핀의 모드를 출력으로 설정
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BLUE_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(RED_PIN, GPIO.OUT)

# GPIO 설정 초기화
def cleanup_gpio():
    GPIO.cleanup()

# LED를 순차적으로 켜고 끄는 함수
def cycle_leds():
    # 파란색 LED 켜기
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(BLUE_PIN, GPIO.LOW)
   
    # 초록색 LED 켜기
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(GREEN_PIN, GPIO.LOW)
   
    # 빨간색 LED 켜기
    GPIO.output(RED_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(RED_PIN, GPIO.LOW)

# 메인 프로그램
def main():
    setup_gpio()
    try:
        while True:
            cycle_leds()
    except KeyboardInterrupt:
        # Ctrl+C 눌렀을 때 실행 종료
        pass
    finally:
        cleanup_gpio()  # GPIO 설정 초기화

# 실행 진입점
if __name__ == "__main__":
    main()
```

---

# 사용된 함수

## <mark>GPIO.setmode()</mark>
: GPIO 핀 번호링 체계를 설정 <br>
- GPIO.BOARD	핀 번호를 보드의 물리적 위치로 지정.
- GPIO.BCM	핀 번호를 Broadcom SOC 채널 번호로 지정. <- 주로 사용
```python
GPIO.setmode(GPIO.BCM)
```

## <mark>GPIO.setup()</mark>
- GPIO 핀을 입력 또는 출력 모드로 설정

### 1. 기본 구조

```python
GPIO.setup(channel, direction, pull_up_down=None, initial=None)
```

| 인자 이름       | 데이터 타입      | 기능 |
|---------------|---------------|----------------------------------------------------------------|
| `channel`    | `int or list` | 설정할 GPIO 핀 번호 (정수: 단일 핀, 리스트: 여러 핀 설정 가능) |
| `direction`  | `int`         | 핀의 모드 설정 (`GPIO.IN` = 입력 모드, `GPIO.OUT` = 출력 모드) |
| `pull_up_down` | `int (선택)` | 내부 풀업/풀다운 저항 설정 (`GPIO.PUD_OFF(기본값)`, `GPIO.PUD_UP`, `GPIO.PUD_DOWN`) |
| `initial`    | `int (선택)` | 출력 모드에서 초기 핀 상태 (`GPIO.HIGH` or `GPIO.LOW`) |

---

### 2. 사용 예제

#### 2.1. 기본적인 사용법 (필수 인자만 사용)
```python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # 핀 번호 모드 설정 (BCM 방식)
GPIO.setup(17, GPIO.OUT)  # GPIO 17번 핀을 출력 모드로 설정
```

---

#### 2.2. 풀업/풀다운 저항 설정
```python
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO 18번 핀을 입력 모드 + 내부 풀업 저항 활성화
```
**풀업 저항 (Pull-up resistor)**: 기본적으로 HIGH(1) 상태 유지  
**풀다운 저항 (Pull-down resistor)**: 기본적으로 LOW(0) 상태 유지 <- 보통 이것으로 많이 사용됨

➡ 스위치 같은 입력 장치에서 **떠 있는 상태(Floating)를 방지**하기 위해 사용됨.

---

#### 2.3. 초기 출력 값 설정
```python
GPIO.setup(23, GPIO.OUT, initial=GPIO.HIGH)  # GPIO 23번 핀을 출력 모드로 설정하고 초기 값을 HIGH(1)로 설정
```
**출력 모드 (`GPIO.OUT`)일 때만 `initial` 설정 가능!**  
➡ 전원 인가 시 특정 핀을 **HIGH(1) 또는 LOW(0)** 상태로 시작하도록 설정 가능. (초기 상태는 LOW인 것이 좋다)

---

#### 2.4. 모든 인자를 활용한 설정 예시
```python
GPIO.setup(24, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN, initial=GPIO.LOW)
```
✅ GPIO 24번 핀을 출력 모드로 설정  
✅ 풀다운 저항 활성화 (기본값 LOW)  
✅ 초기 값을 LOW(0)로 설정  

---

#### 2.5. 여러 개의 핀을 한 번에 설정
```python
GPIO.setup([5, 6, 13], GPIO.OUT, initial=GPIO.LOW)
```
📌 GPIO 5, 6, 13번 핀을 한 번에 설정 (출력 모드 & 초기 LOW)

---

### 3. 정리
✅ `GPIO.setup(channel, direction, pull_up_down=None, initial=None)`  
✅ **필수:** `channel`, `direction`  
✅ **선택:** `pull_up_down`, `initial`  
✅ `pull_up_down`은 **입력 모드 (`GPIO.IN`)** 에서 사용  
✅ `initial`은 **출력 모드 (`GPIO.OUT`)** 에서 사용  

---


## <mark>GPIO.output()</mark>
- GPIO 핀에 전압을 출력하여 핀 상태를 변경하는 데 사용
- 주로 출력 모드로 설정된 핀에 사용
  
```python
GPIO.output(channel, state)
```

| 인자 이름  | 데이터 타입    | 기능 |
|-----------|-------------|------------------------------------------------|
| `channel` | `int or list` | 출력 상태를 변경할 GPIO 핀의 번호 (단일: 정수, 여러 개: 리스트) |
| `state`   | `int or bool` | 핀의 상태 설정 (`GPIO.HIGH` 또는 `True`: HIGH, `GPIO.LOW` 또는 `False`: LOW) |

---

```python
GPIO.output(18, GPIO.HIGH)  # GPIO 18번 핀을 HIGH(ON) 상태로 변경
```
```python
GPIO.output([17, 18], [GPIO.HIGH, GPIO.LOW])  # GPIO 17번 핀은 HIGH, 18번 핀은 LOW로 설정
```

---

## <mark>GPIO.cleanup()</mark>
- GPIO 핀을 정리하고 초기 상태로 되돌리는 함수 (입력 모드로 변경됨)
- 프로그램 종료 시 권장됨
  - 이전 프로그램에서 GPIO를 사용한 후 cleanup()을 호출하지 않으면, 다음 프로그램이 실행될 때 **"GPIO 핀을 이미 사용 중"**이라는 오류가 발생할 수도 있음
```py
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)



GPIO.cleanup()  # 모든 GPIO 핀 해제
```
- 위의 코드에서 GPIO.cleanup()을 호출하지 않은 경우
  - 프로그램이 종료된 후에도 GPIO 18번 핀은 계속 HIGH(전압 출력) 상태로 유지되어 LED가 꺼지지 않을 수도 있음
  - 
