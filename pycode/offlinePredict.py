# !usr/bin/env python
# -*- coding: utf-8 -*-


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
from unbalanced_dataset import UnderSampler,ClusterCentroids
from ReadCSV import *

if __name__ == '__main__':

    # fileName = '../data/UI29.csv'
    # Xtrain, Ytrain = ReadTrainData(fileName)

    # model = GradientBoostingClassifier(n_estimators=200)
    # # model = AdaBoostClassifier()
    # # model = LogisticRegression()

    # start = time.time()

    # US = UnderSampler(ratio=40.)
    # # # US = ClusterCentroids(ratio=30.)
    # Xtrain, Ytrain = US.fit_transform(Xtrain, Ytrain)
    # end = time.time()
    # print "Data decimation time: ", end - start

    # start = time.time()
    # model.fit(Xtrain, Ytrain)
    # end = time.time()

    modelFilePath = '../modelFile/'
    modelFileName = 'GBDT100Dec40Train.pkl'
    # modelFileName = 'LRDec40Train.pkl'
    # cPickle.dump(model, open(modelFilePath + modelFileName, 'w'))

    model = cPickle.load(open(modelFilePath + modelFileName, 'r'))
    # 读取商品子集
    fielItems = '../data/tianchi_fresh_comp_train_item.csv'
    Items = ReadCSV(fielItems, [0], object)
    ItemsDic = {}
    for i in range(1, len(Items)):
        item = Items[i][0]
        ItemsDic[item] = True
    del Items
    # 计算训练集F1值
    fileName = '../data/UI29.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    UI = ReadUI(fileName)
    pYtrain = model.predict_proba(Xtrain)[:, 1]
    del Xtrain
    pYtrain = np.array(pYtrain)
    UI = UI[pYtrain > 0.5]
    Ytrain = Ytrain[pYtrain > 0.5]
    pYtrain = pYtrain[pYtrain > 0.5]

    Yzip = []
    for i in range(len(Ytrain)):
        if UI[i][1] in ItemsDic:
            temp = (Ytrain[i], pYtrain[i])
            Yzip.append(temp)
    Yzip.sort(key=lambda x: x[1], reverse=True)
    submitNum = 698
    Yzip = Yzip[0:submitNum]

    TPNum = sum(map(lambda x: x[0], Yzip))
    Precise = 1.0 * TPNum / submitNum
    Recall = 1.0 * TPNum / submitNum
    F1 = 2.0 * Precise * Recall / (Precise + Recall)
    print 'Train Set: F1/P/R %f/%f/%f\n' % (F1, Precise, Recall)

    # 计算验证集的F1
    fileName = '../data/UI30.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    UI = ReadUI(fileName)
    pYtrain = model.predict_proba(Xtrain)[:, 1]
    del Xtrain
    pYtrain = np.array(pYtrain)
    UI = UI[pYtrain > 0.5]
    Ytrain = Ytrain[pYtrain > 0.5]
    pYtrain = pYtrain[pYtrain > 0.5]

    Yzip = []
    for i in range(len(Ytrain)):
        if UI[i][1] in ItemsDic:
            temp = (Ytrain[i], pYtrain[i])
            Yzip.append(temp)
    Yzip.sort(key=lambda x: x[1], reverse=True)
    submitNum = 767
    Yzip = Yzip[0:submitNum]

    TPNum = sum(map(lambda x: x[0], Yzip))
    Precise = 1.0 * TPNum / submitNum
    Recall = 1.0 * TPNum / submitNum
    F1 = 2.0 * Precise * Recall / (Precise + Recall)
    print 'Validation Set: F1/P/R %f/%f/%f\n' % (F1, Precise, Recall)
