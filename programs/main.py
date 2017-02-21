#!/usr/bin/env python
# coding=utf-8
# import packages
import sys
import numpy as np
import pdb
import random
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import tree
from fileIO import *
from algo import *

def generateSubdataset(X,Y,recordNum):

    subX = []
    subY = []

    subsetRecordNumberSet = random.sample(range(len(X)),recordNum)
    for i in subsetRecordNumberSet:
        subX.append(X[i])
        subY.append(Y[i])
    return subX,subY

def cross_validation(X,Y,method):

    """
    trainSampleNumber = trainNumber
    testSampleNumber = testNumber
    
    trainSampleSet = random.sample(range(len(X)),trainSampleNumber)
    trainX = []
    trainY = []
    for i in range(len(trainSampleSet)):
        trainX.append(X[i])
        trainY.append(Y[i])

    testSampleSet = random.sample(range(len(X)),testSampleNumber) 
    testX = []
    testY = []
    for i in range(len(testSampleSet)):
        testX.append(X[i])
        testY.append(Y[i])
    """

    SampleNumSet = random.sample(range(len(X)),len(X))
    ten_fold_X = []
    ten_fold_Y = []
    for i in range(10):
        subsetX = []
        subsetY = []
        for j in range(int(len(X)/10.0*i),int(len(X)/10.0*(i+1))):
            subsetX.append(X[SampleNumSet[j]])
            subsetY.append(Y[SampleNumSet[j]])
        ten_fold_X.append(subsetX)
        ten_fold_Y.append(subsetY)
    result = 0
    for i in range(10):
        testX = ten_fold_X[i]
        testY = ten_fold_Y[i]
        trainX = []
        trainY = []
        for j in range(10):
            if j != i:
                for item in ten_fold_X[j]:
                    trainX.append(item)
                for item in ten_fold_Y[j]:
                    trainY.append(item)
        #support vector machine
        if method == 'svm':
            clf = svm.SVC(decision_function_shape='ovo')
            clf.fit(trainX,trainY)
        #neural network
        if method == 'nn':
            clf = MLPClassifier(solver='lbfgs',alpha=1e-5,
                            hidden_layer_sizes=(8,4),random_state=1)
            clf.fit(trainX,trainY)
        #naive bayes
        if method =='nb':
            clf = GaussianNB()
            clf.fit(trainX,trainY)
        #decision tree
        if method =='tree':
            clf = tree.DecisionTreeClassifier()
            clf.fit(trainX,trainY)
        #lda
        if method =='lda':
            clf = LinearDiscriminantAnalysis()
            clf.fit(trainX,trainY)

        count = 0
        predictResult = clf.predict(testX)
        for i in range(len(predictResult)):
            if predictResult[i] == testY[i]:
                count = count + 1
        result  = result + (count*1.0/len(testY))
    """
    #support vector machine
    if method == 'svm':
        clf = svm.SVC(decision_function_shape='ovo')
        clf.fit(trainX,trainY)
    #neural network
    if method == 'nn':
        clf = MLPClassifier(solver='lbfgs',alpha=1e-5,
                           hidden_layer_sizes=(8,4),random_state=1)
        clf.fit(trainX,trainY)
    #naive bayes
    if method =='nb':
        clf = GaussianNB()
        clf.fit(trainX,trainY)
    #decision tree
    if method =='tree':
        clf = tree.DecisionTreeClassifier()
        clf.fit(trainX,trainY)

    count = 0
    predictResult = clf.predict(testX)
    for i in range(len(predictResult)):
        if predictResult[i] == testY[i]:
            count = count + 1
    
    """
    return result/10.0
    


