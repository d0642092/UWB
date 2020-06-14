import unittest
from PointCalculation import pointCalculation

class PCtest(unittest.TestCase):

    anchors_x = [100,100,-100,-100]
    anchors_y = [100,-100,-100,100]
    anchors_dis = [70.7,70.7,70.7,70.7]
    PC = pointCalculation(anchors_x,anchors_y,anchors_dis)

    def test_get_cos_1(self):
        ans = self.PC.get_cos(1.73,2,1) # cos(30)
        self.assertEqual(ans,0.87)

    def test_get_cos_2(self):
        ans = self.PC.get_cos(1,2,1.73) # cos(60)
        self.assertEqual(ans,0.5)

    def test_get_dis_1(self):
        ans = self.PC.get_dis(1.73,2,1) #  1.73 * cos(30)
        self.assertEqual(ans,1.51)

    def test_get_dis_2(self):
        ans = self.PC.get_dis(1,2,1.73) # 1 * cos(60)
        self.assertEqual(ans,0.5)

    # def get_anchor_dis_Test(self):
    #     #
    # def get_group_Test(self):
    #     #
    # def get_cal_array_Test(self):
    #     #
    # def get_point_Test(self):
    #     #
    # def get_colse_point_Test(self):
    #     #

if __name__ == "__main__":
        unittest.main()  # py .\PointCalculationTest.py -v         -->      use -v to get more information

