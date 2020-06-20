from PointCalculation import pointCalculation
import turtle as tl
import threading
from catEmulator import anchor_DisQ
import pygame

# ---------------------------   PointCalculation_Set   -------------------------
anchor_x = [200 , 400 , 400 , 200]
anchor_y = [200 , 200 , 400 , 400]
anchor_Dis = []
pc = pointCalculation(anchor_x,anchor_y,anchor_Dis)
anchorGroups = pc.get_group(4)
# ---------------------------   PointCalculation_Set   -------------------------
color = ["blue","black","green","purple"]

class catTraceT(threading.Thread):
    def __init__(self,name = "catTrace",flag = True):
        threading.Thread.__init__(self)
        self.name = name
        self.flag = flag
    def run(self):
        # ---------------------------   DrawInit       -------------------------
        tl.screensize(64 * 20, 64 * 16)
        tl.speed(5)
        tl.penup()
        canvas = tl.getcanvas()
        canvas.config(xscrollincrement = str(100))
        canvas.config(yscrollincrement = str(100))
        canvas.yview_scroll(-2,'unit')
        canvas.xview_scroll(2,'unit')
        for i in range(len(anchor_x)):
            tl.color(color[i])
            tl.goto(anchor_x[i],anchor_y[i])
            tl.stamp()
        tl.color("red")
        # ---------------------------   DrawInit       -------------------------

        # ---------------------------   LocateByCode   -------------------------       
        while True:
            while anchor_DisQ.qsize() == 0 and self.flag:
                pass
            if not self.flag:
                break
            distances = anchor_DisQ.get()
            pc.set_dis(distances)
            points = pc.get_cal_array(anchorGroups)
            if points is None:
                continue
            try:
                finalPoint = pc.get_close_point(points)
            except ValueError as e:
                print(repr(e))
            tl.goto(finalPoint)
            tl.stamp()
        
        # ---------------------------   LocateByCode   ------------------------- 