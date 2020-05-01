import threading

class run(threading.Thread):
    def __init__(self,num,flag):
        threading.Thread.__init__(self)
        self.num = num
        self.flag = flag
    def run(self):
        while self.flag:
            print(self.num)

if __name__ == "__main__":
    R = run("Running",True)
    R.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        R.flag = False
        print("InterRupt")
        