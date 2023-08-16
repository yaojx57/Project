import whisper
import argparse
import math
import numpy as np


from jiwer import wer


def check_wer(reference, hypothesis):
    error = wer(reference, hypothesis)
    return error


def cal_RMSE(actual_scores: list, pre_scores: list):
    MSE = np.square(np.subtract(actual_scores,pre_scores)).mean() 

    RMSE = math.sqrt(MSE)
    print('Root Mean Square Error is '+str(RMSE))
    return RMSE