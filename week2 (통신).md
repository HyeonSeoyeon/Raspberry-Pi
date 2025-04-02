# 라즈베리파이 개요

### 라즈베리파이
- 라즈베리파이는 영국 라즈베리파이 재단이 교육을 목적으로 만든 신용카드 크기 저비용 컴퓨터다.
- 컴퓨터 과학과 기본적인 컴퓨팅 기술을 배우기 쉽게 하려고 만들어졌다.
- 라즈베리파이는 프로그래밍 학습, 하드웨어 프로젝트 구축, 소프트웨어 실험, 미디어 재생 등 여러 방면에서 활용된다.
- 특히 임베디드 컴퓨팅 분야에 많이 활용되며 각 종 센서와 연결하여 <mark>IoT(Internet of Things) 분야에도 광범위하게 활용</mark>되고 있다.
  
### 라즈베리파이 특징
- 가격: 매우 <mark>저렴</mark>하고 다양한 모델이 있어 용도와 필요성에 따라 선택 가능하다.
- 크기: 신용카드 크기로 <mark>매우 작아</mark> 다양한 프로젝트에 쉽게 사용할 수 있다.
- <mark>확장성: GPIO 핀을 통해 센서, 모터, LED 등 다양한 외부 장치를 연결할 수 있다.</mark>
- 소프트웨어: <mark>여러 운영 체제를 지원</mark>하며, Python, Scratch 등 <mark>다양한 프로그래밍 언어</mark>로 개발할 수 있다.
- 커뮤니티: 전 세계적으로 <mark>넓은 사용자와 개발자 커뮤니티</mark>를 보유하고 있어 다양한 자료와 지원을 받을 수 있다.

### 수업에서 사용되는 라즈베리파이
```
    모델명        |	출시년도 |	     CPU         |  	메모리    |	USB 포트 수 |	 HDMI 포트 수  |	GPIO 핀 수 |	      비고
Raspberry Pi 4 B |	  2019   |	1.5 GHz 쿼드코어 |	2GB/4GB/8GB |      4      |	2 (micro HDMI) |	    40     |	RAM 옵션 다양화
```
- ARM 계열 CPU 사용 : 모바일기기에 특화된 CPU - 발열이 적다

### <mark>GPIO 핀(General Purpose Input/Output)</mark> 이란?
- 컴퓨터의 범용 입출력 핀
- 라즈베리파이 같은 마이크로컨트롤러 또는 단일 보드 컴퓨터에서 <mark>다양한 전자 부품과의 물리적 연결</mark>을 가능하게 하는 핀
- GPIO 핀들을 통해 <mark>센서, 모터, LED 등 외부 장치를 컨트롤러에 연결</mark> -> 프로그래밍을 통해 데이터를 읽거나 장치를 제어
- GPIO 핀은 <mark>디지털 신호를 입력(읽기)하거나 출력(쓰기)</mark>하는 용도로 사용
- 사용자가 직접 제어할 수 있다는 점에서 유연함
- <mark>40개의 핀</mark>이 있고, 핀에서 필요로 하는 <mark>주요 통신 방법이 5가지</mark> 정도 있다 (외워야 함)

------------

### 1. 라즈베리파이 GPIO 일반 디지털 입출력 (Input/Output)
- 라즈베리파이에서 가장 기본적으로 사용하는 핀 모드이다.
  - <mark>입력 (GPIO.IN): 외부 센서나 스위치의 상태를 읽을 때 사용</mark>
  - <mark>출력 (GPIO.OUT): LED, 릴레이, 부저 등 외부 장치를 제어할 때 사용</mark>
- <mark>HIGH (3.3V), LOW (0V)</mark> 두 가지 상태를 가진다.
- 입력 모드일 때 내부 풀업/풀다운 저항 설정 가능하다. (<mark>PUD_UP, PUD_DOWN, PUD_OFF</mark>)
  - https://blog.naver.com/jamduino/220820935325
