import numpy as np
import csv
import pandas as pd

fileLoc = '../data/A_H_90_5.csv'

def computeAngle(v1, v2):
    angle = (180/np.pi)*np.arccos(sum(v1*v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))
    return angle

def getStartVector():
    data = pd.read_csv(fileLoc, header = 4, skiprows = [6], usecols = [4,5,6])
    startVector = data.iloc[0:256].median()
    return startVector

def getEndVector():
    data = pd.read_csv(fileLoc, header = 4, skiprows = [6], usecols = [4,5,6])
    endVector = data.iloc[-256:].median()
    return endVector

#kf = KalmanFilter(transition_matrices = [[1, 1], [0, 1]], observation_matrices = [[0.1, 0.5], [-0.3, 0.0]]),measurements = np.asarray([[1,0], [0,0], [0,1]])
startVect = getStartVector()
endVect = getEndVector()
print(startVect)
print(endVect)
angle = computeAngle(startVect,endVect)
print(angle)