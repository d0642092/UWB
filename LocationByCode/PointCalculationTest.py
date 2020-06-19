import unittest
from PointCalculation import pointCalculation

class PCtest(unittest.TestCase):

    anchors_x = [100,100,-100,-100]
    anchors_y = [100,-100,-100,100]
    anchors_dis = [70.7,70.7,70.7,70.7]
    PC = pointCalculation(anchors_x,anchors_y,anchors_dis)

    def test_get_cos_1(self):
        res = self.PC.get_cos(1.73,2,1) # cos(30)
        self.assertEqual(res,0.87)

    def test_get_cos_2(self):
        res = self.PC.get_cos(1,2,1.73) # cos(60)
        self.assertEqual(res,0.5)

    def test_get_dis_1(self):
        res = self.PC.get_dis(1.73,2,1) #  1.73 * cos(30)
        self.assertEqual(res,1.51)

    def test_get_dis_2(self):
        res = self.PC.get_dis(1,2,1.73) # 1 * cos(60)
        self.assertEqual(res,0.5)

    def test_get_anchor_dis(self):
        res = self.PC.get_anchor_dis(3,4)
        self.assertEqual(res, 5)

    def test_get_group(self):
        res = self.PC.get_group(3)
        ans = [[0,1,2]]
        self.assertEqual(res,ans)
    
    def test_get_group_ValueError(self):
        with self.assertRaises(ValueError):
            self.PC.get_group(2)

    def test_get_cal_array(self):
        res = self.PC.get_cal_array(self.PC.get_group(4))
        print(res)
        ans = [[0,0]]*4
        self.assertEqual(res,ans)
    # def test_get_point(self):
    #     
    # def test_get_colse_point(self):
    #     

if __name__ == "__main__":
        unittest.main()  # py .\PointCalculationTest.py -v         -->      use -v to get more information

