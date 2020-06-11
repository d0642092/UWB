import math
import numpy as np
import turtle as tl

class pointCalculation():
    def __init__(self,anchors_x,anchors_y,anchors_dis):
        self.anchors_x = anchors_x
        self.anchors_y = anchors_y
        self.anchors_dis = anchors_dis
    
    def set_dis(self,anchors_dis):
        self.anchors_dis = anchors_dis

    def set_XandY(self,anchors_x,anchors_y):
        self.anchors_x = anchors_x
        self.anchors_y = anchors_y

    def get_cos(self,a,b,c):
        tmp = math.pow(a,2) + math.pow(b,2) - math.pow(c,2)
        div = 2 * a * b
        return round(tmp / div , 2) # cos(c)

    def get_dis(self,a,b,c):
        return round(a * self.get_cos(a,b,c),2)

    def get_anchor_dis(self,x_off,y_off):
        return round(math.sqrt(math.pow(x_off,2) + math.pow(y_off,2)),2)

    def get_group(self,anchor_numbers):
        ans = []
        tmp = []
        for i in range(anchor_numbers):
            for j in range(i+1,anchor_numbers):
                for n in range(j+1,anchor_numbers):
                    tmp.append(i)
                    tmp.append(j)
                    tmp.append(n)
                    ans.append(tmp.copy())
                    tmp.clear()
        return ans

    def get_cal_array(self,anchor_groups):
        constList = []
        paraArray = []
        paraTmp = []
        ansPoint = []
        for group in anchor_groups:
            startAnchor = group[0]
            for i in group[1:]:
                endAnchor = i
                x_off = self.anchors_x[startAnchor] - self.anchors_x[endAnchor]
                y_off = self.anchors_y[startAnchor] - self.anchors_y[endAnchor]
                # x * x_off + y * y_off = const
                dis_between_start_end = self.get_anchor_dis(x_off,y_off)
                dis_start = self.anchors_dis[startAnchor]
                dis_end = self.anchors_dis[endAnchor]
                cur_off = self.get_dis(dis_start,dis_between_start_end,dis_end)
                proportion = round(cur_off / dis_between_start_end , 2)
                cur_off_x = x_off * proportion
                cur_off_y = y_off * proportion
                point_x = self.anchors_x[startAnchor] - cur_off_x
                point_y = self.anchors_y[startAnchor] - cur_off_y
                if x_off == 0:
                    const = point_y
                    y_off = 1
                elif y_off == 0:
                    const = point_x
                    x_off = 1
                else:
                    const = point_x * x_off + point_y * y_off
                paraTmp.append(x_off)
                paraTmp.append(y_off)
                paraArray.append(paraTmp.copy())
                constList.append(const)
                paraTmp.clear()
            A = np.mat(paraArray)
            paraArray.clear()
            b = np.mat(constList).T
            constList.clear()
            r = np.linalg.solve(A,b)
            ansPoint.append([r[0,0],r[1,0]])
        return ansPoint
    
    def draw_init(self):
        color = ["blue","yellow","green","purple",'black']
        tl.speed(5)
        for i in range(len(self.anchors_dis)):
            tl.color(color[i])
            tl.penup()
            tl.goto(self.anchors_x[i],self.anchors_y[i])
            tl.stamp()

    def draw_move_line(self,points):
        tl.color("grey")
        tl.penup()
        for point in points:
            tl.goto(point[0],point[1])
            tl.stamp()
        tl.done()
    
    def get_point(self,points):
        sum_X = 0
        sum_Y = 0
        for i in points:
            sum_X += i[0]
            sum_Y += i[1]
        return [ sum_X / len(points) , sum_Y / len(points)]


    def get_close_point(self,points): # undone , I need to think
        mark = [0] * len(points)
        #color = list(range(len(points)))
        offset = 100
        for i in range(len(points)):
            x = points[i][0]
            y = points[i][1]
            for j in range(len(points)):
                if i == j:continue
                else:
                    test_x = points[j][0]
                    test_y = points[j][1]
                    if x + offset > test_x and test_x > x - offset and y + offset > test_y and test_y > y - offset:
                        mark[j] += 1
        maxIndex = 0
        max = 0
        for i in range(len(mark)):
            if mark[i] > max:
                max = mark[i]
                maxIndex = i
        x = points[maxIndex][0]
        y = points[maxIndex][1]
        max_X = points[maxIndex][0]
        max_Y = points[maxIndex][1]
        for j in range(len(points)):
                if maxIndex == j:continue
                else:
                    test_x = points[j][0]
                    test_y = points[j][1]
                    if x + offset > test_x and test_x > x - offset and y + offset > test_y and test_y > y - offset:
                        max_X += points[j][0]
                        max_Y += points[j][1]
        if mark[maxIndex] != 0:
            raise ValueError("Bad Points",points)
        mark[maxIndex] += 1
        return [max_X / mark[maxIndex]  , max_Y / mark[maxIndex]]
                        
                        


        