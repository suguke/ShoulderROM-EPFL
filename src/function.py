from math import sqrt
import numpy as np
import csv
import pandas as pd

# class vector():
#     def __init__(self):
#         self.acc = np.zeros((3,1),dtype ='i')
#         self.gyr = np.zeros((3,1),dtype ='i')
    
#     def computeNorm(self):
#         norm = np.sqrt(np.sum(np.power(self.acc,2)))
#         return norm

# def computeScalar(v1, v2):
#     scalar = np.sum(np.multiply(v1.acc,v2.acc))
#     return scalar

# def computeAngle(v1, v2):
#     norm1 = v1.computeNorm()
#     norm2 = v2.computeNorm()
#     angle = np.arccos(computeScalar(v1,v2)/(norm1*norm2))
#     return angle

def computeAngle(v1, v2):
    angle = np.arccos((180/np.pi)*np.arccos(sum(v1*v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))))
    return angle

def getStartVector():
    data = pd.read_csv('data.csv',header = 4, skiprows = [6], usecols = [4,5,6])
    startVector = data.iloc[0:128].median()
    return startVector

def getEndVector():
    data = pd.read_csv('data.csv',header = 4, skiprows = [6], usecols = [4,5,6])
    endVector = data.iloc[-256:].median()
    return endVector

# x = vector()
# y = vector()
# x.acc = [1,55,0]
# y.acc = [32,0,1]
# print((180/np.pi)*computeAngle(x,y))