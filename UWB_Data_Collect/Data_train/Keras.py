from keras.datasets import fashion_mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras.layers.core import Dense,Flatten
from keras.layers import Dense, LSTM
# from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas


# sheet_name = ["200x200_An96_340", "100x100_An96_81"]
# sheet_name = []
train_data = []
real_data = []
data = pandas.read_excel('D:/Python/UWB_Data_Collect/Data_train/王泓文_2020-05-30 08-47-320.XLSX', sheet_name="YuXiang_1")
print(data.head())
# for i in range(2):
#     for j in range(25):
#         tempList=[]
#         y_train1.append(df.iloc[i+j][5])
#         for k in range(6,13):
#             tempList.append(df.iloc[i+j][k])
#         x_train1.append(tempList)
#
# x_train1 = np.reshape(x_train1, (len(x_train1),1,7))
# y_train1 = np.reshape(y_train1, (len(y_train1),1))
#
#
# model1 = Sequential()
# model1.add(LSTM(128,input_shape=(1,7)))
# model1.add(Dense(64,activation='relu'))
# model1.add(Dense(32,activation='relu'))
# model1.add(Dense(1,activation='relu'))
# model1.compile(loss = 'mse',optimizer="adam",metrics=['mse'])
# model1.fit(x_train1,y_train1,batch_size=8,epochs=200,validation_split=0.2)