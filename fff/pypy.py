import threading
import traceback
threadLock = threading.Lock()
def func1():
    threadLock.acquire()
    print('iiiii')
    timer = threading.Timer(3, func1)
    print('idfdhfhdf{}'.format(threading.activeCount()))
    timer.start()
    threadLock.release()
if __name__ == '__main__':
    try:
        func1()
    except:
        traceback.print_exc()