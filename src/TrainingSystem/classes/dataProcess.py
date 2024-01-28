import pandas as pd

class DataProcess():
    def __init__(self, savePath, filename, sheetname):
        self.savePath = savePath
        self.filename = filename
        self.sheetname = sheetname
        self.storeDir = self.savePath + self.filename
        # firstTime get_data has different variable
        self.firstTime = True
        pass
    def record_data(self, start ,end, throughBy=None, count=None):
        X = []
        if count==None:
            for value in range(start, end+1, throughBy):
                X.append(value)
        else:
            for value in range(count):
                X.append(start)
        return X.copy()

    def get_data(self,ws, start, end, throughBy):
        # start, end = [row, col]
        data = []
        tmp = []
        for row in range(start[0], end[0]):
            for col in range(start[1], end[1], throughBy):
                tmp.append(ws.cell(row,col).value)
            data.append(tmp.copy())
            tmp.clear()
        return data.copy()
    def cal_point(pc, data, group):
        point=[]
        dx = []
        dy = []
        for dis in data:
            pc.set_dis(dis)
            points = pc.get_cal_array(group)
            if points is None:
                continue
            try:
                point.append(pc.get_point(points))
            except ValueError as e:
                print(e)
            except TypeError as e:
                point.append(["nan", "nan"])
                print(e)
        for p in point:
            dx.append(p[0])
            dy.append(p[1])
        return dx.copy(), dy.copy()
    def remove_nan(dx, dy):
        for i in range(len(dx)):
            if "nan" in dx:
                dx.remove("nan")
                dy.remove("nan")
            else:
                break
        return None
    def data_save(self, data):
        df = pd.DataFrame(data)
        try:
            with pd.ExcelWriter(self.storeDir, mode='a') as writer:
                df.to_excel(writer, sheet_name = self.sheetname, encoding="utf_8")
        except FileNotFoundError:
            df.to_excel(self.storeDir, sheet_name = self.sheetname, encoding="utf_8")
        return None