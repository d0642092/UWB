import threading

# max = 10
class A (threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num
    def run(self):
        try:
            while True:
                print(self.num)
        except KeyboardInterrupt:
            print(123)
            exit()



