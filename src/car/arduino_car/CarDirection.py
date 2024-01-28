import math


class coreJudge():
    def __init__(self):
        self.command = '90+90'
        self.servo1 = 90
        self.servo2 = 90
        self.carbackWaitNotToHazard = 0
        self.range = 50.0
    def absMath(self, num: float):
        if num < 0:
            return -num
        else:
            return num

    def quardrantCal(self, x, y):
        if x >= 0 and y >= 0:
            return 1
        elif x < 0 and y >= 0:
            return 2
        elif x < 0 and y < 0:
            return 3
        elif x >= 0 and y < 0:
            return 4

    def angletanCal(self, x, y):
        if x != 0:
            return math.atan((self.absMath(y) / self.absMath(x))) / math.pi * 180
        else:
            return 90

    def getlastcoord(self, direct: str):
        while direct.split('\\', 1)[1] != '':
            direct = direct.split('\\', 1)[1]
        return direct.split('\\', 1)[0]

    def getcommand(self, x, y):
        defineRangeShort = float(self.range)  # 近距離
        defineRangeLong = float(self.range+50)  # 遠距離
        Dis: float = math.sqrt(x*x + y*y)  # 距離
        angletan = self.angletanCal(x, y)  # x, y軸 tan夾角
        quardrant = self.quardrantCal(x, y)  # 象限
        # Case 1
        if Dis <= defineRangeShort:
            # 小於 100 cm
            self.servo1 = 90
            self.servo2 = 90
            print("目的地上")
            self.carbackWaitNotToHazard = 0
        # Case 2
        elif defineRangeShort < Dis <= defineRangeLong or (self.carbackWaitNotToHazard > 0 and (quardrant == 3 or quardrant == 4)):
            print("近距離", end='')
            # 小於 200 cm, 正前方 30度夾角
            if ((quardrant == 1 or quardrant == 2 ) and 75 <= angletan <= 90):
                self.servo1 = 105 + (75 * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort)))
                self.servo2 = 75 - (75 * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort)))
                print("正前方")
                self.carbackWaitNotToHazard = 0
            # 小於 200 cm, 正後方 30度夾角
            elif ((quardrant == 3 or quardrant == 4 ) and 75 <= angletan <= 90):
                # 需要在這裡避免迴轉, 倒車loop
                if self.carbackWaitNotToHazard > 0:
                    if defineRangeLong < Dis < defineRangeLong * 1.5:
                        Dis = defineRangeLong
                    elif defineRangeLong * 1.5 < Dis:
                        self.carbackWaitNotToHazard = 0
                        Dis = defineRangeLong
                    self.carbackWaitNotToHazard = (self.carbackWaitNotToHazard) % 20
                self.carbackWaitNotToHazard += 1
                self.servo1 = 75 - (75 * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort)))
                self.servo2 = 105 + (75 * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort)))
                print("正後方")
            # 小於 200 cm, 右前方 75度夾角
            elif quardrant == 1 and 0 <= angletan < 75:
                self.servo1 = 105 + (75 * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort)))
                self.servo2 = 75 - (angletan * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort))) if 45 < angletan < 75 else 120 + (((30/45) * (45 - angletan)) * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort)))
                print("右前方")
                self.carbackWaitNotToHazard = 0
            # 小於 200 cm, 右後方 90度夾角(包含正後方)
            elif quardrant == 4 and 0 <= angletan <= 90:
                # 需要在這裡避免迴轉, 倒車loop
                if self.carbackWaitNotToHazard > 0:
                    if defineRangeLong < Dis < defineRangeLong * 1.5:
                        Dis = defineRangeLong
                    elif defineRangeLong * 1.5 < Dis:
                        self.carbackWaitNotToHazard = 0
                        Dis = defineRangeLong
                    self.carbackWaitNotToHazard = (self.carbackWaitNotToHazard) % 20
                self.carbackWaitNotToHazard += 1
                self.servo1 = 75 - (75 * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort)))
                self.servo2 = 105 + (((75/90)*angletan) * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort))) if 45 < angletan < 75 else 60 - (((30/45) * (45 - angletan)) * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort)))
                print("右後方")
                if (75 - self.servo1) > (self.servo2 - 105):
                    print("左後輪強")
                else:
                    print("左後輪弱")
            # 小於 200 cm, 左前方 75度夾角
            elif quardrant == 2 and 0 <= angletan < 75:
                # A(a>b true) if a>b else B (a>b false)
                self.servo1 = 105 + (angletan * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort))) if 45 < angletan < 75 else 60 - (((30/45) * (45 - angletan)) * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort)))
                self.servo2 = 75 - (75 * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort)))
                print("左前方")
                self.carbackWaitNotToHazard = 0
            # 小於 200 cm, 左後方 90度夾角(不包含正後方)
            elif quardrant == 3 and 0 <= angletan <= 90:
                # 需要在這裡避免迴轉, 倒車loop
                if self.carbackWaitNotToHazard > 0:
                    if defineRangeLong < Dis < defineRangeLong * 1.5:
                        Dis = defineRangeLong
                    elif defineRangeLong * 1.5 < Dis:
                        self.carbackWaitNotToHazard = 0
                        Dis = defineRangeLong
                    self.carbackWaitNotToHazard = (self.carbackWaitNotToHazard) % 20
                self.carbackWaitNotToHazard += 1
                self.servo1 = 75 - (((75/90)*angletan) * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort))) if 45 < angletan < 75 else 120 + (((30/45) * (45 - angletan)) * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort)))
                self.servo2 = 105 + (75 * ((Dis - defineRangeShort) / (defineRangeLong - defineRangeShort)))
                print("左後方")
                if (75 - self.servo1) > (self.servo2 - 105):
                    print("左後輪強")
                else:
                    print("左後輪弱")
        # Case 3
        elif defineRangeLong < Dis:
            print("遠距離", end='')
            self.carbackWaitNotToHazard = 0
            # 大於 200 cm, 正前方 30度夾角
            if ((quardrant == 1 or quardrant == 2 ) and 75 <= angletan <= 90):
                self.servo1 = 180
                self.servo2 = 0
                print("正前方")
            # 大於 200 cm, 右前方 75 度夾角
            elif quardrant == 1 and 0 <= angletan < 75:
                self.servo1 = 180
                self.servo2 = (60/75) * (75 - angletan)
                print("右前方")
            # 大於 200 cm, 右後方 90 度夾角(包含正後方)
            elif quardrant == 4 and 0 <= angletan < 90:
                self.servo1 = 180
                self.servo2 = 120
                print("右後方")
            # 大於 200 cm, 左前方 75 度夾角
            elif quardrant == 2 and 0 <= angletan < 75:
                self.servo1 = 120 + ((60/75) * angletan)
                self.servo2 = 0
                print("左前方")
            # 大於 200 cm, 左後方 90 度夾角(不包含正後方)
            elif quardrant == 3 and 0 <= angletan < 90:
                self.servo1 = 60
                self.servo2 = 0
                print("左後方")

        self.command = str(int(self.servo1)) + '+' + str(int(self.servo2))
        print("象限:{}, 角度:{}".format(quardrant, angletan))
        print("Hazard:{}".format(self.carbackWaitNotToHazard))


    def direction(self, position: str):
        XandY: str = self.getlastcoord(position)
        x = float(XandY.split(',', 1)[0])
        y = float(XandY.split(',', 1)[1])
        self.getcommand(x, y)

# if __name__ == '__main__':
#     pass
