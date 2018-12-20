# Run this file to test the angle computation
# Change the pathfile to selecte the desired data

import numpy as np
import csv
import pandas as pd

fileLoc = '../data/RE2a_H_90_7.csv'

def computeAngle(v1, v2):
    '''Computation of the angle between 2 vectors'''
    angle = (180/np.pi)*np.arccos(sum(v1*v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))
    return angle

def getStartVector():
    '''Extract a start vector over 2s of sample at 128 Hz'''
    data = pd.read_csv(fileLoc, header = 4, skiprows = [6], usecols = [4,5,6])
    startVector = data.iloc[0:256].median()
    return startVector

def getEndVector():
    '''Extract an end vector over 2s of sample at 128 Hz'''
    data = pd.read_csv(fileLoc, header = 4, skiprows = [6], usecols = [4,5,6])
    endVector = data.iloc[-256:].median()
    return endVector

startVect = getStartVector()
endVect = getEndVector()
print(startVect)
print(endVect)
angle = computeAngle(startVect,endVect)
print(angle)