from sklearn.linear_model import LinearRegression, LassoLarsCV, RidgeCV
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
from .classes.modelFunction import ModelFunction
from .classes.drawImage import DrawImage

if __name__ == "__main__":
    mf = ModelFunction(
        root = "../../data/2020-09-08_outdoor/",
        outputFile = "Electronics2",
        trainSheet = "ignore",
        predSheet = "ignore",
    )
    MAPPING = {"An0094": "A", "An0095": "B", "An0096": "C", "An0099": "D"}
    trainDegree = [1,5,10]
    trainModel={}
    imageTitle = {1: "Linear Regression",
            3: "${3^{rd}}$ Regression",
            4: "${4^{th}}$ Regression",
            5: "${5^{th}}$ Regression",
            10: "${10^{th}}$ Regression"}
    saveDeg = 10
    saveReg = "lasso"

    # lasso, ridge
    C = 15
    # ridge
    A = mf.linspace(0,1,11)
    for deg in trainDegree:
        position = DrawImage.init_image(deg, imageTitle)
        mf.outputSheet = mf.predictSheet + str(deg)
        predResult = {"linear":{},"lasso":{},"ridge":{},"svr":{}}
        trainResult = {}
        for anchor, notation in MAPPING.items():
            xTrain, yTrain = mf.read_data(mf.trainPath, mf.trainSheet, notation)
            xPred, yPred = mf.read_data(mf.predictPath, mf.predictSheet, notation)
            xSort = sorted(xTrain)
            quadraticFeaturizer = PolynomialFeatures(deg)
            xPoly_d = quadraticFeaturizer.fit_transform(xTrain)
            xPrediction_d = quadraticFeaturizer.fit_transform(xPred)

            # Linear Regression #
            linear = LinearRegression()
            linear.fit(xPoly_d, yTrain)
            trainResult["linear"] = linear.predict(quadraticFeaturizer.transform(xSort)).reshape(-1, )
            predResult["linear"] = mf.store_data(linear.predict(xPrediction_d).reshape(-1,), predResult["linear"], xPred.reshape(-1,), notation,  yPred.reshape(-1,))
            trainModel["linear"] = linear
            # Linear Regression #

            # Lasso #
            lars = LassoLarsCV(cv=C)
            lars.fit(xPoly_d, yTrain)
            trainResult["lasso"] = lars.predict(quadraticFeaturizer.transform(xSort)).reshape(-1, )
            predResult["lasso"] = mf.store_data(lars.predict(xPrediction_d).reshape(-1, ), predResult["lasso"], xPred.reshape(-1, ), notation, yPred.reshape(-1, ))
            trainModel["lasso"] = lars
            # Lasso #

            # Ridge #
            ridge = RidgeCV(alphas=A, cv=C)
            ridge.fit(xPoly_d, yTrain)
            trainResult["ridge"] = ridge.predict(quadraticFeaturizer.transform(xSort)).reshape(-1, )
            predResult["ridge"] = mf.store_data(ridge.predict(xPrediction_d).reshape(-1, ), predResult["ridge"], xPred.reshape(-1, ), notation, yPred.reshape(-1, ))
            trainModel["ridge"] = ridge
            # Ridge #

            # SVR #
            # svr = SVR(kernel="linear") if deg == 1 else SVR(kernel="poly", degree=deg, coef0=10)
            # print(deg)
            # svr.fit(xTrain, yTrain)
            # trainResult["svr"] = svr.predict(xSort).reshape(-1,)
            # predResult["svr"] = mf.store_data(svr.predict(xPred).reshape(-1,), predResult["svr"], xPred.reshape(-1,), notation, yPred.reshape(-1,))
            # SVR #
            # mf.data_show("./model_detail2.txt",linear, lars,ridge, deg, anchor)
            if deg == saveDeg:
                mf.model_save(saveReg, anchor, trainModel)
            DrawImage.subimage_create(position, anchor, xTrain, yTrain, xSort, trainResult)
            position += 1
        mf.result_write(mf.outputPath, "linear" + mf.outputSheet, predResult["linear"])
        mf.result_write(mf.outputPath, "Lasso" + mf.outputSheet, predResult["lasso"])
        mf.result_write(mf.outputPath, "Ridge" + mf.outputSheet, predResult["ridge"])
        # mf.result_write(mf.outputPath, "SVR" + mf.outputSheet, predResult["svr"])
        DrawImage.save_and_show(mf.imagePath, "Degree%d.png" % deg)