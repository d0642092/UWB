
import serial
from Program.Car.past_code.SenpaiWork.carside import xyzplot as xyz
import time
import threading
from Program.Car.past_code.SenpaiWork.carside import zmqcam
import zmq
# ser = serial.Serial('com5',57600)
ser = serial.Serial('com5',115200)
# 115200看 flymcu.exe

# ip = '10.22.26.212'
ip = '192.168.8.104'
#57600
print(ser.portstr)
data = []
def pro_print(data): #print xyz
    print(data)
    xyz.printplt(data)

def tp_read(): #read data from sp
    global data
    while True:
        tmp = ser.read(24)
        if(tmp[0]!=253 or tmp[21]!=254):
            continue
        print(tmp)
        data=tmp


def zmqrec(ip): #recieve control command and send command
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind ('tcp://'+ip+':55688')
    while True:
        rec = socket.recv()
        socket.send_string('OK')
        ser.write(rec)
        # print(rec)

tr = threading.Thread(target = tp_read)
ct = threading.Thread(target = zmqcam.start,args= (ip,))
t_cdrec = threading.Thread(target = zmqrec,args= (ip,))


if __name__ == "__main__":
    tr.start()
    t_cdrec.start()
    ct.start()
    while True:
        if data == []:
            continue
        pro_print(data)
        time.sleep(0.1)

    