- <mark>디지털 신호</mark>만 처리 할 수 있다. (아날로그 입력 불가, 필요시 ADC(아날로그-디지털 변환기) 사용)
  - 라즈베리파이 GPIO 핀 번호 <mark>GPIO2 ~ GPIO27</mark> 대부분 사용 가능
  - 특별 기능(SPI, I2C, PWM 등) 없는 핀은 모두 일반 입출력으로 사용 가능
    
### 2. 라즈베리파이 GPIO I2C 통신 (반이중통신: 쌍방향, 하나씩 통신하는 무전기)
- I2C(Inter-Integrated Circuit)는 소수의 핀을 사용해 여러 장치 간 데이터를 전송하는 <mark>직렬 통신 프로토콜</mark>이다.
  - 직렬 통신: 데이터를 한 줄(선)로 하나씩 순서대로 보내는 방식 - 느리다, 단순
  - 병렬 통신: 여러 개의 선을 이용해서 데이터를 한 번에 여러 개씩 보내는 방식 - 빠르다, 복잡
  - 라즈베리파이는 직렬 통신 방식을 사용해서 센서나 다른 장치들과 데이터를 주고받는다.
  - 마스터가 슬레이브에게 데이터를 보내면, 그 순간에는 슬레이브가 데이터를 보낼 수 없어서 기다려야 한다.
- 라즈베리파이 GPIO 핀 번호
  - <mark>Data (GPIO2), Clock (GPIO3)</mark>
  - EEPROM Data (GPIO0), EEPROM Clock (GPIO1)
- 마스터-슬레이브 구조로, 하나의 마스터가 여러 슬레이브 장치와 통신할 수 있다.
  - 마스터는 일반적으로 라즈베리파이가 역할을 수행하며 슬레이브가 병렬로 연결되어 있다.
  - I2C에서 슬레이브는 주로 센서, 메모리 장치, LCD 디스플레이와 같은 저속 주변 장치이다.
  - 마스터가 슬레이브와 통신할 때, 다른 슬레이브들은 무시한다.
- 라즈베리파이에서는 <mark>SDA(데이터 라인)와 SCL(클록 라인)</mark> 두 개의 신호 라인을 사용한다.
  - SCL (Clock, GPIO3): 0,1 클럭을 계속 반복적으로 보냄 (일정한 박자를 맞춰주는 역할)
  - SDA (Data, GPIO2): 실제 데이터가 오가는 길 (master가 slave, slave가 master에게 데이터 전송하는 선)
