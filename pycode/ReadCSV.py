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
    cols = None
    Dtype = None
    data = ReadCSV(fileName, cols, Dtype)
    Xtrain = data[:, 4:]
    Ytrain = data[:, 3]
    return Xtrain, Ytrain


def ReadTestData(fileName):
    cols = None
    Dtype = None
    data = ReadCSV(fileName, cols, Dtype)
    Xtest = data[:, 3:]
    return Xtest


def ReadUI(fileName):
    cols = [0, 1]
    type = object
    UI = ReadCSV(fileName, cols, type)
    return UI
