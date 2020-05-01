# This code try how to connect two program
# from pynput import keyboard
import threading
from A import *
from pynput import keyboard
import time

class control(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

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

    # child.start()
    C.start()


    C.join()
    # child.join()