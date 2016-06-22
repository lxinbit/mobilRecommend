import MySQLdb
# import cPickle
import numpy as np
import time
import pandas as pd
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from unbalanced_dataset import UnderSampler,ClusterCentroids
from ReadCSV import *

if __name__ == '__main__':

    fileName = '../data/UI29.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)

    model = GradientBoostingClassifier(n_estimators=100)
    # model = AdaBoostClassifier()
    # model = LogisticRegression()

    start = time.time()

    US = UnderSampler(ratio=40.)
    # # US = ClusterCentroids(ratio=30.)
    Xtrain, Ytrain = US.fit_transform(Xtrain, Ytrain)
    end = time.time()
    print "Data decimation time: ", end - start

    start = time.time()
    model.fit(Xtrain, Ytrain)
    end = time.time()

    fileName = '../data/UI29Inter.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)

    pYtrain = model.predict_proba(Xtrain)[:, 1]
    Yzip = zip(Ytrain, pYtrain)
    Yzip.sort(key=lambda x: x[1], reverse=True)
    submitNum = 698
    Yzip = Yzip[0:submitNum]

    TPNum = sum(map(lambda x: x[0], Yzip))
    Precise = 1.0 * TPNum / submitNum
    Recall = 1.0 * TPNum / submitNum
    F1 = 2.0 * Precise * Recall / (Precise + Recall)
    print 'Train Set: F1/P/R %f/%f/%f\n' % (F1, Precise, Recall)

    fileName = '../data/UI30Inter.csv'
    Xval, Yval = ReadTrainData(fileName)

    pYval = model.predict_proba(Xval)[:, 1]
    Yzip = zip(Yval, pYval)
    Yzip.sort(key=lambda x: x[1], reverse=True)
    submitNum = 767
    Yzip = Yzip[0:submitNum]

    TPNum = sum(map(lambda x: x[0], Yzip))
    Precise = 1.0 * TPNum / submitNum
    Recall = 1.0 * TPNum / submitNum
    F1 = 2.0 * Precise * Recall / (Precise + Recall)
    print 'Validation Set: F1/P/R %f/%f/%f\n' % (F1, Precise, Recall)
