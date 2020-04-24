import threading
import requests
from openpyxl import Workbook
import json
import queue

url = "http://192.168.8.107/php/diagnosis.php?getrangingdiagnosis=4210000000001198&project_id=1"
input = {'An0011': '{"Ranging":"327","PCnt":"212","AnCnt":"6","TagRecv":"-101","TagFP":"-119","AnRecv":"-101","AnFP":"-110","LostRate":"0","DataRate":"7.15198","DataCount":"13187","SlotTime":"68","ResetTime":"136","TagVelocity":"0.00","SD":"3.38","IMU":"0,0,10,1,1,0"}', 'An0095': '{"Ranging":"165","PCnt":"209","AnCnt":"6","TagRecv":"-101","TagFP":"-96","AnRecv":"-101","AnFP":"-108","LostRate":"2","DataRate":"7.17","DataCount":"12790","SlotTime":"68","ResetTime":"136","TagVelocity":"0.00","SD":"1.10","IMU":"0,0,10,1,1,0"}', 'An0099': '{"Ranging":"175","PCnt":"215","AnCnt":"6","TagRecv":"-103","TagFP":"-98","AnRecv":"-101","AnFP":"-110","LostRate":"5","DataRate":"7.13","DataCount":"12880","SlotTime":"68","ResetTime":"136","TagVelocity":"0.00","SD":"1.73","IMU":"0,0,10,1,1,0"}', 'An0094': '{"Ranging":"145","PCnt":"213","AnCnt":"6","TagRecv":"-101","TagFP":"-96","AnRecv":"-102","AnFP":"-105","LostRate":"1","DataRate":"7.03","DataCount":"13208","SlotTime":"68","ResetTime":"136","TagVelocity":"0.00","SD":"1.28","IMU":"0,0,10,1,1,0"}', 'An0096': '{"Ranging":"145","PCnt":"216","AnCnt":"6","TagRecv":"-101","TagFP":"-96","AnRecv":"-101","AnFP":"-102","LostRate":"0","DataRate":"6.61","DataCount":"12931","SlotTime":"68","ResetTime":"136","TagVelocity":"0.00","SD":"1.94","IMU":"0,0,10,1,1,0"}'}
DataQueue = queue.Queue()

class catchData (threading.Thread):
    def __init__ (self,num):
        threading.Thread.__init__(self)
        self.num = num

    
    def run(self):
        AnchorName = ["An0011","An0094","An0095","An0096","An0099"]
        #while True:
        try:
            # dis = requests.get(url)
            for i in AnchorName:
                dis = json.loads(input[i])
                # output.append(dis["Ranging"])
                # output.append(dis["IMU"])
                # output.append(0)

        except KeyError:
            pass
        DataQueue.put(dis)

class writeData (threading.Thread):
    def __init__ (self,num):
        threading.Thread.__init__(self)
        self.num = num
    
    def run(self):
        output = []
        wb = Workbook()
        ws = wb.active
        ws.append(["An0011","","","An0094","","","An0095","","","An0096","","","An0099","",""])
        ws.append(["Ranging","IMU","Actual"]*5)
        disData = DataQueue.get()
        output.append(disData["Ranging"])
        output.append(disData["IMU"])
        output.append(0)
        ws.append(output)
        wb.save('Test.xlsx')


                    

if __name__ == "__main__":
    
    # data = {i:eval(dis[i]) for i in AnchorName}
    #print(data)
    IMU = catchData("IMU")
    write = writeData("Write")
    IMU.start()
    write.start()
    IMU.join()
    write.join()

