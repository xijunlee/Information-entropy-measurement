#!/usr/bin/env python
# coding=utf-8
from itertools import combinations
from entropy import *

class informationGainCalc:

    def __init__(self,XX,n,thre):
        self.X = XX
        self.n = n
        self.threshold = thre
        self.maxEntropy = -21400000
        self.maxEntropyAttrSet = set([])

    def informationGainMax(self,extendedSet,candidatedSet):
        if len(extendedSet) >= self.n or len(candidatedSet) == 0:
            tmp = calcJointEntropy(self.X,extendedSet,'discrete')
            if tmp >= self.maxEntropy:
                self.maxEntropy = tmp 
                self.maxEntropyAttrSet = extendedSet
            return
        Ho = calcJointEntropy(self.X,extendedSet,'discrete')
        maxInfoGain = -21400000
        maxInfoGainAttr = 0
        for attr in candidatedSet:
            Hc = calcJointEntropy(self.X,(extendedSet|set([attr])),'discrete')
            increment = (Hc-Ho)/Ho
            if increment < self.threshold:
                candidatedSet.remove(attr)
            if Hc >= maxInfoGain:
                maxInfoGain = Hc
                maxInfoGainAttr = attr
        extendedSet.add(maxInfoGainAttr)
        if maxInfoGainAttr in candidatedSet:
            candidatedSet.remove(maxInfoGainAttr)

        self.informationGainMax(extendedSet,candidatedSet)

    def searchOptimal(self,attrTotalNum,selectedNum):
    
        candidatedSet = combinations(range(attrTotalNum),selectedNum)

        maxEnt = -21400000
        optimalAttrSet = []
        for itemSet in candidatedSet:
            jointEntropy = calcJointEntropy(self.X,itemSet,'discrete')
            if jointEntropy >= maxEnt:
                maxEnt = jointEntropy
                optimalAttrSet = itemSet

        print ("The optimal attribute set obtained by searching is:")
        print set(optimalAttrSet),maxEnt
    
    def searchAll(self,attrTotalNum,selectedNum):

        candidatedSet = combinations(range(attrTotalNum),selectedNum)

        entropyPairList = []
        i = 0 
        for itemSet in candidatedSet:
            jointEntropy = calcJointEntropy(self.X,itemSet,'discrete')
            item = {'attrSet':itemSet,'entropy':jointEntropy}
            entropyPairList.append(item)
            print ("Calulating the %d th entropy..." %(i))
            i = i + 1

        sortedEntropyPairList = sorted(entropyPairList,key = lambda x:x['entropy'])

        return sortedEntropyPairList

        
"""
def searchOptimal(X,attrTotalNum,selectedNum):
    
    candidatedSet = combinations(range(attrTotalNum),selectedNum)

    maxEntropy = -21400000
    optimalAttrSet = []
    for itemSet in candidatedSet:
        jointEntropy = calcJointEntropy(X,itemSet,'discrete')
        if jointEntropy >= maxEntropy:
            maxEntropy = jointEntropy
            optimalAttrSet = itemSet
        print itemSet,jointEntropy

    print ("The optimal attribute set is:\n")
    print optimalAttrSet,max

def informationGainMax(X,extendedSet,candidatedSet,n,threshold,maxEntropy):
    if len(extendedSet) >= n or len(candidatedSet) == 0:
        tmp = calcJointEntropy(X,extendedSet,'discrete')
        if tmp >= maxEntropy:
            maxEntropy = tmp
            print extendedSet,tmp
        return
    Ho = calcJointEntropy(X,extendedSet,'discrete')
    maxInfoGain = -21400000
    maxInfoGainAttr = 0
    for attr in candidatedSet:
        Hc = calcJointEntropy(X,(extendedSet|set([attr])),'discrete')
        increment = (Hc-Ho)/Ho
        if increment < threshold:
            candidatedSet.remove(attr)
        if Hc >= maxInfoGain:
            maxInfoGain = Hc
            maxInfoGainAttr = attr
    extendedSet.add(maxInfoGainAttr)
    if maxInfoGainAttr in candidatedSet:
        candidatedSet.remove(maxInfoGainAttr)

    informationGainMax(X,extendedSet,candidatedSet,n,threshold,maxEntropy)
"""




