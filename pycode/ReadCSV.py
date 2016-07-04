# !usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
#####################################################################
#   函数功能：读取 CSV 文件
#
#   输入参数：fileName
#
#   输出参数：数据矩阵
#
#   编写时间：2016年6月
#
##################################################################


def ReadCSV(fileName, cols, Dtype):
    reader = pd.read_csv(fileName, header=None, usecols=cols, iterator=True, dtype=Dtype)
    loop = True
    chunkSize = 3000000
    chunks = []
    while loop:
        try:
            chunk = reader.get_chunk(chunkSize)
            chunks.append(chunk)
        except StopIteration:
            loop = False
            print "Iteration is stopped."
    df = pd.concat(chunks, ignore_index=True)
    values = df.values
    return values


def ReadTrainData(fileName):
    NumCol = len(pd.read_csv(fileName, nrows=1).columns)
    cols = range(3, NumCol)
    Dtype = None
    data = ReadCSV(fileName, cols, Dtype)
    Xtrain = data[:, 1:]
    Ytrain = data[:, 0]
    return Xtrain, Ytrain


def ReadTestData(fileName):
    NumCol = len(pd.read_csv(fileName, nrows=1).columns)
    cols = range(3, NumCol)
    Dtype = None
    Xtest = ReadCSV(fileName, cols, Dtype)
    return Xtest


def ReadUI(fileName):
    cols = [0, 1]
    type = object
    UI = ReadCSV(fileName, cols, type)
    return UI