- I2C 통신의 시작과 종료((Start Condition & Stop Condition)
  - <mark>마스터가 SCL이 High이고 SDA가 Low인 상태에서, SDA를 High로 바꾸어 슬레이브에게 통신 시작을 알림</mark>
  - 🚦 예시: 신호등에서 초록불(SCL=HIGH)일 때 🚶‍♂️보행자가 갑자기 도로로 뛰어든다(SDA = LOW로 변경).
  - <mark>끝 부분에서 SCL이 High일 때 SDA가 High로 바뀌는 것을 정지조건(Stop Condition)</mark>
- 🎯 I2C의 장점
  - 선이 2개만 필요해서 깔끔함.
  - 여러 개의 기기를 연결할 수 있음.
- 🎯 I2C의 단점
  - 반이중 통신이라 한 번에 한 방향으로만 데이터 보낼 수 있어서 속도가 느림.

### 3. 라즈베리파이 GPIO SPI 통신 (전이중통신: 양방향, 동시에 통신하는 스마트폰)
- SPI(Serial Peripheral Interface)는 <mark>고속 직렬 통신 프로토콜</mark>이다.
  - SPI는 높은 속도가 필요한 응용 분야에 적합하다.
- 마스터-슬레이브 구조이다.
- SPI 기본 신호
  - <mark>MOSI(Master Out Slave In): 마스터 → 슬레이브 데이터 전송</mark>
  - <mark>MISO(Master In Slave Out): 슬레이브 → 마스터 데이터 전송</mark>
  - <mark>SCLK(Serial Clock): 클럭 신호 (마스터가 박자를 맞춰줌)</mark>
  - <mark>SS(Slave Select)[SS==CE]: 특정 슬레이브 활성화(슬레이브 선택)</mark>
- 라즈베리파이 GPIO 핀 번호
  - <mark>SPI0: MOSI (GPIO10); MISO (GPIO9); SCLK (GPIO11); CE0 (GPIO8); CE1 (GPIO7)</mark>
  - SPI1: MOSI (GPIO20); MISO (GPIO19); SCLK (GPIO21); CE0 (GPIO18); CE1 (GPIO17); CE2 (GPIO16)
- I2C와 다르게 데이터 전송 선이 두개가 있다. (I2C에서는 SDA)
  - 동시에 데이터 주고 받기 가능(전이중)
-  장치를 두 개밖에 꽂지 못함 (하나 통신하고 있으면 하나는 대기 상태)
  - 예시: CE0에 붙은 장치가 활성화되어 있으면 CE1에 붙은 장치는 대기
- SPI 통신 과정 예시
  - 1️⃣ 마스터가 슬레이브 선택: CE0(GPIO8) = Low 
  - 2️⃣ 동시에 데이터 주고받기: MOSI (GPIO10), MISO (GPIO9)
  - 3️⃣ 통신 종료: CE0(GPIO8) = High
- 🎯 SPI의 장점
  - 전이중 통신 가능 → 데이터 송수신이 동시에 이루어져서 빠름
  - I2C보다 높은 속도 가능
- 🎯 SPI의 단점
  - I2C보다 더 많은 선이 필요함
  - CE 수만큼만 기기 연결 가능

#### <I2C vs SPI 차이점 정리>
통신 방식:	반이중 (한 번에 한 방향)	vs 전이중 (동시에 송수신 가능)<br>
속도:	비교적 느림 vs 빠름<br>
선 개수:	2개 (SCL, SDA) vs 최소 4개 (MOSI, MISO, SCLK, SS)<br>
연결 가능한 기기 수:	많음 vs 제한적 (CE 개수만큼)<br>

#### <I2C vs SPI 사용할 GPIO 핀 정리>
I2C SDA:	GPIO2<br>
I2C SCL:	GPIO3<br>
SPI MOSI:	GPIO10<br>
SPI MISO:	GPIO9<br>
SPI SCLK:	GPIO11<br>
SPI CE0:	GPIO8<br>
SPI CE1:	GPIO7<br>

🔹 결론 <br>
I2C는 선이 적고 간단하지만 느림 (온도 센서, OLED 화면 같은 간단한 장치에 적합).<br>
SPI는 빠르지만 선이 많음 (SD 카드, 카메라 모듈 같은 고속 데이터 전송에 적합).
    
### 4. 라즈베리파이 GPIO UART 통신 (반이중통신, SPI의 옛 버전이라고 생각하세요)
- UART(Universal Asynchronous Receiver/Transmitter)는 <mark>비동기 직렬 통신을 위한 프로토콜</mark>이다.
- UART는 시작 비트, 데이터 비트, 패리티 비트(선택 사항), 정지 비트로 구성된 데이터 패킷을 사용해 통신한다.
- UART는 주로 컴퓨터, 마이크로컨트롤러, 통신 장비 간의 저속 통신에 사용된다.
- 라즈베리파이에서는 <mark>TX(송신) 핀과 RX(수신) 핀</mark>을 사용한다.
- 라즈베리파이 GPIO 핀 번호
  - <mark>TX (GPIO14); RX (GPIO15)</mark>
  
### 5. 라즈베리파이 GPIO PWM 출력(통신 X)
- PWM(Pulse Width Modulation)은 <mark>디지털 신호를 조절해 아날로그(시간, 소리)와 같은 효과</mark>를 내는 기술이다.
- PWM은 펄스의 폭을 변화시켜 출력 전압의 평균값을 조절한다.
  - purse를 modulation(이진화)시켜서 보내주는 데이터
- PWM은 효율적인 전력 관리와 부드러운 아날로그 제어를 가능하게 한다.
- 라즈베리파이에서는 PWM을 LED의 밝기 조절, 모터의 속도 조절 등을 할 수 있다.
- 라즈베리파이 GPIO 핀 번호
  - Software PWM available on all pins
  - Hardware PWM available on <mark>GPIO12, GPIO13, GPIO18, GPIO19</mark>

### 직렬 통신과 병렬 통신
<table>
  <tr>
    <td>구분</td>
    <td>직렬 통신</td>
    <td>병렬 통신</td>
  </tr>
  <tr>
    <td>데이터 선</td>
    <td>1~2개 (SDA, SCL, RX, TX 등)</td>
    <td>여러 개 (8, 16, 32개 선)</td>
  </tr>
  <tr>
    <td>전송 방식</td>
    <td>1비트씩 순서대로 전송</td>
    <td>여러 비트 동시에 전송</td>
  </tr>
  <tr>
    <td>다중화 사용</td>
    <td>경우에 따라 (TDMA, FDMA 적용 가능)</td>
    <td>사용 안 함, 선 자체가 분리되어 있음</td>
  </tr>
  <tr>
    <td>예시</td>
    <td>UART, SPI, I²C, USB</td>
    <td>CPU-RAM, PATA, Parallel Port, GPIO 병렬 출력</td>
  </tr>
</table>

### I2C 직렬 통신 예시
<table>
  <tr>
    <td>단계</td>
    <td>SDA 데이터 및 상태</td>
    <td>SCL 상태</td>
    <td>설명</td>
  </tr>
  <tr>
    <td>Start Condition</td>
    <td>SDA: HIGH → LOW</td>
    <td>HIGH</td>
    <td>통신 시작. SCL HIGH 상태에서 SDA가 HIGH → LOW로 떨어짐</td>
  </tr>
  <tr>
    <td>슬레이브 주소 전송</td>
    <td>1 0 1 0 0 0 0 (슬레이브 주소 7비트, 예: 0b1010000)</td>
    <td>동기화됨</td>
    <td>마스터가 슬레이브의 주소 전송 (비트 순서대로 직렬 전송)</td>
  </tr>
  <tr>
    <td>R/W 비트</td>
    <td>1 (Read 요청)</td>
    <td>동기화됨</td>
    <td>1 = Read 요청 (슬레이브에게 데이터 읽기 요청)</td>
  </tr>
  <tr>
    <td>슬레이브 ACK</td>
    <td>0 (ACK)</td>
    <td>동기화됨</td>
    <td>슬레이브가 자신의 주소와 일치하면 LOW(0) 전송 → "응답하겠다"</td>
  </tr>
  <tr>
    <td>슬레이브 데이터 전송</td>
    <td>1 1 0 0 1 1 0 0 (예: 0xCC, 11001100)</td>
    <td>동기화됨</td>
    <td>슬레이브가 마스터에게 데이터 전송, 비트 하나씩 직렬로 전달</td>
  </tr>
  <tr>
    <td>마스터 NACK</td>
    <td>1 (NACK)</td>
    <td>동기화됨</td>
    <td>마스터가 HIGH(1) 전송 → "더 이상 안 받겠다" 신호</td>
  </tr>
  <tr>
    <td>Stop Condition</td>
    <td>SDA: LOW → HIGH</td>
    <td>HIGH</td>
    <td>통신 종료. SCL HIGH 상태에서 SDA가 LOW → HIGH로 올라감</td>
  </tr>
</table>

