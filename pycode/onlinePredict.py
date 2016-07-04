# !usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cPickle
from ReadCSV import *
import csv
import xgboost as xgb


def onlinePredict():
    modelFilePath = '../modelFile/'
    modelFileName = 'GBDT200Dec40.pkl'
    model = cPickle.load(open(modelFilePath + modelFileName, 'r'))

    fileName = '../data_new/UI31.csv'
    Xtest = ReadTestData(fileName)
    UI = ReadUI(fileName)

    pYtest = model.predict_proba(Xtest)[:, 1]
    pYtest = np.array(pYtest)
    UI = UI[pYtest > 0.5]
    pYtest = pYtest[pYtest > 0.5]

    fielItems = '../data/tianchi_fresh_comp_train_item.csv'
    Items = ReadCSV(fielItems, [0], object)
    ItemsDic = {}
    for i in range(1, len(Items)):
        item = Items[i][0]
        ItemsDic[item] = True
    del Items

    UISubmit = []
    for i in range(len(pYtest)):
        if UI[i][1] in ItemsDic:
            temp = (UI[i][0], UI[i][1], pYtest[i])
            UISubmit.append(temp)
    UISubmit.sort(key=lambda x: x[2], reverse=True)
    submitNum = 517
    UISubmit = UISubmit[0:submitNum]

    fileSubmit = '../data/submitFile/model.csv'
    f = open(fileSubmit, 'w')
    writer = csv.writer(f)
    writer.writerow(['user_id', 'item_id'])
    for ui in UISubmit:
        writer.writerow([ui[0], ui[1]])
    f.close()


def onlinePredictXgboost():
    modelFilePath = '../modelFile/'
    modelFileName = 'xgboost3.model'
    # bst.dump_model(modelFilePath + modelFileName)
    modelName = modelFilePath + modelFileName
    bst = xgb.Booster(model_file=modelName)
    fileName = '../data_new/UI31.csv'
    Xtest = ReadTestData(fileName)
    UI = ReadUI(fileName)
    dtest = xgb.DMatrix(Xtest)
    pYtest = bst.predict(dtest)

    pYtest = np.array(pYtest)
    UI = UI[pYtest > 0.5]
    pYtest = pYtest[pYtest > 0.5]

    fielItems = '../data/tianchi_fresh_comp_train_item.csv'
    Items = ReadCSV(fielItems, [0], object)
    ItemsDic = {}
    for i in range(1, len(Items)):
        item = Items[i][0]
        ItemsDic[item] = True
    del Items

    UISubmit = []
    for i in range(len(pYtest)):
        if UI[i][1] in ItemsDic:
            temp = (UI[i][0], UI[i][1], pYtest[i])
            UISubmit.append(temp)
    UISubmit.sort(key=lambda x: x[2], reverse=True)
    submitNum = 517
    UISubmit = UISubmit[0:submitNum]

    fileSubmit = '../data/submitFile/model.csv'
    f = open(fileSubmit, 'w')
    writer = csv.writer(f)
    writer.writerow(['user_id', 'item_id'])
    for ui in UISubmit:
        writer.writerow([ui[0], ui[1]])
    f.close()


def onlinePredictKeras():
    modelFilePath = '../modelFile/'
    modelFileName = 'kerasmoedl.HD'
    model = cPickle.load(open(modelFilePath + modelFileName, 'r'))

    fileName = '../data/UI31.csv'
    Xtest = ReadTestData(fileName)
    UI = ReadUI(fileName)

    pYtest = model.predict_proba(Xtest)[:, 1]
    pYtest = np.array(pYtest)
    UI = UI[pYtest > 0.5]
    pYtest = pYtest[pYtest > 0.5]

    fielItems = '../data/tianchi_fresh_comp_train_item.csv'
    Items = ReadCSV(fielItems, [0], object)
    ItemsDic = {}
    for i in range(1, len(Items)):
        item = Items[i][0]
        ItemsDic[item] = True
    del Items

    UISubmit = []
    for i in range(len(pYtest)):
        if UI[i][1] in ItemsDic:
            temp = (UI[i][0], UI[i][1], pYtest[i])
            UISubmit.append(temp)
    UISubmit.sort(key=lambda x: x[2], reverse=True)
    submitNum = 517
    UISubmit = UISubmit[0:submitNum]

    fileSubmit = '../data/submitFile/model.csv'
    f = open(fileSubmit, 'w')
    writer = csv.writer(f)
    writer.writerow(['user_id', 'item_id'])
    for ui in UISubmit:
        writer.writerow([ui[0], ui[1]])
    f.close()


def onlinePredictBlending():
    modelFilePath = '../modelFile/'
    modelFileName = 'LRTest.model'
    model = cPickle.load(open(modelFilePath + modelFileName, 'r'))

    fileName = '../data_new/UI31.csv'
    Xtest = ReadTestData(fileName)
    UI = ReadUI(fileName)

    pYtest1 = model.predict_proba(Xtest)[:, 1]
    pYtest1 = np.array(pYtest1)

    modelFileName = 'xgboost3.model'
    # bst.dump_model(modelFilePath + modelFileName)
    modelName = modelFilePath + modelFileName
    bst = xgb.Booster(model_file=modelName)

    dtest = xgb.DMatrix(Xtest)
    del Xtest
    pYtest2 = bst.predict(dtest)
    pYtest = 0.7 * pYtest2 + 0.3 * pYtest1
    UI = UI[pYtest > 0.5]
    pYtest = pYtest[pYtest > 0.5]

    fielItems = '../data/tianchi_fresh_comp_train_item.csv'
    Items = ReadCSV(fielItems, [0], object)
    ItemsDic = {}
    for i in range(1, len(Items)):
        item = Items[i][0]
        ItemsDic[item] = True
    del Items

    UISubmit = []
    for i in range(len(pYtest)):
        if UI[i][1] in ItemsDic:
            temp = (UI[i][0], UI[i][1], pYtest[i])
            UISubmit.append(temp)
    UISubmit.sort(key=lambda x: x[2], reverse=True)
    submitNum = 517
    UISubmit = UISubmit[0:submitNum]

    fileSubmit = '../data/submitFile/model.csv'
    f = open(fileSubmit, 'w')
    writer = csv.writer(f)
    writer.writerow(['user_id', 'item_id'])
    for ui in UISubmit:
        writer.writerow([ui[0], ui[1]])
    f.close()
if __name__ == '__main__':

    # onlinePredictXgboost()
    onlinePredictBlending()
