import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt

deg = 4
# deg = 4

# sheet_name = ["100x100_An96_81", "100x100_An94_92", "100x100_An96_87", "100x100_An96_230","150x150_An96_100",
#               "150x150_An96_144", "150x150_An96_255", "200x200_An96_302", "200x200_An96_250","200x200_An96_340"]
# data = pd.DataFrame(pd.read_excel('D:/Python/UWB_Data_Collect/2020-03-21_G-print/G-print_2.xlsx', sheet_name="100x100_An94_80"))
#
# for sheet in sheet_name:
#     df1 = pd.DataFrame(pd.read_excel('D:/Python/UWB_Data_Collect/2020-03-21_G-print/G-print_2.xlsx', sheet_name=sheet))
#     data = pd.concat([data, df1])

data = pd.read_excel('D:/Python/UWB_Data_Collect/Data_train/All_data.xlsx')

train_data = data["An0095"]
real_data = data["Real95"]
area = data["Area"]
tmp_index = []
for i, values in enumerate(train_data):
    if values == 0:
        tmp_index.append(i)

tmp_index.sort(reverse=True)
for i in tmp_index:
    train_data.pop(i)
    real_data.pop(i)
    area.pop(i)

b=[]
for i in range(0, len(train_data), 5):
    b.append(train_data[i:i+5])

print(b)

# data = pd.concat([train_data, real_data, area], axis=1)
#
# train, validation = train_test_split(data, test_size=0.3, random_state=None)
#
# X_train = train.loc[:, ["An0095","Area"]].values
# X_validation = validation.loc[:, ["An0095","Area"]].values
#
# X_train_d2 = PolynomialFeatures(deg).fit_transform(X_train)
# X_validation_d2 = PolynomialFeatures(deg).fit_transform(X_validation)
# # print("X_train with degree=2:")
# # print(X_train_d2)
#
# y_train = train.loc[:, "Real95"].values.reshape(-1, 1)
# y_validation = validation.loc[:, "Real95"].values.reshape(-1, 1)
#
# reg_d1 = LinearRegression()
# reg_d1.fit(X_train, y_train)
# y_hat_1 = reg_d1.predict(X_validation)
#
# mse_d1 = mean_squared_error(y_validation, y_hat_1)
# print("MSE with degree=1: {:.0f}".format(mse_d1))
#
# reg_d2 = LinearRegression()
# reg_d2.fit(X_train_d2, y_train)
# y_hat_2 = reg_d2.predict(X_validation_d2)
# print(X_validation)
# mse_d2 = mean_squared_error(y_validation, y_hat_2)
# print("MSE with degree=4: {:.0f}".format(mse_d2))
#
#
# # X_arr = np.linspace(data[["An0095","Area"]].min(), data[["An0095","Area"]].max()).reshape(-1, 1)
# # X_arr_d1 = np.linspace(data[["An0095""Area"]].min(), data[["An0095","Area"]].max()).reshape(-1, 1)
# # X_arr_d2 = PolynomialFeatures(deg).fit_transform(X_arr)
# X_arr = train.loc[:, "An0095"].values
# y_arr = train.loc[:, "Real95"].values
# X_arr_d1 = train.loc[:, ["An0095","Area"]].values
# X_arr_d2 = PolynomialFeatures(deg).fit_transform(train.loc[:, ["An0095","Area"]].values)
# y_arr_d1 = reg_d1.predict(X_arr_d1)
# y_arr_d2 = reg_d2.predict(X_arr_d2)
# #
# plt.scatter(train["An0095"], train["Real95"], s=5, c="b", label="Train")
# plt.scatter(validation["An0095"], validation["Real95"], s=5, c="r", label="Validation")
# plt.plot(X_arr, y_arr_d1, c="c", linewidth=3, label="d=1")
# # plt.plot(X_arr, y_arr_d2, c="g", linewidth=0.1, label="d=4")
# plt.xlabel("distance")
# plt.ylabel("real")
# plt.legend(loc="upper left")
# plt.show()
#
# test = PolynomialFeatures(deg).fit_transform([[245,22500]])
# print(reg_d2.predict(test))
# print(222)
#
# test = PolynomialFeatures(deg).fit_transform([[470,60000]])
# print(reg_d2.predict(test))
# print(442)
#
# # fig = plt.figure()
# # # plt.plot(train_data, real_data, 'r.', markersize=5)
# # plt.plot(X_arr, y_arr, 'r.', markersize=10)
# # # plt.plot(X_test, y_, 'g.-', markersize=10)
# # plt.plot(X_arr_d2, y_arr_d2, 'g.', markersize=5)
# # # plt.plot(X_train, lr.predict(X_test[:, np.newaxis]), 'b-')
# # # plt.gca().add_collection(lc)
# # plt.legend(('Data', 'Data_predict'), loc='lower right')
# # plt.title('Isotonic regression')
# # plt.show()
# #
#
#
#
#
#
# # mse = mean_squared_error(y_validation, y_hat)
#
# # print("MSE of simple linear regression: {:.0f}".format(mse))
# #
# # print("Simple")
# # print([y_hat,y_validation,X_validation])
#
#
#
#
#
#
#
# # print("Multiple")
# # X_train_multiple = train.loc[:, ["An0095", "Area"]].values
# # X_validation_multiple = validation.loc[:, ["An0095", "Area"]].values
# # reg_multiple = LinearRegression()
# # reg_multiple.fit(X_train_multiple, y_train)
# # y_hat_multiple = reg_multiple.predict(X_validation_multiple)
# # mse_multiple = mean_squared_error(y_validation, y_hat_multiple)
# # print("MSE of multiple linear regression: {:.0f}".format(mse_multiple))
# # print([y_hat_multiple,y_validation,X_validation_multiple])
