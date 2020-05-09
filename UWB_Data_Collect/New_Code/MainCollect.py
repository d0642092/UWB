import time
import threading  # https://dotblogs.com.tw/yc421206/2011/01/04/20575
from UWB_Data_Collect.New_Code.CatchData import catchData
from UWB_Data_Collect.New_Code.WriteData import writerData
from UWB_Data_Collect.New_Code.ControllCar import Forward

class ServerNotAlive(threading.Thread):
    def __init__(self,flag):
        threading.Thread.__init__(self)
        self.flag = flag
    def run(self):
        while self.flag:
            if not controlCar.flag:  # 會占用主程式所以另用一個thread 不能用~controlCar.flag
                # dataCatch.flag = False  # 應該沒有意義到<有sleep>
                print("server close")
                self.flag = False


if __name__ == "__main__":

    car_runTime = 10  # How much time let the car run
    total_distance = 100  # How long if the car run car_runTime second
    avg_V = total_distance / car_runTime  # The average velocity

    controlCar = Forward("ControlCar", True)
    checkServer = ServerNotAlive(True)
    # dataCatch = catchData("CatchData", True)  # car 延遲兩秒 sleep(2)
    # dataWrite = writerData("WriteData", 1, True, avg_V)

    controlCar.start()
    checkServer.start()

    # time.sleep(2.2)
    # dataCatch.start()
    # dataWrite.start()


    carStart = time.time()
    carEnd = time.time()

    try:
        if checkServer.flag:
            while carEnd - carStart < car_runTime:
                # print(carEnd - carStart)
                carEnd = time.time()

        # 停止 thread
        checkServer.flag = False
        controlCar.flag = False
        # dataCatch.flag = False
        # while True:
        #     pass
    except KeyboardInterrupt:
        controlCar.flag = False
        # dataCatch.flag = False
        checkServer.flag = False
    print("stasteart to join")
    controlCar.join()
    print("start cs join")
    checkServer.join()
    # dataWrite.undone = False
    # dataWrite.join()