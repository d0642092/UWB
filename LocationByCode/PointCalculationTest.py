import unittest
from PointCalculation import pointCalculation

class PCtest(unittest.TestCase):

    anchors_x = [100,100,-100,-100]
    anchors_y = [100,-100,-100,100]
    anchors_dis = [70.7,70.7,70.7,70.7]
    PC = pointCalculation()
    PC.set_XandY(anchors_x,anchors_y)

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
        Dis = [141.4]*3
        self.PC.set_dis(Dis)
        res = self.PC.get_cal_array(self.PC.get_group(3))
        ans = [0,0]
        for i in range(len(ans)):
            self.assertAlmostEqual(res[0][i],ans[i],delta=5)

    def test_get_cal_array1(self):
        Dis = [100,100,223.6]
        self.PC.set_dis(Dis)
        res = self.PC.get_cal_array(self.PC.get_group(3))
        ans = [100,0]
        for i in range(len(ans)):
            self.assertAlmostEqual(res[0][i],ans[i],delta=5)

    def test_get_cal_array2(self):
        Dis = [223.6,100,100]
        self.PC.set_dis(Dis)
        res = self.PC.get_cal_array(self.PC.get_group(3))
        ans = [0,-100]
        for i in range(len(ans)):
            self.assertAlmostEqual(res[0][i],ans[i],delta=5)

    def test_get_cal_array3(self):
        Dis = [316.22,316.22,141.42]
        self.PC.set_dis(Dis)
        res = self.PC.get_cal_array(self.PC.get_group(3))
        ans = [-200,0]
        for i in range(len(ans)):
            self.assertAlmostEqual(res[0][i],ans[i],delta=5)

    def test_get_cal_array4(self):
        Dis = [111.8,180.26,180.26,111.8]
        self.PC.set_dis(Dis)
        res = self.PC.get_cal_array(self.PC.get_group(3))
        ans = [0,50]
        for i in range(len(ans)):
            self.assertAlmostEqual(res[0][i],ans[i],delta=5)

    def test_get_cal_array5(self):
        Dis = [316.22,316.22,141.42,141.42]
        self.PC.set_dis(Dis)
        res = self.PC.get_cal_array(self.PC.get_group(4))
        ans = [[-200,0]] * 4
        for i in range(4):
            for j in range(2):
                self.assertAlmostEqual(res[i][j],ans[i][j],delta=5)

    def test_get_cal_array6(self):
        Dis = [111.8,180.26,180.26,111.8]
        self.PC.set_dis(Dis)
        res = self.PC.get_cal_array(self.PC.get_group(4))
        ans = [[0,50]] * 4
        for i in range(4):
            for j in range(2):
                self.assertAlmostEqual(res[i][j],ans[i][j],delta=5)

    def test_get_cal_arrayfitError1(self):
        Dis = [50,50,50]
        self.PC.set_dis(Dis)
        res = self.PC.get_cal_array(self.PC.get_group(3))
        self.assertEqual(res,None)

    def test_get_cal_arrayfitSuccess1(self):
        Dis = [90,90,223.6]
        self.PC.set_dis(Dis)
        res = self.PC.get_cal_array(self.PC.get_group(3))
        ans = [100,0]
        for i in range(len(ans)):
            self.assertAlmostEqual(res[0][i],ans[i],delta=5)

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

    def test_fitTriangle1(self):
        res = self.PC.fitTriangle(160,70,70)
        ans = [160,80,80]
        self.assertEqual(res,ans)
    
    def test_fitTriangle2(self):
        res = self.PC.fitTriangle(70,160,70)
        ans = [70,150,80]
        self.assertEqual(res,ans)

    def test_fitTriangle3(self):
        res = self.PC.fitTriangle(70,70,160)
        ans = [70,80,150]
        self.assertEqual(res,ans)

    def test_fitTriangleError1(self):
        with self.assertRaises(ValueError):
            self.PC.fitTriangle(50,70,160)
    
    def test_fitTriangleError2(self):
        with self.assertRaises(ValueError):
            self.PC.fitTriangle(160,50,70)

    def test_fitTriangleError3(self):
        with self.assertRaises(ValueError):
            self.PC.fitTriangle(50,160,70)
    
if __name__ == "__main__":
        unittest.main()  # py .\PointCalculationTest.py -v         -->      use -v to get more information

