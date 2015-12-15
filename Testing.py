from NeuralNetUtil import buildExamplesFromCarData,buildExamplesFromPenData,buildExamplesFromExtraData
from NeuralNet import buildNeuralNet
import cPickle
import os
import sys
from math import pow, sqrt
import xlwt

def average(argList):
    return sum(argList) / float(len(argList))

def stDeviation(argList):
    mean = average(argList)
    diffSq = [pow((val - mean), 2) for val in argList]
    return sqrt(sum(diffSq) / len(argList))

penData = buildExamplesFromPenData()
def testPenData(hiddenLayers = [24]):
    return buildNeuralNet(penData, maxItr = 200, hiddenLayerList = hiddenLayers)

carData = buildExamplesFromCarData()
def testCarData(hiddenLayers = [16]):
    return buildNeuralNet(carData, maxItr = 200, hiddenLayerList = hiddenLayers)

pokerData = buildExamplesFromExtraData()
def testPokerData(hiddenLayers = [10]):
    return buildNeuralNet(pokerData, maxItr = 200, hiddenLayerList = hiddenLayers)

def questionFiveAnalysis(numPerceptrons = -1, noPrinting = 0, questionSix = 0):
    out = sys.stdout
    penResults = range(5)
    maxPen = 0
    totalPen = 0

    carResults = range(5)
    maxCar = 0
    totalCar = 0

    for i in range(5):
        if (questionSix == 0):
            print 'Trial %d: Pen' % (i + 1)

        if (noPrinting):
            sys.stdout = open(os.devnull, 'w')

        if (numPerceptrons == -1):
            penResults[i] = testPenData()[1]
        else:
            if numPerceptrons != 0:
                penResults[i] = testPenData([numPerceptrons])[1]
            else:
                penResults[i] = testPenData([])[1]
        if (penResults[i] > maxPen):
            maxPen = penResults[i]

        if (noPrinting):
            sys.stdout = out
        if (questionSix == 0):
            print 'Trial %d: Car' % (i + 1)
        if (noPrinting):
            sys.stdout = open(os.devnull, 'w')

        if (numPerceptrons == -1):
            carResults[i] = testCarData()[1]
        else:
            if numPerceptrons != 0:
                carResults[i] = testCarData([numPerceptrons])[1]
            else:
                carResults[i] = testCarData([])[1]
        totalCar += carResults[i]
        if (carResults[i] > maxCar):
            maxCar = carResults[i]
        totalPen += penResults[i]

        if (noPrinting):
            sys.stdout = out

    avgPen = totalPen / 5.0
    avgCar = totalCar / 5.0
    varPen = 0
    varCar = 0
    for i in range(5):
        varPen += pow(penResults[i] - avgPen, 2)
        varCar += pow(carResults[i] - avgCar, 2)

    stdPen = sqrt(varPen)
    stdCar = sqrt(varCar)
    if (questionSix == 0):
        print '\n\nPen data accuracy:'
        print 'Max: %f; Average: %f; Standard Deviation: %f\n' % (maxPen, avgPen, stdPen)
        print 'Car data accuracy:'
        print 'Max: %f; Average: %f; Standard Deviation: %f' % (maxCar, avgCar, stdCar)

    return [(maxPen, avgPen, stdPen), (maxCar, avgCar, stdCar)]

def questionSixAnalysis():
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("Sheet1")
    sheet1.write(1, 1, "Number of perceptrons")
    sheet1.write(1, 2, "Max accuracy")
    sheet1.write(1, 4, "Average accuracy")
    sheet1.write(1, 6, "Standard Deviation")
    sheet1.write(2, 2, "Pen")
    sheet1.write(2, 3, "Car")
    sheet1.write(2, 4, "Pen")
    sheet1.write(2, 5, "Car")
    sheet1.write(2, 6, "Pen")
    sheet1.write(2, 7, "Car")

    print '|-----------------------------------------------------------------------|'
    print '| \t    Pen\t\t\t|| \t\t    Car\t\t\t|'
    print '|  Max\t|  Avg\t|     StdDev\t||\tMax\t|  Avg\t|     StdDev\t|'
    print '|-----------------------------------------------------------------------|'
    numPerceptrons = 0
    while numPerceptrons <= 40:
        results = questionFiveAnalysis(numPerceptrons, 1, 1)
        print '| %.3f\t| %.3f\t|     %.3f\t||     %.3f\t| %.3f\t|     %.3f\t|num=%d' % (results[0][0], results[0][1], results[0][2], results[1][0], results[1][1], results[1][2], numPerceptrons)
        sheet1.write(numPerceptrons / 5 + 3, 1, numPerceptrons)
        sheet1.write(numPerceptrons / 5 + 3, 2, results[0][0])
        sheet1.write(numPerceptrons / 5 + 3, 3, results[1][0])
        sheet1.write(numPerceptrons / 5 + 3, 4, results[0][1])
        sheet1.write(numPerceptrons / 5 + 3, 5, results[1][1])
        sheet1.write(numPerceptrons / 5 + 3, 6, results[0][2])
        sheet1.write(numPerceptrons / 5 + 3, 7, results[1][2])
        numPerceptrons += 5
    print '|-----------------------------------------------------------------------|'

    book.save("Question Six Analysis.xls")

def learnXOR():
    examples = ([([0, 0], [0]), ([0, 1], [1]), ([1, 0], [1]), ([1, 1], [0])], [([0, 0], [0]), ([0, 1], [1]), ([1, 0], [1]), ([1, 1], [0])])
    iter = float("infinity")
    num = 0
    while iter != 1:
        if num != 0:
            results = buildNeuralNet(examples, maxItr = 100000, hiddenLayerList = [num])
        else:
            results = buildNeuralNet(examples, maxItr = 100000, hiddenLayerList = [])
        print '%d nodes in the hidden layer achieved %f accuracy\n\n' % (num, results[1])
        num += 1
        iter = results[1]

def questionEightAnalysis():
    results = range(5)
    for i in range(len(results)):
        print 'Trial ', (i + 1)
        results[i] = testPokerData(hiddenLayers = [5])[1]
        print '5 nodes in the hidden layer achieved %f accuracy\n\n' % (results[i])

    maxAcc = max(results)
    totalAcc = 0
    for i in range(len(results)):
        totalAcc += results[i]
    avgAcc = totalAcc / len(results)
    varAcc = 0
    for i in range(len(results)):
        varAcc += pow(results[i] - avgAcc, 2)
    stdAcc = sqrt(varAcc)

    print 'Maximum Accuracy: ', maxAcc
    print 'Average Accuracy: ', avgAcc
    print 'Standard Deviation: ', stdAcc



"""Uncomment and comment the lines below according to which methods you want to call"""
#testCarData()
#testPenData()
#testPokerData()

#questionFiveAnalysis()
#questionSixAnalysis()
#learnXOR()
questionEightAnalysis()