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
import xgboost as xgb


def trainModel():
    modelFilePath = '../modelFile/'
    # modelFileName = 'GBDT200Dec40.pkl'
    modelFileName = 'LRTest.model'

    fileName1 = '../data_new/UI28.csv'
    Xtrain, Ytrain = ReadTrainData(fileName1)
    # # UI = ReadUI(fileName)
    US = UnderSampler(ratio=40., random_state=1)
    Xtrain1, Ytrain1 = US.fit_transform(Xtrain, Ytrain)
    del Xtrain, Ytrain

    fileName = '../data_new/UI29.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    # UI = ReadUI(fileName)
    US = UnderSampler(ratio=40., random_state=2)
    Xtrain2, Ytrain2 = US.fit_transform(Xtrain, Ytrain)
    del Xtrain, Ytrain

    fileName = '../data_new/UI30.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    # UI = ReadUI(fileName)
    US = UnderSampler(ratio=40., random_state=3)
    Xtrain3, Ytrain3 = US.fit_transform(Xtrain, Ytrain)
    del Xtrain, Ytrain

    Xtrain = np.vstack((Xtrain1, Xtrain2, Xtrain3))
    Ytrain = np.hstack((Ytrain1, Ytrain2, Ytrain3))
    del Xtrain1, Xtrain2, Ytrain1, Ytrain2, Xtrain3, Ytrain3

    # model = GradientBoostingClassifier(n_estimators=200)
    # model = AdaBoostClassifier()
    model = LogisticRegression(C=1)

    model.fit(Xtrain, Ytrain)
    cPickle.dump(model, open(modelFilePath + modelFileName, 'w'))


def trainModelXgboost():
    modelFilePath = '../modelFile/'
    modelFileName = 'xgboost3.model'

    fileName1 = '../data_new/UI28.csv'
    Xtrain, Ytrain = ReadTrainData(fileName1)
    # # UI = ReadUI(fileName)
    US = UnderSampler(ratio=40., random_state=1)
    Xtrain1, Ytrain1 = US.fit_transform(Xtrain, Ytrain)
    del Xtrain, Ytrain

    fileName = '../data_new/UI29.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    # UI = ReadUI(fileName)
    US = UnderSampler(ratio=40., random_state=1)
    Xtrain2, Ytrain2 = US.fit_transform(Xtrain, Ytrain)
    del Xtrain, Ytrain

    fileName = '../data_new/UI30.csv'
    Xtrain, Ytrain = ReadTrainData(fileName)
    # UI = ReadUI(fileName)
    US = UnderSampler(ratio=40., random_state=1)
    Xtrain3, Ytrain3 = US.fit_transform(Xtrain, Ytrain)
    del Xtrain, Ytrain

    Xtrain = np.vstack((Xtrain1, Xtrain2, Xtrain3))
    Ytrain = np.hstack((Ytrain1, Ytrain2, Ytrain3))
    del Xtrain1, Xtrain2, Ytrain1, Ytrain2, Xtrain3, Ytrain3

    dtrain = xgb.DMatrix(Xtrain, label=Ytrain)
    param = {'bst:max_depth': 2, 'bst:eta': 0.3, 'silent': 1,
             'objective': 'binary:logistic'}
    # param['nthread'] = 4
    param['subsample'] = 0.9
    plst = param.items()
    plst += [('eval_metric', 'auc')]  # Multiple evals can be handled in this way
    plst += [('eval_metric', 'ams@0')]
    num_round = 10
    bst = xgb.train(plst, dtrain, num_round)
    bst.save_model(modelFilePath + modelFileName)
    # bst.dump_model(modelFilePath + modelFileName)


if __name__ == '__main__':

    trainModelXgboost()
    trainModel()
