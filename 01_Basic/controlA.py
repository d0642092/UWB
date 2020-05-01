# This code try how to connect two program
# from pynput import keyboard
import threading
from A import *

class control(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num
    def run(self):
        try:
            while True:
                print(self.num)
        except KeyboardInterrupt:
            print(456)
            exit()

# def keyboard_on_press(key):
#
#
#
# def keyboard_on_release(key):
#     print('{0} release'.format(key))
#     if key == key.esc:
#         # Stop listener
#         return False
#
# def keytest():
#     with keyboard.Listener(on_press=keyboard_on_press,
#                       on_release=keyboard_on_release) as listener: #  press的時候, 執行method
#         listener.join()
# keyboardThread = threading.Thread(target=keytest)

if __name__ == '__main__':
    C = control("control")
    child = A("kid")

    child.start()
    C.start()


    C.join()
    child.join()