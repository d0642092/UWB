import math
import serial
import socket

def absMath(num):
    if(num < 0):
        return -num
    else:
        return num


class coreJudge():
    def __init__(self):
        self.turnPower = 1  # 旋轉功率
        self.shiftPower = 1  # 平移功率
        self.lastdisFlag = 2  # 更遠或更近: '0' 目的地上, '1' 近, '2' 遠
        self.disFlag = 2
        self.lastturnFlag = 2  # 上一次的前進方位
        self.turnFlag = 2  # 本次的前進方位

    def update(self):
        self.lastturnFlag = self.turnFlag
        self.lastdisFlag = self.disFlag

    def turnflagOverJudge(self):
        # strongWeakFlag>>> '1' 太強, '0' 太弱, '2' 無須調整
        strongWeakFlag = 2
        if 3 >= self.lastturnFlag >= 1:
            # 左旋轉太強
            if 7 >= self.turnFlag >= 4:
                strongWeakFlag = 1
            elif self.lastturnFlag == 1 and self.turnFlag-self.lastturnFlag >= 1:
                strongWeakFlag = 1
            elif self.lastturnFlag == 2 and self.turnFlag-self.lastturnFlag >= 1:
                strongWeakFlag = 1
            # 左旋轉太弱
            elif self.lastturnFlag == 3 and self.turnFlag == 3:
                strongWeakFlag = 0
                pass
        elif 6 >= self.turnFlag >= 4 and self.turnFlag - self.lastturnFlag < 0:
            # 右旋轉太強
            if 3 >= self.turnFlag >= 1:
                strongWeakFlag = 1
            elif self.lastturnFlag == 4 and self.turnFlag - self.lastturnFlag >= 1:
                strongWeakFlag = 1
            elif self.lastturnFlag == 5 and self.turnFlag - self.lastturnFlag >= 1:
                strongWeakFlag = 1
            # 右旋轉太弱
            elif self.lastturnFlag == 6 and self.turnFlag == 6:
                strongWeakFlag = 0
        return strongWeakFlag

    def direction(self, x, y):
        # ===========判斷方向===========
        slopeFlag = 0
        turnFlag = 0

        # 判斷如何接近目標
        # 判斷離y軸多少
        if x == 0:
            slopeFlag = 0
        elif absMath(y) / absMath(x) >= math.tan(math.radians(80)):
            slopeFlag = 1
        elif absMath(y) / absMath(x) >= math.tan(math.radians(30)):
            slopeFlag = 2
        else:
            # include y==0
            slopeFlag = 3
        # 判斷是在哪個定義的旋轉區域
        if slopeFlag <= 1:
            if y > 0:
                turnFlag = 0
            elif y < 0:
                turnFlag = 7
        elif slopeFlag == 2:
            if x > 0:
                if y > 0:
                    turnFlag = 1
                elif y < 0:
                    turnFlag = 3
            elif x < 0:
                if y > 0:
                    turnFlag = 4
                elif y < 0:
                    turnFlag = 6
        elif slopeFlag == 3:
            if x > 0:
                turnFlag = 2
            elif x < 0:
                turnFlag = 5

        # 當遠離時, 大於等於900cm
        if (x * x) + (y * y) >= 40000:
            self.disFlag = 2  # In Case: 遠離中
            print('遠距離')
            if turnFlag == 0:
                # 正前進
                print('正前方...')
            elif turnFlag == 1:
                # 弱功率右旋轉
                print('右前方...')
            elif turnFlag == 2:
                # 中功率右旋轉
                print('右方...')
            elif turnFlag == 3:
                # 強功率右旋轉
                print('右後方')
            elif turnFlag == 4:
                # 弱功率左旋轉
                print('左前方...')
            elif turnFlag == 5:
                # 中功率左旋轉
                print('左方...')
            elif turnFlag == 6:
                # 強功率左旋轉
                print('左後方')
            elif turnFlag == 7:
                print('後方')
        # 接近時
        elif (x * x) + (y * y) >= 10000:
            self.disFlag = 1  # In Case: 接近中
            print('近距離')
            if turnFlag == 0:
                # 正前進
                print('前方...')
            elif 3 >= turnFlag >= 1:
                print('右方')
            elif 6 >= turnFlag >= 4:
                print('左方')
            elif turnFlag == 7:
                print('後方')
        # 幾乎在目的地上
        else:
            self.disFlag = 0  # In Case: 目的地中
            print('在目的地上')
            if turnFlag == 0:
                print('無須校正')
            elif 3 >= turnFlag >= 1:
                print('右旋轉校正')
            elif 6 >= turnFlag >= 4:
                print('左旋轉校正')
            elif turnFlag == 7:
                print('右旋轉校正')

        # 設定旋轉方向
        self.turnFlag = turnFlag

if __name__ == '__main__':
    test = coreJudge()
    print(test.disFlag)
