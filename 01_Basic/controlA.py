# This code try how to connect two program
# from pynput import keyboard
import threading
from A import *

class control(threading.Thread):
    def __init__(self, num, flag):
        threading.Thread.__init__(self)
        self.num = num
        self.flag = flag
    def run(self):
        while self.flag:
            print(self.num)
            pr(a["b"])
            break

if __name__ == '__main__':
    C = control("control", True)
    child = A("kid", True)

    child.start()
    C.start()


    try:
        while True:
            pass
        # C.join()
        # child.join()
    except KeyboardInterrupt:
        C.flag = False
        child.flag = False

        exit()