if __name__ == "__main__":
    
    X,Xt,Y,totalRecordNum,totalAttributeNum = LoadLargeContinuousDataFromTxt(sys.argv[1])

    """
        the experiment about different number of attributes
    """
   
    '''
    resultPairList = []
    for maxAttrNum in range(1,totalAttributeNum+1):

        trainAttrSet = set([i for i in range(maxAttrNum)])
        trainX = []
        for i in trainAttrSet:
            trainX.append(Xt[i])
        trainX = map(list, zip(*trainX))
        print ("the %d th experiment..."% (maxAttrNum))
        print ("Calculating entropy...")
        entropy = calcJointEntropy(trainX,trainAttrSet,'discrete')
        
        # 10-fold cross validation with 3 classifiers
        print ("Calculating SVM ...")
        svmResult = cross_validation(trainX,Y,'svm')
        print ("Calculating decision tree ...")
        treeResult = cross_validation(trainX,Y,'tree')
        print ("Calculating LDA ...")
        ldaResult = cross_validation(trainX,Y,'lda')

        resultItem = {'entropy':entropy,'svmResult':svmResult,'treeResult':treeResult,'ldaResult':ldaResult}
        resultPairList.append(resultItem)
    
 
    resultPairList = sorted(resultPairList,key = lambda x:x['entropy'])
    writeFileName = str(sys.argv[1])+'_experiment_2.txt_with_3_classifiers'
    file = open(writeFileName,'w+')
    
    """
    str2 = "["
    for item in resultPairList:
        str2 = str2 + str(item['entropy']) + ','
    str2 = str2 + ']'
 
    file.write(str2+'\n')
    str3 = "["
    for item in resultPairList:
        str3 = str3 + str(item['predictResult']) + ','
    str3 = str3 + ']'
    file.write(str3)
    """

    for item in resultPairList:
        file.write("%f\t%f\t%f\t%f\n" %(item['entropy'],item['svmResult'],item['treeResult'],item['ldaResult']))
    print ("Successfully saved the result in the form of text doc!")
    file.close()
    '''

    """
        the experiment about different size dataset
    """
    
    writeFileName = str(sys.argv[1])+'_'+'_experiment_3_with_3_classifiers.txt'
    
    print writeFileName

    file = open(writeFileName,'w+')   
    
    resultPairList = []
    ratio = []
    ratioDegree = 20
    for item in range(1,ratioDegree+1,1):
        ratio.append(1.0/ratioDegree*item)
    #subsetRecordNumber = int(totalRecordNum*0.75)
    for r in ratio:
        subsetRecordNumber = int(totalRecordNum*r)
        print ("generating the %f percent dataset with %d records" %(r,subsetRecordNumber))
        tmpX,tmpY = generateSubdataset(X,Y,subsetRecordNumber)
        print ("calculating corresponding entropy...")
        entropy = calcJointEntropy(tmpX,[attr for attr in range(totalAttributeNum)],'discrete')
        print ("10-fold cross validating...")

        # 10-fold cross validation with 3 classifiers
        print ("Calculating SVM ...")
        svmResult = cross_validation(tmpX,tmpY,'svm')
        print ("Calculating decision tree ...")
        treeResult = cross_validation(tmpX,tmpY,'tree')
        print ("Calculating LDA ...")
        ldaResult = cross_validation(tmpX,tmpY,'lda')

        resultItem = {'entropy':entropy,'svmResult':svmResult,'treeResult':treeResult,'ldaResult':ldaResult}
        resultPairList.append(resultItem)

    resultPairList = sorted(resultPairList,key = lambda x:x['entropy'])
    for item in resultPairList:
        file.write("%f\t%f\t%f\t%f\n" %(item['entropy'],item['svmResult'],item['treeResult'],item['ldaResult']))
   
    '''
    str1 = "["
    for item in ratio:
        str1 = str1 + str(item) + ','
    str1 = str1 + ']'
    file.write(str1+'\n')
    str2 = "["
    for item in resultPairList:
        str2 = str2 + str(item['entropy']) + ','
    str2 = str2 + ']'
 
    file.write(str2+'\n')
    str3 = "["
    for item in resultPairList:
        str3 = str3 + str(item['predictResult']) + ','
    str3 = str3 + ']'

    file.write(str3)
    
    #for item in resultPairList:
    #    file.write("%f\t%f\n" % (item['entropy'],item['predictResult']))
    '''
    print ("Successfully saved the result in the form of text doc!")
    file.close()
    
    
    
    
    """
        the experiment about the same number of attributes with different entropies
    """
    """
    if totalAttributeNum >=20: 
        expectedAttrNum = 2
    elif totalAttributeNum >=10:
        expectedAttrNum = 3
    else:
        expectedAttrNum = 4

    infoCalc = informationGainCalc(X,expectedAttrNum,0.0001)

    print ("Calculating information entropy ...")

    entropyPairList = infoCalc.searchAll(totalAttributeNum,expectedAttrNum)

    writeFileName = str(sys.argv[1])+'_experiment_1_with_3_classifiers.txt'
    
    print writeFileName

    file = open(writeFileName,'w+')   
     
    if totalRecordNum <= 500:
        trainSampleNumber = int(len(X)*0.85)
        testSampleNumber = int(len(X)*0.15)
    elif totalRecordNum <= 1000:   
        trainSampleNumber = int(len(X)*0.5)
        testSampleNumber = int(len(X)*0.1)
    else:   
        trainSampleNumber = int(len(X)*0.05)
        testSampleNumber = int(len(X)*0.01)


    resultPairList = []

    j=0
    for item in entropyPairList:
        trainAttrSet = item['attrSet']
        trainX = []
        print ("The %d th attribute set experiment..." %(j+1))
        j=j+1
        for i in trainAttrSet:
            trainX.append(Xt[i])
        trainX = map(list, zip(*trainX))
        # 10-fold cross validation with 3 classifiers
        print ("Calculating SVM ...")
        svmResult = cross_validation(trainX,Y,'svm')
        print ("Calculating decision tree ...")
        treeResult = cross_validation(trainX,Y,'tree')
        print ("Calculating LDA ...")
        ldaResult = cross_validation(trainX,Y,'lda')

        resultItem = {'entropy':item['entropy'],'svmResult':svmResult,'treeResult':treeResult,'ldaResult':ldaResult}
        resultPairList.append(resultItem)

     
    resultPairList = sorted(resultPairList,key = lambda x:x['entropy'])
    for item in resultPairList:
        file.write("%f\t%f\t%f\t%f\n" %(item['entropy'],item['svmResult'],item['treeResult'],item['ldaResult']))

    file.close()
    print ("Successfully saved the result in the form of text doc!")

    """

    """
       the accuracy comprision between the primitive search and the recursiving search
    """
    """
    expectedAttrNumSet = [i for i in range(1,totalAttributeNum+1)]

    for expectedAttrNum in expectedAttrNumSet:

        infoCalc = informationGainCalc(X,expectedAttrNum,0.0001)

        for i in range(totalAttributeNum):
            candidatedSet = set([j for j in range(totalAttributeNum)])
            candidatedSet.remove(i)
            extendedSet = set([i])
            infoCalc.informationGainMax(extendedSet,candidatedSet)
     
        print ("The optimal attribute set obtained by recursiving is:")
        print infoCalc.maxEntropyAttrSet,infoCalc.maxEntropy

        infoCalc.searchOptimal(totalAttributeNum,expectedAttrNum)

    """

    """
    expectedAttrNum = 4

    infoCalc = informationGainCalc(X,expectedAttrNum,0.0001)

    for i in range(totalAttributeNum):
        candidatedSet = set([j for j in range(totalAttributeNum)])
        candidatedSet.remove(i)
        extendedSet = set([i])
        infoCalc.informationGainMax(extendedSet,candidatedSet)
     
    print ("The optimal attribute set obtained by recursiving is:")
    print infoCalc.maxEntropyAttrSet,infoCalc.maxEntropy

    infoCalc.searchOptimal(totalAttributeNum,expectedAttrNum)
    """


    """
    file = open('svm_result.txt','w+')   
    
    print ("Starting %s fitting ..." %(sys.argv[2]))

    file.write("The prediction result of %s\n" %(sys.argv[2])) 
    trainSampleNumber = int(len(X)*0.1)
    testSampleNumber = int(len(X)*0.05)

    for maxAttrNum in range(1,totalAttributeNum+1):
        trainAttrSet = set([i for i in range(maxAttrNum)])
        trainX = []
        for i in trainAttrSet:
            trainX.append(Xt[i])
        trainX = map(list, zip(*trainX))
        print ("the %d th experiment"% (maxAttrNum))
        result =  cross_validation(trainX,Y,trainSampleNumber,testSampleNumber,sys.argv[2])  
        file.write("%d %f\n" % (maxAttrNum,result))

    file.close()
    print ("Successfully saved the result in the form of text doc!")
    """
    """
    trainNumberSet = []
    testNumberSet = []

    for i in range(10):
        trainNumberSet.append(trainSampleNumber)
        testNumberSet.append(testSampleNumber)

    trainAttrSet = [i for i in range(totalAttributeNum)]

    trainX = []
    for i in trainAttrSet:
        trainX.append(Xt[i])
    trainX = map(list, zip(*trainX))

    file = open('predictResult.txt','w+')
    
    print ("Starting %s fitting ..." %(sys.argv[2]))

    file.write("The prediction result of %s\n" %(sys.argv[2])) 
    file.write("train sample number, train sample number, accuracy\n")
    for i in range(10):
      result =  cross_validation(trainX,Y,trainNumberSet[i],testNumberSet[i],sys.argv[2])
      print ("the %d times prediction." %(i+1))
      file.write("%d %d %f\n" % (trainNumberSet[i],testNumberSet[i],result))
    
    file.close()

    print ("Successfully saved the result in the form of text doc!")
    """
