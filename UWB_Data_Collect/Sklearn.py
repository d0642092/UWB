import pandas
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.isotonic import IsotonicRegression
from sklearn import metrics
import matplotlib.pyplot as plt

# sheet_name = ["200x200_An96_340", "100x100_An96_81"]
# sheet_name = ["100x100_An94_80", "100x100_An96_81", "100x100_An94_92", "100x100_An96_87", "100x100_An96_230",
#               "150x150_An96_100", "150x150_An96_144", "150x150_An96_255", "200x200_An96_302", "200x200_An96_250",
#               "200x200_An96_340"]
train_data = []
real_data = []
area_data = []

def train(train_data,real_data):
    # train_data = np.array(train_data)
    # real_data = np.array(real_data)
    # X = train_data.reshape(-1, 1)
    # y = real_data.reshape(-1, 1)
    X_train, X_test, y_train, y_test = train_test_split(train_data, real_data, test_size=0.2, random_state=None)
    # model = LinearRegression()
    model = IsotonicRegression()
    print(X_train)
    model.fit(X_train, y_train)  # training the algorithm
    # coeff_df = pandas.DataFrame(model.coef_,["Distance","Area"], columns=['Coefficient'])
    # print(coeff_df)
    y_pred = model.predict(X_test)
    print(X_test)
    df = pandas.DataFrame({'Actual': y_test, 'Predicted': y_pred, 'distance': X_test})
    # print("OK")
    # print(df)
    # print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
    # print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
    # print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

    # plt.scatter(X_test[:,:1], y_test, color='gray')
    # plt.plot(X_test[:,:1], y_pred, color='red', linewidth=2)
    #
    # plt.scatter(X_test, y_test, color='gray')
    # plt.plot(X_test, y_pred, color='red', linewidth=2)
    # plt.show()
    # df.to_excel("An0011_train.xlsx",encoding="utf-8")
    try:
        with pandas.ExcelWriter('Linear_lose_train95.xlsx', mode='a') as writer:
            df.to_excel(writer, sheet_name='0.2', encoding="utf_8")
    except FileNotFoundError:
        df.to_excel('Linear_lose_train95.xlsx', sheet_name='0.2', encoding="utf_8")


data = pandas.read_excel('D:/Python/UWB_Data_Collect/Data_train/All_data(200).xlsx')
# train_data.extend(data[["An0095","誤差2"]].values)
# print(train_data)
real_data.extend(data["Real95"])
# real_data.extend(data["誤差2"])
# print(real_data)
train_data.extend(data["An0095"])
area_data.extend(data["Area"])
# print(train_data)
tmp = []
for i,value in enumerate(train_data):
    if value == 0:
        tmp.append(i)
tmp.sort(reverse=True)
for i in tmp:
    train_data.pop(i)
    real_data.pop(i)
    area_data.pop(i)
# train_data = np.hstack([np.array(train_data)[:,np.newaxis],np.array(area_data)[:,np.newaxis]])
# print(train_data)
# real_data = np.array(real_data)
# print(train_data[:,:1])
# print(train_data)

train(train_data, real_data)





