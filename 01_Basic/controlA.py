# This code try how to connect two program
# from pynput import keyboard
import threading
from A import *
from pynput import keyboard
import time

class control(threading.Thread):
    def __init__(self, num, flag):
        threading.Thread.__init__(self)
        self.num = num
<<<<<<< HEAD

    @classmethod
    def print_run(cls):
        while True:
            time.sleep(1)
            print("running")

    @classmethod
    def keyboard_on_press(cls, key):
        exit(0)

    @classmethod
    def keyboard_on_release(cls, key):
        print('{0} release'.format(key))
        if key == key.esc:
            # Stop listener
            return False

    @classmethod
    def keytest(cls):
        with keyboard.Listener(on_press=cls.keyboard_on_press,
                               on_release=cls.keyboard_on_release) as listener:  # press的時候, 執行method
            listener.join()
        while True:
            time.sleep(1)
            print("running")

    def run(self):
        keyboardThread = threading.Thread(target=self.keytest)
        # printRunning = threading.Thread(target=self.print_run)

        keyboardThread.start()
        # printRunning.start()

        keyboardThread.join()
        # printRunning.join()



if __name__ == '__main__':
    C = control("control")
    # child = A("kid")
=======
        self.flag = flag
    def run(self):
        while self.flag:
            print(self.num)
            pr(a["b"])
            break

if __name__ == '__main__':
    C = control("control", True)
    child = A("kid", True)
>>>>>>> 20a69e0e8cf1e47bdd0bd83795adcc00b79884c6

    # child.start()
    C.start()


<<<<<<< HEAD
    C.join()
    # child.join()
=======
    try:
        while True:
            pass
        # C.join()
        # child.join()
    except KeyboardInterrupt:
        C.flag = False
        child.flag = False

        exit()
>>>>>>> 20a69e0e8cf1e47bdd0bd83795adcc00b79884c6
