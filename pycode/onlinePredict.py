# !usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cPickle
from ReadCSV import *
import csv


if __name__ == '__main__':

    modelFilePath = '../modelFile/'
    modelFileName = 'GBDT300Dec70.pkl'
    model = cPickle.load(open(modelFilePath + modelFileName, 'r'))

    fileName = '../data/UI31d1.csv'
    Xtest = ReadTestData(fileName)
    UI = ReadUI(fileName)

    pYtest = model.predict_proba(Xtest)[:, 1]
    pYtest = np.array(pYtest)
    UI = UI[pYtest > 0.2]

    fielItems = '../data/tianchi_fresh_comp_train_item.csv'
    Items = ReadCSV(fielItems, [0], object)

    UISubmit = []
    for ui in UI:
        if ui[1] in Items:
            UISubmit.append(ui)

    fileSubmit = '../data/model.csv'
    f = open(fileSubmit, 'w')
    writer = csv.writer(f)
    writer.writerow(['user_id', 'item_id'])
    for ui in UISubmit:
        writer.writerow(ui)
    f.close()

    # modelFilePath = '../modelFile/'
    # modelFileName = 'GBDT100Dec70.pkl'
    # model = cPickle.load(open(modelFilePath + modelFileName, 'r'))

    # fileName = '../data/UI31Inter.csv'
    # Xtest = ReadTestData(fileName)
    # UI = ReadUI(fileName)

    # pYtest = model.predict_proba(Xtest)[:, 1]
    # UIProb = zip(UI, pYtest)

    # UIProb.sort(key=lambda x: x[1], reverse=True)
    # submitNum = 517
    # UIProb = UIProb[0:submitNum]

    # fileSubmit = '../data/model.csv'
    # f = open(fileSubmit, 'w')
    # writer = csv.writer(f)
    # writer.writerow(['user_id', 'item_id'])
    # for uip in UIProb:
    #     writer.writerow([uip[0][0], uip[0][1]])
    # f.close()
