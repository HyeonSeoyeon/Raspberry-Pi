import threading  # 파이썬에서 스레드를 다루기 위한 모듈 임포트
import time       # 시간 관련 함수(예: time.sleep)를 사용하기 위한 모듈 임포트

# --- 전역 변수 및 락(Lock) 초기화 ---
# 스레드 간에 공유될 전역 변수 'counter' 초기화
counter = 0
# threading.Lock 객체 생성: 여러 스레드가 동시에 공유 자원(여기서는 counter)에 접근하는 것을 막아주는 동기화 도구
lock = threading.Lock()

# --- 스레드에서 실행할 함수 정의 ---
# 각 스레드가 독립적으로 수행할 작업을 정의하는 함수
def worker(name):
    global counter  # 전역 변수 counter를 함수 내에서 수정하기 위해 global 키워드 사용
    for i in range(10): # 각 스레드는 10번 반복 작업 수행
        # with lock: 구문은 락(lock)을 획득하고, 블록이 끝나면 자동으로 락을 해제합니다.
        # 이 블록 안의 코드는 오직 한 번에 하나의 스레드만 실행할 수 있도록 보장됩니다.
        with lock:
            counter += 1  # 공유 자원인 counter를 1 증가
            # 현재 실행 중인 스레드의 이름과 작업 진행 상황, 현재 카운터 값 출력
            print(f"[{threading.current_thread().name}] {name} 작업 중... (카운터={counter})")
        time.sleep(0.1) # 0.1초 대기하여 다른 스레드에게 CPU 제어권을 넘겨줄 기회를 줍니다. (예제 편의상 1초에서 0.1초로 변경)

# --- 스레드 객체 생성 및 설정 ---
# threading.Thread 객체 생성:
# target: 스레드가 실행할 함수 (worker 함수)
# args: target 함수에 전달할 인자들의 튜플 (여기서는 ("스레드1",))
# name: 스레드의 이름을 지정 (디버깅 시 유용)
t1 = threading.Thread(target=worker, args=("스레드1",), name="Thread-1")
t2 = threading.Thread(target=worker, args=("스레드2",), name="Thread-2")

# 데몬 스레드 설정:
# 'daemon = True'로 설정하면 메인 스레드가 종료될 때 데몬 스레드도 강제로 종료됩니다.
# 'daemon = False' (기본값)로 설정하면 해당 스레드가 종료될 때까지 메인 스레드가 기다립니다.
t1.daemon = False
t2.daemon = False

# --- 스레드 실행 ---
# .start() 메서드를 호출하여 스레드의 작업을 시작합니다.
# 이 시점부터 worker 함수가 새 스레드에서 비동기적으로 실행됩니다.
t1.start()
t2.start()

# --- 스레드 정보 확인 ---
# 현재 실행 중인 활성 스레드의 개수 출력
print(f"\n현재 실행 중인 쓰레드 수: {threading.active_count()}")
# 현재 실행 중인 모든 Thread 객체 목록 출력
print(f"현재 실행 중인 쓰레드 목록: {threading.enumerate()}")

# .is_alive() 메서드를 사용하여 특정 스레드가 현재 실행 중인지 확인
print(f"{t1.name} 살아있나? {t1.is_alive()}")
print(f"{t2.name} 살아있나? {t2.is_alive()}")

# --- 스레드 종료 대기 ---
# .join() 메서드는 해당 스레드가 작업을 완료하고 종료될 때까지 메인 스레드를 블록(대기)시킵니다.
# join()을 사용하지 않으면 메인 스레드가 먼저 종료되면서 작업 중인 서브 스레드도 함께 종료될 수 있습니다 (데몬 스레드가 아닐 경우).
t1.join()
t2.join()

print("메인 쓰레드 종료됨.")
print(f"최종 카운터 값: {counter}") # 모든 스레드가 작업을 마친 후 최종 카운터 값 출력
