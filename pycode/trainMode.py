import MySQLdb
# import cPickle
import numpy as np
import time
import pandas as pd
import cPickle
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from unbalanced_dataset import UnderSampler
from sklearn.metrics import confusion_matrix
from ReadCSV import *


if __name__ == '__main__':

    modelFilePath = '../modelFile/'
    modelFileName = 'GBDT100Dec70.pkl'

    fileName = '../data/UI29.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    UI = ReadUI(fileName)
    US = UnderSampler(ratio=40.)
    Xtrain1, Ytrain1 = US.fit_transform(Xtrain, Ytrain)

    fileName = '../data/UI30.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    UI = ReadUI(fileName)
    US = UnderSampler(ratio=40.)
    Xtrain2, Ytrain2 = US.fit_transform(Xtrain, Ytrain)

    Xtrain = np.vstack((Xtrain1, Xtrain2))
    Ytrain = np.hstack((Ytrain1, Ytrain2))
    del Xtrain1, Xtrain2, Ytrain1, Ytrain2

    model = GradientBoostingClassifier(n_estimators=300)
    # model = AdaBoostClassifier()

    start = time.time()
    model.fit(Xtrain, Ytrain)
    end = time.time()
    # cPickle.dump(model, open(modelFilePath + modelFileName, 'w'))
