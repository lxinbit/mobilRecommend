# !usr/bin/env python
# -*- coding: utf-8 -*-


from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from ReadCSV import *
import time
from unbalanced_dataset import UnderSampler
import numpy as np
import csv


modelFilePath = '../modelFile/'
modelFileName = 'kerasmoedl.HD'

fileName1 = '../data/UI28.csv'
Xtrain, Ytrain = ReadTrainData(fileName1)
# # UI = ReadUI(fileName)
US = UnderSampler(ratio=40., random_state=1)
Xtrain1, Ytrain1 = US.fit_transform(Xtrain, Ytrain)
del Xtrain, Ytrain

fileName = '../data/UI29.csv'
Xtrain, Ytrain = ReadTrainData(fileName)
# UI = ReadUI(fileName)
US = UnderSampler(ratio=40., random_state=1)
Xtrain2, Ytrain2 = US.fit_transform(Xtrain, Ytrain)
del Xtrain, Ytrain

fileName = '../data/UI30.csv'
Xtrain, Ytrain = ReadTrainData(fileName)
# UI = ReadUI(fileName)
US = UnderSampler(ratio=40., random_state=1)
Xtrain3, Ytrain3 = US.fit_transform(Xtrain, Ytrain)
del Xtrain, Ytrain

Xtrain = np.vstack((Xtrain1, Xtrain2, Xtrain3))
Ytrain = np.hstack((Ytrain1, Ytrain2, Ytrain3))
del Xtrain1, Xtrain2, Ytrain1, Ytrain2, Xtrain3, Ytrain3


model = Sequential()
model.add(Dense(64, input_dim=35, init='uniform'))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(32, init='uniform'))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1, init='uniform'))
model.add(Activation('sigmoid'))

sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='binary_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

model.fit(Xtrain, Ytrain,
          nb_epoch=20,
          batch_size=16)

# model.save_weights(modelFilePath + modelFileName)
fileName = '../data/UI31.csv'
Xtest = ReadTestData(fileName)
UI = ReadUI(fileName)

pYtest = model.predict_proba(Xtest)
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
