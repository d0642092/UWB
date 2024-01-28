import pandas as pd
import numpy as np
import pickle
import subprocess as link
class ModelFunction():
    def __init__(self, root, outputFile, trainSheet, predSheet):
        self.root = root
        self.trainPath = self.root + "trainData/static.xlsx"
        self.predictPath = self.root + "trainData/dynamic.xlsx"
        self.outputPath = self.root + "trainResult/%s.xlsx" % outputFile
        self.imagePath = self.root + "img/"
        self.modelPath = "../../result/Anchor_model/"
        self.trainSheet = trainSheet
        self.predictSheet = predSheet
        self.outputSheet = "default"
    def read_data(path, sheet, anchor):
        # read training data, 1 means measured, 2 means actual
        data = pd.read_excel(io = path, sheet_name = sheet)
        X = np.array(data[anchor + "1"]).reshape(-1, 1)
        Y = np.array(data[anchor + "2"]).reshape(-1, 1)
        return X, Y
    def result_write(path, sheet, result):
        # output the prediction result
        df = pd.DataFrame(result)
        try:
            with pd.ExcelWriter(path, mode='a') as writer:
                df.to_excel(writer, sheet_name=sheet, encoding="utf_8")
        except FileNotFoundError:
            df.to_excel(path, sheet_name=sheet, encoding="utf_8")
    def store_data(predict, dict, range, anchor, ans = None):
        dict[anchor + "_range"] = range
        dict[anchor + "_pred"] = predict
        # dict[anchor + "_ans"] = ans
        return dict
    def data_show(filename, linear, larsCV, ridge, degree, anchor):
        # open file
        fp = open(filename, "a")

        # record information to file
        print(anchor + " in degree " + str(degree) + ":",file=fp)
        print("\tlinear coef: ", linear.coef_,file=fp)
        print("\tlinear intercept: ", linear.intercept_,file=fp)
        print("\n",file=fp)
        print("\tlarsCV coef: ", larsCV.coef_,file=fp)
        print("\tlarsCV intercept: ", larsCV.intercept_,file=fp)
        print("\tlarsCV alpha: ", larsCV.alpha_,file=fp)
        print("\n",file=fp)
        print("\tridge coef: ", ridge.coef_,file=fp)
        print("\tridge intercept: ", ridge.intercept_,file=fp)
        print("\tridge alpha: ", ridge.alpha_,file=fp)

        # close file
        fp.close()

    def linspace(start, end, count):
        return np.linspace(start,end,count)

    def model_save(self, regressionName ,modelName , model):
        pickle.dump(model[regressionName], open(self.modelPath + modelName + ".sav", 'wb'))
        return None

    def link_program(program,v1=None, v2=None, v3=None,v4=None):

        # linking to other python file
        command = "python " + program +" "+ v1 + " " + v2 + " " + v3 + " " + v4
        ret = link.run(command)
        if ret.returncode == 0:
            print("success:", ret)
        else:
            print("error:", ret)
        return None