# 파이썬 쓰레드 실습: join만 뺐을때

import threading
import time

# 전역 변수와 락 생성
counter = 0 # 쓰레드가 공유하는 변수
lock = threading.Lock()  # 쓰레드 간 자원 동기화를 위한 락 (락을 만듦)

# 쓰레드에서 실행할 함수 정의 (쓰레드 함수)
def worker(name, id_num="1234"):
    global counter
    for i in range(10):
        with lock:  # 락을 사용하여 공유 자원(counter) 접근 보호
            counter += 1 # 락 안쪽의 counter 변수는 접근 보호
            print(f"[{threading.current_thread().name}] {name}-{id_num} 작업 중... (카운터={counter})")
        time.sleep(1)

# 쓰레드 객체 생성 (target은 함수, args는 인자 튜플) (쓰레드 만들기: worker 함수의 내용을 가지는 스레드 2개 만들기, 인자값 하나는 끝에 , )
t1 = threading.Thread(target=worker, args=("스레드1",), name="Thread-1")
t2 = threading.Thread(target=worker, args=("스레드2",), name="Thread-2")
# 쓰레드로 worker를 실행시키지 않았다면 하나 다 끝나고 다름 하나가 시작되었을 것.

# 데몬 설정 (True로 설정 시 메인 종료와 함께 쓰레드도 종료됨)
t1.daemon = True
t2.daemon = True

# 쓰레드 실행
t1.start()
t2.start()

# 현재 실행 중인 쓰레드 정보 출력
print(f"현재 실행 중인 쓰레드 수: {threading.active_count()}")
print(f"현재 실행 중인 쓰레드 목록: {threading.enumerate()}") # 현재 쓰레드가 몇개가 돌고있는 지

# is_alive()로 쓰레드 실행 여부 확인
print(f"{t1.name} 살아있나? {t1.is_alive()}") # 실행되고 있는지 종료되고 있는지
print(f"{t2.name} 살아있나? {t2.is_alive()}")

# join()으로 쓰레드가 종료될 때까지 대기 (이게 없으면 메인 쓰레드가 혼자 죽고 서브 쓰레드는 돌아감)


print("메인 쓰레드 종료됨.")
print(f"최종 카운터 값: {counter}")
