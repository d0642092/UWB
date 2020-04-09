import numpy as np
import pandas
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.isotonic import IsotonicRegression
from sklearn.utils import check_random_state


train_data = []
real_data = []
area_data = []


data = pandas.read_excel('D:/Python/UWB_Data_Collect/Data_train/All_data.xlsx')

real_data.extend(data["Real95"])
train_data.extend(data["An0095"])
# area_data.extend(data["Area"])

tmp = []
for i,value in enumerate(train_data):
    if value == 0:
        tmp.append(i)
tmp.sort(reverse=True)
for i in tmp:
    train_data.pop(i)
    real_data.pop(i)
    # area_data.pop(i)

# train_data = np.hstack([np.array(train_data)[:,np.newaxis],np.array(area_data)[:,np.newaxis]])
###############################################################################
# Fit IsotonicRegression and LinearRegression models
X_train, X_test, y_train, y_test = train_test_split(train_data, real_data, test_size=0.3, random_state=None)

ir = IsotonicRegression()

# y_ = ir.fit_transform(X_train, y_train)
ir.fit(X_train, y_train)

y_ = ir.predict(X_test)
print(y_)
# lr = LinearRegression()
# lr.fit(X_train, y_train)  # x needs to be 2d for LinearRegression

###############################################################################
# plot result
#
# segments = [[[i, y[i]], [i, y_[i]]] for i in range(n)]
# lc = LineCollection(segments, zorder=0)
# lc.set_array(np.ones(len(y)))
# lc.set_linewidths(0.5 * np.ones(n))


test = ir.predict([768])
print(test)
print(746)

test = ir.predict([472])
print(test)
print(442)

test = ir.predict([1000])
print(test)
# print(44)

fig = plt.figure()
# plt.plot(train_data, real_data, 'r.', markersize=5)
plt.plot(X_test, y_, 'r.', markersize=10)
# plt.plot(X_test, y_, 'g.-', markersize=10)
plt.plot(X_test, y_test, 'g.', markersize=5)
# plt.plot(X_train, lr.predict(X_test[:, np.newaxis]), 'b-')
# plt.gca().add_collection(lc)
plt.legend(('Data', 'Data_predict'), loc='lower right')
plt.title('Isotonic regression')
plt.show()



# 100 ~ 1000 才能預測
# 遠距離資料不夠
# 模型行外資料都不太行