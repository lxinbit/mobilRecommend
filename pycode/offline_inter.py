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
from unbalanced_dataset import UnderSampler, ClusterCentroids
from ReadCSV import *
import xgboost as xgb


def offlineTrain(modelFilePath, modelFileName, randomstate):

    # modelFileName = 'LRDec40Train.pkl'
    start = time.time()
    fileName = '../data_new/UI28.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    # UI = ReadUI(fileName)
    US = UnderSampler(ratio=40., random_state=randomstate)
    Xtrain1, Ytrain1 = US.fit_transform(Xtrain, Ytrain)

    fileName = '../data_new/UI29.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    # UI = ReadUI(fileName)
    US = UnderSampler(ratio=40., random_state=randomstate + 1)
    Xtrain2, Ytrain2 = US.fit_transform(Xtrain, Ytrain)

    Xtrain = np.vstack((Xtrain1, Xtrain2))
    Ytrain = np.hstack((Ytrain1, Ytrain2))
    del Xtrain1, Xtrain2, Ytrain1, Ytrain2
    end = time.time()
    print "read and decimation data: ", end - start

    start = time.time()
    # model = GradientBoostingClassifier(n_estimators=100)
    # model = AdaBoostClassifier()
    model = LogisticRegression(C=1)
    model.fit(Xtrain, Ytrain)
    end = time.time()
    print "model fit time:", end - start
    cPickle.dump(model, open(modelFilePath + modelFileName, 'w'))


def validition(modelFilePath, modelFileName):
    model = cPickle.load(open(modelFilePath + modelFileName, 'r'))
    # 计算训练集F1值
    fileName = '../data_new/UI29Inter.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    # UI = ReadUI(fileName)
    pYtrain = model.predict_proba(Xtrain)[:, 1]
    del Xtrain
    Yzip = zip(Ytrain, pYtrain)

    Yzip.sort(key=lambda x: x[1], reverse=True)
    submitNum = 698
    Yzip = Yzip[0:submitNum]

    TPNum = sum(map(lambda x: x[0], Yzip))
    Precise = 1.0 * TPNum / submitNum
    Recall = 1.0 * TPNum / submitNum
    F1 = 2.0 * Precise * Recall / (Precise + Recall)
    print 'Train Set: F1/P/R %f/%f/%f\n' % (F1, Precise, Recall)

    # 计算验证集的F1
    fileName = '../data_new/UI30Inter.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    # UI = ReadUI(fileName)
    pYtrain = model.predict_proba(Xtrain)[:, 1]
    del Xtrain
    Yzip = zip(Ytrain, pYtrain)

    Yzip.sort(key=lambda x: x[1], reverse=True)
    submitNum = 767
    Yzip = Yzip[0:submitNum]

    TPNum = sum(map(lambda x: x[0], Yzip))
    Precise = 1.0 * TPNum / submitNum
    Recall = 1.0 * TPNum / submitNum
    F1 = 2.0 * Precise * Recall / (Precise + Recall)
    print 'Validation Set: F1/P/R %f/%f/%f\n' % (F1, Precise, Recall)


def offlineTrainXgboost(modelFilePath, modelFileName, randomstate):
    start = time.time()
    fileName1 = '../data_new/UI28.csv'
    Xtrain, Ytrain = ReadTrainData(fileName1)
    # # UI = ReadUI(fileName)
    US = UnderSampler(ratio=40., random_state=randomstate)
    Xtrain1, Ytrain1 = US.fit_transform(Xtrain, Ytrain)
    del Xtrain, Ytrain

    fileName2 = '../data_new/UI29.csv'
    Xtrain, Ytrain = ReadTrainData(fileName2)
    # UI = ReadUI(fileName)
    US = UnderSampler(ratio=40., random_state=randomstate)
    Xtrain2, Ytrain2 = US.fit_transform(Xtrain, Ytrain)
    del Xtrain, Ytrain

    Xtrain = np.vstack((Xtrain1, Xtrain2))
    Ytrain = np.hstack((Ytrain1, Ytrain2))
    del Xtrain1, Xtrain2, Ytrain1, Ytrain2
    # sum_pos = sum(Ytrain)
    # sum_neg = len(Ytrain) - sum_pos
    end = time.time()
    print "read and decimation data: ", end - start

    # fileName = '../data/UI30Inter.csv'
    # Xval, Yval = ReadTrainData(fileName)

    dtrain = xgb.DMatrix(Xtrain, label=Ytrain)
    # dval = xgb.DMatrix(Xval, label=Yval)
    # evallist = [(dval, 'eval'), (dtrain, 'train')]
    param = {'bst:max_depth': 3, 'bst:eta': 0.3, 'silent': 1,
             'objective': 'binary:logistic'}
    # param['nthread'] = 4
    param['subsample'] = 0.9
    # param['scale_pos_weight'] = sum_neg / sum_pos
    plst = param.items()
    plst += [('eval_metric', 'auc')]  # Multiple evals can be handled in this way
    plst += [('eval_metric', 'ams@0')]
    num_round = 10
    bst = xgb.train(plst, dtrain, num_round)
    xgb.plot_importance(bst)
    bst.save_model(modelFilePath + modelFileName)


