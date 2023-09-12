from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from speech_info import result_json
from read_json import get_train_data
import numpy as np
from scipy.optimize import curve_fit

def sigmoid(k,x,x0):
    return (1 / (1 + np.exp(-k*(x-x0))))



def fitting(data ,type: str='l', level: str='l'):
    x = []
    y = []
    x, y = get_train_data(type, level)
    x = np.array(x)
    y = np.array(y)
    popt, pcov = curve_fit(sigmoid, x, y, method='dogbox')
    print(len(data))
    pred_data = sigmoid(data, *popt)
    print(len(pred_data))
    if len(data)!=len(pred_data):
        print('False')
    return pred_data*100