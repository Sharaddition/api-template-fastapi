import time
from threading import Thread

def executed(id):
    print('Executed:', id)

def delay_fn(sec):
    print('Thread:', sec)
    time.sleep(sec)
    executed(sec)

def compare_thread():
    start_time = time.time()
    thread1 = Thread(target=delay_fn, args=[4])
    thread2 = Thread(target=delay_fn, args=[3])
    thread1.start()
    thread2.start()
    delay_fn(2)
    thread1.join()
    thread2.join()
    print('Time Elapsed:', time.time()-start_time)
    # print(thread1, thread2, no_fn)

compare_thread()