def validitionXgboost(modelFilePath, modelFileName):

    modelName = modelFilePath + modelFileName
    bst = xgb.Booster(model_file=modelName)
    # 计算训练集F1值
    # fileName = '../data/UI29Inter.csv'
    fileName = '../data_new/UI29Inter.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    # UI = ReadUI(fileName)
    dtrain = xgb.DMatrix(Xtrain, label=Ytrain)
    pYtrain = bst.predict(dtrain)
    del Xtrain
    Yzip = zip(Ytrain, pYtrain)

    Yzip.sort(key=lambda x: x[1], reverse=True)
    submitNum = 698
    Yzip = Yzip[0:submitNum]

    TPNum = sum(map(lambda x: x[0], Yzip))
    Precise = 100.0 * TPNum / submitNum
    Recall = 100.0 * TPNum / submitNum
    F1 = 2.0 * Precise * Recall / (Precise + Recall)
    print 'Train Set: F1/P/R %f%%/%f%%/%f%%\n' % (F1, Precise, Recall)

    # 计算验证集的F1
    fileName = '../data_new/UI30Inter.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    # UI = ReadUI(fileName)
    dtrain = xgb.DMatrix(Xtrain, label=Ytrain)
    pYtrain = bst.predict(dtrain)
    del Xtrain
    Yzip = zip(Ytrain, pYtrain)

    Yzip.sort(key=lambda x: x[1], reverse=True)
    submitNum = 767
    Yzip = Yzip[0:submitNum]

    TPNum = sum(map(lambda x: x[0], Yzip))
    Precise = 100.0 * TPNum / submitNum
    Recall = 100.0 * TPNum / submitNum
    F1 = 2.0 * Precise * Recall / (Precise + Recall)
    print 'Train Set: F1/P/R %f%%/%f%%/%f%%\n' % (F1, Precise, Recall)


def validitionBlending(modelFilePath, modelFileName1, modelFileName2):
    model = cPickle.load(open(modelFilePath + modelFileName1, 'r'))
    # 计算训练集F1值
    fileName = '../data_new/UI29Inter.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    # UI = ReadUI(fileName)
    pYtrain1 = model.predict_proba(Xtrain)[:, 1]

    modelName = modelFilePath + modelFileName2
    bst = xgb.Booster(model_file=modelName)
    dtrain = xgb.DMatrix(Xtrain, label=Ytrain)
    pYtrain2 = bst.predict(dtrain)
    del Xtrain
    pYtrain = 0.7 * pYtrain2 + 0.3 * pYtrain1
    Yzip = zip(Ytrain, pYtrain)

    Yzip.sort(key=lambda x: x[1], reverse=True)
    submitNum = 698
    Yzip = Yzip[0:submitNum]

    TPNum = sum(map(lambda x: x[0], Yzip))
    Precise = 1.0 * TPNum / submitNum
    Recall = 1.0 * TPNum / submitNum
    F1 = 2.0 * Precise * Recall / (Precise + Recall)
    print 'Train Set: F1/P/R %f/%f/%f\n' % (F1, Precise, Recall)

    # 计算验证集的F1
    fileName = '../data_new/UI30Inter.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    # UI = ReadUI(fileName)
    pYtrain1 = model.predict_proba(Xtrain)[:, 1]
    dtrain = xgb.DMatrix(Xtrain, label=Ytrain)
    pYtrain2 = bst.predict(dtrain)
    del Xtrain
    pYtrain = 0.7 * pYtrain2 + 0.3 * pYtrain1
    Yzip = zip(Ytrain, pYtrain)

    Yzip.sort(key=lambda x: x[1], reverse=True)
    submitNum = 767
    Yzip = Yzip[0:submitNum]

    TPNum = sum(map(lambda x: x[0], Yzip))
    Precise = 100.0 * TPNum / submitNum
    Recall = 100.0 * TPNum / submitNum
    F1 = 2.0 * Precise * Recall / (Precise + Recall)
    print 'Validation Set: F1/P/R %f/%f/%f\n' % (F1, Precise, Recall)

if __name__ == '__main__':

    modelFilePath = '../modelFile/'
    modelFileName = 'xgboostTrain.model'
    # modelFileName = 'LRTrain.model'

    # offlineTrain(modelFilePath, modelFileName, 1)
    # validition(modelFilePath, modelFileName)
    offlineTrainXgboost(modelFilePath, modelFileName, 1)
    validitionXgboost(modelFilePath, modelFileName)

    # validitionBlending(modelFilePath, 'LRTrain.model', 'xgboostTrain.model')
