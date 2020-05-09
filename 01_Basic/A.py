import threading

# max = 10
a = {"a":1,"b":2}
class A (threading.Thread):
    def __init__(self, num, flag):
        threading.Thread.__init__(self)
        self.num = num
        self.flag = flag
    def run(self):
        while self.flag:
            print(self.num)
            break
def pr(name):
    print(name)



