
import time
# import threading
from UWB_Data_Collect.New_Code.CatchData import catchData
from UWB_Data_Collect.New_Code.WriteData import writerData
from UWB_Data_Collect.New_Code.ControllCar import Forward

if __name__ == "__main__":

    car_runTime = 5  # How much time let the car run
    total_distance = 100  # How long if the car run car_runTime second
    avg_V = total_distance / car_runTime  # The average velocity

    dataCatch = catchData("CatchData", True)   # car 延遲兩秒 sleep(2)
    dataWrite = writerData("WriteData", 1, True, avg_V)
    controlCar = Forward("ControlCar", True)

    controlCar.start()
    dataCatch.start()
    dataWrite.start()

    # if ~controlCar.flag:  # 會占用主程式
    #     dataCatch.flag = False
    #     exit()


    carStart = time.time()
    carEnd = time.time()

    try:
        while carEnd - carStart < car_runTime:
            print(carEnd - carStart)
            carEnd = time.time()

        # 停止 thread
        controlCar.flag = False
        dataCatch.flag = False
        # while True:
        #     pass
    except KeyboardInterrupt:
        controlCar.flag = False
        dataCatch.flag = False
    dataWrite.undone = False
    dataWrite.join()