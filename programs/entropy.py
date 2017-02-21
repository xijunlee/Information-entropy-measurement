#!/usr/bin/env python
# coding=utf-8
from math import *
import pdb
def log2(x):
    return log(x)*1.0 / log(2)

"""
    calculate the entropy of the idx th attribute
    X: the dataset
    idx: the index
    type: discrete or continuous
"""
def calcIndividualEntropy(X,idx,type):

    X = map(list, zip(*X))#transform the dataset X
    ent = 0.0

    if type == 'discrete':
        attr = X[idx]
        elementSet = set(attr)
        totalRecordNum = len(attr)
        for item in elementSet:
            p = attr.count(item)*1.0 / totalRecordNum
            ent = ent - p * log2(p)
    
    return ent


"""
    calculate the joint entropy of a set of attributes
    indexSet: the set of index
    type: discrete or continuous
"""
def calcJointEntropy(X,indexSet,type):

    X = map(list, zip(*X))#transform the dataset X
    ent = 0.0
    
    if type == 'discrete':
        jointSet = []
        for i in range(len(X[0])):
            tmp = ''
            for idx in indexSet:
                tmp = tmp + str(X[idx][i])
            jointSet.append(tmp)
    

        elementSet = set(jointSet)
        totalRecordNum = len(X[0])
        for item in elementSet:
             p = jointSet.count(item)*1.0 / totalRecordNum
             ent = ent - p * log2(p)
    return ent

