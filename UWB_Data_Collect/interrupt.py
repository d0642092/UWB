import threading

class run(threading.Thread):
    def __init__(self,num,flag):
        threading.Thread.__init__(self)
        self.num = num
        self.flag = flag
    def run(self):
        while self.flag:
            print(self.num)

    def help():
        print("To view the list type 'view'"
              "\n To add an item type 'add'"
              "\n To remove an item type 'remove'"
              "\n To exit type exit or Ctrl + c can be used at any time")

    # =========SUBROUTENES END===============

    while loop:
        # task = input("What do you want to do? Type \"help\" for help:- ")
        # if task == 'help':
        #     help()
        # else:
        #     print("Invalid return please try again.")
        print("running")

except KeyboardInterrupt:
    print("InterRupt")
    exit()

if __name__ == "__main__":
    R = run("Running",True)
    R.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        R.flag = False
        print("InterRupt")

