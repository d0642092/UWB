import time
import struct
import matplotlib.pyplot as plt
import numpy as np
from math import *

t = [0]
Xa = [0]
Ya = [0]
Za = [0]
now = time.time()

def printplt(data):
    global t,Xa,Ya,Za,now
    plt.ion()
    plt.figure(1)
    if(data[0]!=253 or data[21]!=254):
        print('error')
    info = [data[i:i+1] for i in range(0, len(data), 1)]
    
    plt.clf()
    test = info[1:5]
    a=b''
    for i in test:
        a+=i
    result,=struct.unpack_from(">i",a)
    Xa_now=result/1000

    test = info[5:9]
    a=b''
    for i in test:
        a+=i
    result,=struct.unpack_from(">i",a)
    Ya_now=result/1000

    test = info[9:13]
    a=b''
    for i in test:
        a+=i
    result,=struct.unpack_from(">i",a)
    Za_now=result/1000

#    test = info[13:15]
#    a=b''
#    for i in test:
#        a+=i
#    print(a)
#    result,=struct.unpack_from(">H",a)
#    print(result)
    new = time.time()-now
    if t is None:
        t = [new]
        Xa = [Xa_now]
        Ya = [Ya_now]
        Za = [Za_now]
    else:
        t.append(new)
        Xa.append(Xa_now)
        Ya.append(Ya_now)
        Za.append(Za_now)
    if(len(Xa)>20):
        Xa = Xa[1:]
        Ya = Ya[1:]
        Za = Za[1:]
        t = t[1:]
    plt.plot(t,Xa,'-r')
    plt.plot(t,Ya,'-g')
    plt.plot(t,Za,'-b')
    plt.pause(0.1)