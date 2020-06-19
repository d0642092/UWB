import math
from openpyxl import load_workbook
import turtle as tl
import numpy as np

def get_cos(c,a,b):#短邊、長邊、anchor間距離
    tmp = math.pow(a,2) + math.pow(b,2) - math.pow(c,2)
    div = 2 * a * b
    return round(tmp / div , 2) # cos(c)

def get_dis(c,a,b):
    return a * get_cos(c,a,b)

def get_anchor_dis(x_off,y_off):
    return round(math.sqrt(math.pow(x_off,2) + math.pow(y_off,2)),2)

# x = [0,-75,75,-75,75]
# y = [0,-75,-75,75,75]
#dis = [162,90,189,120,232]#anchor
#dis = [138,80,174,128,200]#real
#dis = [153,99,100,177,190]#anchor
#dis = [116,92,92,178,175]#real
#dis = [174,102,245,88,234]
#dis = [133,105,222,100,222]
x = [-242,242,242,-242]
y = [110,110,-110,-110]
dis = [358, 624, 530, 142]

con = []
tmp_offList = []
arr_offList = []
tar_x = []
tar_y = []

for i in range(2):
    for j in [i+1,i+2]:
        third = i if dis[i] > dis[j] else j  # 取長邊
        print(third)
        sec = j if third == i else i # 取短邊
        print(sec)
        x_off = x[third] - x[sec] # anchor間的 x offset
        y_off = y[third] - y[sec] # anchor間的 y offset
        print(x_off)
        print(y_off)
        anchor_dis = get_anchor_dis(x_off,y_off) #拿到兩個anchor間的距離
        print(anchor_dis)
        cur_off = get_dis(dis[sec], dis[third] , anchor_dis)
        cur_off_x = round(cur_off * x_off / anchor_dis,2)
        cur_off_y = round(cur_off * y_off / anchor_dis,2)
        print(cur_off_x)
        print(cur_off_y)
        point_x = x[third] - cur_off_x
        point_y = y[third] - cur_off_y
        if x_off == 0:
            c = point_y
            y_off = 1
        elif y_off == 0:
            c = point_x
            x_off = 1
        else:
            c = x_off * point_x + y_off * point_y
        print(c)
        con.append(c)
        tmp_offList.append(x_off)
        tmp_offList.append(y_off)
        arr_offList.append(tmp_offList)
        tmp_offList = []
    A = np.mat(arr_offList)
    arr_offList = []
    print(A)
    b = np.mat(con).T
    con = []
    print(b)
    r = np.linalg.solve(A,b)
    print(r)
    tar_x.append(round(r[0,0],2))
    tar_y.append(round(r[1,0],2))

color = ["blue","orange","green","purple",'black']
tl.speed(20)
for i in range(len(dis)):
    tl.color(color[i])
    tl.penup()
    tl.goto(x[i],y[i])
    tl.stamp()
    tl.goto(x[i],y[i]-dis[i])
    tl.pendown()
    tl.circle(dis[i])
tl.penup()
for i in range(len(tar_x)):
    tl.goto(tar_x[i],tar_y[i])
    tl.color("red")
    tl.stamp()
tl.done()






