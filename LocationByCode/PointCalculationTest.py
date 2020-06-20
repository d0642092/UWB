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
        Dis = [70.7]*3
        self.PC.set_dis(Dis)
        res = self.PC.get_cal_array(self.PC.get_group(3))
        ans = [0,0]
        for i in range(len(ans)):
            self.assertAlmostEqual(res[0][i],ans[i],delta=2)

    def test_get_cal_array1(self):
        Dis = [100,100,223.6]
        self.PC.set_dis(Dis)
        res = self.PC.get_cal_array(self.PC.get_group(3))
        ans = [100,0]
        for i in range(len(ans)):
            self.assertAlmostEqual(res[0][i],ans[i],delta=2)

    def test_get_cal_array2(self):
        Dis = [223.606,100,100]
        self.PC.set_dis(Dis)
        res = self.PC.get_cal_array(self.PC.get_group(3))
        ans = [0,-100]
        for i in range(len(ans)):
            self.assertAlmostEqual(res[0][i],ans[i],delta=2)

    def test_get_cal_array3(self):
        Dis = [316.22,316.22,141.4213]
        self.PC.set_dis(Dis)
        res = self.PC.get_cal_array(self.PC.get_group(3))
        ans = [-200,0]
        for i in range(len(ans)):
            self.assertAlmostEqual(res[0][i],ans[i],delta=2)

    def test_get_cal_array4(self):
        Dis = [111.8,180.26,180.26,111.8]
        self.PC.set_dis(Dis)
        res = self.PC.get_cal_array(self.PC.get_group(3))
        ans = [0,50]
        for i in range(len(ans)):
            self.assertAlmostEqual(res[0][i],ans[i],delta=2)

    def test_get_point(self):
        x = 50
        y = 50
        points = [[x,y],[x,-y],[-x,-y],[-x,y]]
        res = self.PC.get_point(points)
        ans = [0,0]
        for i in range(len(ans)):
            self.assertAlmostEqual(res[i],ans[i],delta=0.1)

    def test_get_colse_point1(self):
        x = 10
        y = 10
        points = [[x,y],[x,-y],[-x,-y],[-x,y]]
        res = self.PC.get_close_point(points)
        ans = [0,0]
        for i in range(len(ans)):
            self.assertAlmostEqual(res[i],ans[i],delta=0.1)

    def test_get_colse_point2(self):
        x = 10
        y = 10
        points = [[x,y],[x,-y],[-x,-y],[-6*x,y]]
        res = self.PC.get_close_point(points)
        ans = [3.3,-3.3]
        for i in range(len(ans)):
            self.assertAlmostEqual(res[i],ans[i],delta=0.1)
    
    def test_get_colse_pointException(self):
        with self.assertRaises(ValueError):
            x = 20
            y = 20
            points = [[x,y],[x,-y],[-x,-y],[-2*x,y]]
            self.PC.get_close_point(points)

if __name__ == "__main__":
        unittest.main()  # py .\PointCalculationTest.py -v         -->      use -v to get more information

