import pygame, time
from pygame.locals import *
import queue
import threading
import math

#使用說明
#使用鍵盤"上下左右"控制貓貓
#另一視窗會顯示貓貓移動路徑
#上下相反是由於兩個視窗的(0,0)不同，貓貓在左上角，路徑在左下角
#關閉請直接關閉貓貓視窗，路徑視窗會自動關閉

anchor_x = [200 , 400 , 400 , 200]
# anchor_y = [312 , 312 , 112 , 112]
anchor_y = [200 , 200 , 400 , 400]

def get_dis(x_off,y_off):
    return round(math.sqrt(math.pow(x_off,2) + math.pow(y_off,2)),2)

def cal_Dis(x,y):
    ans = []
    for i in range(4):
        dis = get_dis((anchor_x[i] - x),(anchor_y[i] - y))
        if dis == 0:
            dis += 1
        ans.append(dis)
    return ans

anchor_DisQ = queue.Queue()

class catEmulatorT(threading.Thread):
    def __init__(self,name = "catEmulator",flag = True):
        threading.Thread.__init__(self)
        self.name = name
        self.flag = flag

    def run(self):

        pygame.init()
        pygame.font.init()

        width,height = 64*10, 64*8
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Pygame Cat Emulator')
        pygame.mouse.set_visible(0)
        cur_X = 200
        cur_Y = 200

        keyPressed = [False,False,False,False]

        cat = pygame.image.load("cat.jpg")
        marker = pygame.image.load("marker.jpg")

        while self.flag:
            # print("doing a function")
            screen.fill((255,255,255)) # 清空畫面
            for i in range(4):
                screen.blit(marker,(anchor_x[i],anchor_y[i]))
            screen.blit(cat,(cur_X,cur_Y)) # 顯示貓
            pygame.display.flip() #更新畫面

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.flag = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        keyPressed[0] = True
                    elif event.key == pygame.K_DOWN:
                        keyPressed[1] = True
                    elif event.key == pygame.K_LEFT:
                        keyPressed[2] = True
                    elif event.key == pygame.K_RIGHT:
                        keyPressed[3] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        keyPressed[0] = False
                    elif event.key == pygame.K_DOWN:
                        keyPressed[1] = False
                    elif event.key == pygame.K_LEFT:
                        keyPressed[2] = False
                    elif event.key == pygame.K_RIGHT:
                        keyPressed[3] = False

            if keyPressed[0]:
                if cur_Y > 0:
                    cur_Y -= 15
            elif keyPressed[1]:
                if cur_Y < height - 64:
                    cur_Y += 15
            elif keyPressed[2]:
                if cur_X > 0:
                    cur_X -= 15
            elif keyPressed[3]:
                if cur_X < width - 64:
                    cur_X += 15
            anchor_DisQ.put(cal_Dis(cur_X,cur_Y))
            time.sleep(0.1)
