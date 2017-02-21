#usr/bin/env python
# coding=utf-8
import pdb
import random
import numpy as np

def LoadDiscreteDataFromTxt(txtpath):
    print ("Loading data ...")
    fp = open(txtpath,"r")
    arr = []
    for line in fp.readlines():
        arr.append(line.replace("\r\n","").split("\t"))
    fp.close()

    if len(arr) >= 15000:
        tmp = []
        subsetRecordNumberSet = random.sample(range(len(arr)),int(len(arr)*0.1))
        for i in subsetRecordNumberSet:
            tmp.append(arr[i])
        arr = tmp
    arrTrans =  map(list, zip(*arr))
    print ("Preprocessing data ...")
    transArr = []
    for column in arrTrans:
        col = []
        lis = [item for item in set(column)]
        for item in column:
            for i in range(len(lis)):
                if item == lis[i]:
                    col.append(i)
                    break
        transArr.append(col)
    totalRecordNum = len(transArr[len(transArr)-1])
    totalAttributeNum = len(transArr)-1
    print ("There are total %d records, and %d attributes" %(totalRecordNum,totalAttributeNum))
    Xt = []
    for i in range(0,len(transArr)-1):
        Xt.append(transArr[i])
    Y = transArr[len(transArr)-1]
    X = map(list, zip(*Xt))
    print ("Finished preprocessing!")
    return X,Xt,Y,totalRecordNum,totalAttributeNum

def LoadLargeContinuousDataFromTxt(txtpath):
    print ("Loading large continuous data...")
    """
    fp = open(txtpath,"r")
    arr = []
    for line in fp.readlines():
        numRow = [float(str) for str in line.replace("\n","").split(" ")]
        arr.append(numRow)    
    fp.close()
    """

    npArr = np.loadtxt(txtpath)

    print len(npArr)

    subsetRecordNumberSet = random.sample(range(len(npArr)),int(len(npArr)*0.01))
    tmp = []
    for i in subsetRecordNumberSet:
        tmp.append(npArr[i])

    npArr = np.array(tmp)
    
    transNpArr = npArr.transpose()
    tmp = transNpArr[:len(transNpArr)-1]
    Xt = []
    for row in tmp:
        Xt.append(discreteContinuousData(row))
    Xt = np.array(Xt)

    X = Xt.transpose()
    Y = transNpArr[len(transNpArr)-1]
    Y = Y.transpose()
    
    X = list(X)
    Xt = list(Xt)
    Y = list(Y)

    totalRecordNum = len(X)
    totalAttributeNum = len(Xt)


    print ("There are total %d records, and %d attributes" %(totalRecordNum,totalAttributeNum))

    print ("Finished preprocessing!")

    return X,Xt,Y,totalRecordNum,totalAttributeNum

def LoadContinuousDataFromTxt(txtpath):
    print ("Loading continuous data ...")
    fp = open(txtpath,"r")
    arr = []
    for line in fp.readlines():
        arr.append(line.replace("\n","").split(" "))
    fp.close()

    print (len(arr[0]))

    
    if len(arr) >= 15000:
        tmp = []
        subsetRecordNumberSet = random.sample(range(len(arr)),int(len(arr)*0.1))
        for i in subsetRecordNumberSet:
            tmp.append(arr[i])
        arr = tmp
    
    pdb.set_trace()
    arrTrans =  map(list, zip(*arr))

    print (len(arrTrans))

    print ("Preprocessing data ...")
    transArr = []
    for column in arrTrans:
        col = []
        lis = [item for item in set(column)]
        for item in column:
            for i in range(len(lis)):
                if item == lis[i]:
                    col.append(i)
                    break
        transArr.append(col)
    totalRecordNum = len(transArr[len(transArr)-1])
    totalAttributeNum = len(transArr)-1
    print ("There are total %d records, and %d attributes" %(totalRecordNum,totalAttributeNum))
    Xt = []
    for i in range(0,len(transArr)-1):
        Xt.append(discreteContinuousData(transArr[i]))
    Y = transArr[len(transArr)-1]
    X = map(list, zip(*Xt))
    print ("Finished preprocessing!")
    return X,Xt,Y,totalRecordNum,totalAttributeNum

def discreteContinuousData(row):
    ret = []
    discreteDegree = 20
    minValue = min(row)
    maxValue = max(row)
    for item in row:
        if (maxValue==minValue):
            degree = 0
        else:
            degree = int((item-minValue)*discreteDegree*1.0/(maxValue-minValue)*1.0)
        ret.append(degree)

    return ret

