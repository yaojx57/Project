from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from speech_info import result_json
from read_json import get_train_data
import numpy as np


def fitting(type: str='l', level: str='l'):
    x = []
    y = []
    x, y = get_train_data(type, level)
    x = np.array(x)
    y = np.array(y)
    x_train, x_test, y_train, y_test = train_test_split(x, y,test_size = 0.25)
    logreg = LinearRegression()
    logreg.fit(x_train.reshape(-1,1),y_train.reshape(-1,1))
    print(logreg.score(x_test.reshape(-1,1),y_test.reshape(-1,1)))
    return logreg