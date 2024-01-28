from sklearn.preprocessing import PolynomialFeatures
from socket import *
from .TrainingSystem.classes.pointCalculation import PointCalculation
# API, load model
import requests, pickle, numpy, time
import matplotlib.pyplot as plt
ip = "127.0.0.1" # resiberry_ip
url = "http://%s/php/diagnosis.php?getrangingdiagnosis=4210000000001198&project_id=1" % ip
ANCHOR = ["An0094", "An0095", "An0096", "An0099"]

def get_dis_from_api():
    distance = requests.get(url)
    data = distance.json()  # 解json格式

    dis = []
    for name in ANCHOR:
        tmp = eval(data[name])
        dis.append(tmp['Ranging'])
    return dis
def get_diff(current, past):
    ans = []
    for i in range(len(current)):
        ans.append(int(current[i]) - int(past[i]))
    return ans
def location_system_stabeling(current, past, numOfAnchor):
    # Locating System is Stabeling #
    print("Please Stop Moving, System Locating......")
    diff = [[0,0,0,0]]
    jumpOut = False
    while not jumpOut:
        try:
            if past == []:
                past = get_dis_from_api()
            else:
                current = get_dis_from_api()
                diff.append(get_diff(current,past))
                past = current.copy()
                for i in range(numOfAnchor):
                    if diff[-1][i] > 20 :
                        jumpOut = False
                        print("System Locating...")
                    else:
                        jumpOut = True
        except KeyError as e:
            print(repr(e))
            continue
    # Locating System is Stabeling #
    return current.copy(), past.copy()

def create_message(pc, past, quadraticFeaturizer, anchorGroups):
    fixRange, position = [], []
    for index, name in enumerate(ANCHOR):
        model = pickle.load(open("./Anchor_model/"+name+".sav",'rb'))
        # pass by Location algorithm
        fixRange.extend(model.predict(quadraticFeaturizer.fit_transform(numpy.array(past[index]).reshape(-1, 1))))
    for i, value in enumerate(past):
        past[i] = int(value)
    pc.set_dis(fixRange)
    prpoints = pc.get_cal_array(anchorGroups)
    # transport Location to the Car
    position.extend(pc.get_point(prpoints))
    message = str(position[0]) + "," + str(position[1])+'\\'
    print(message)
    return message

if __name__ == "__main__":
    # Anchor Setting #
    x, y = 50, 50
    anchorX = [x, -x, x, -x]
    anchorY = [y, y, -y, -y]
    # Anchor Setting #
    # count = 0
    current, past = [], []
    numOfAnchor = 4
    # Locating System is Stabeling
    current, past = location_system_stabeling(current, past, numOfAnchor)

    # Communicate Setting #
    HOST = '127.0.0.1'  # socket server端的ip 可在內網
    PORT = 55688  # 'SendCommand.py'是你的server端
    ADDR = (HOST, PORT)
    BUFFSIZE = 1024
    client = socket(AF_INET, SOCK_STREAM)
    try:
        print("connect Car..")
        client.connect(ADDR)
        client.sendall("座標端".encode())
        print(client.recv(BUFFSIZE))
    except Exception:
        print("Connect Fail..")
    # Communicate Setting #
        
    '''
    if diff > limit,
        it would be considered as broken distance Data
    '''
    moveLimit = 100
    quadraticFeaturizer = PolynomialFeatures(10)
    pc = PointCalculation(anchorX, anchorY)
    anchorGroups = pc.get_group(4)
    while True :
        try:
            current = get_dis_from_api()
        except KeyError as k:
            print(repr(k))
            continue
        except Exception:
            continue
        jumpOut = False
        curDiff = get_diff(current, past)
        try:
            for i in range(numOfAnchor):
                if curDiff[i] > moveLimit:
                    jumpOut = True
                    break
            if not jumpOut:
                moveLimit = 100
                # current is a useful Distance Data
                past = current.copy()
                message = create_message(pc, past, quadraticFeaturizer, anchorGroups)
                client.sendall(message.encode())
                time.sleep(0.1)
            else:
                moveLimit += 20
                print("broken data")
        except ValueError as e:
            print(repr(e))
        except TypeError:
            print("points is None")
        except KeyboardInterrupt:
            break
    client.close()