import math

class Node:
    attribute = ""
    leftNode = None
    rightNode = None
    label = None

    def __init__(self, attribute, leftNode, rightNode, label):
        self.attribute = attribute
        self.leftNode = leftNode
        self.rightNode = rightNode
        self.label = label


#Input: S is a list of entries in the data for which the entropy is to be calculated
#Output: Entropy for the list of entries given as input
def calculateEntropy(S):
    numZeros = 0
    numOnes = 0
    total = 0.0
    for value in S:
        total += 1
        if value[-1] == '0':
            numZeros += 1
        else:
            numOnes += 1
    return -numZeros/total * math.log(numZeros/total, 2) - numOnes/total * math.log(numOnes/total, 2)   

def calculateInformationGain(S, attribute):
    indexOfAttribute = columnToIndexMapping[attribute]




trainingSetFile = open("training_set.csv", "r")
columnHeadings = trainingSetFile.readline().split(",")
columnHeadings[-1] = columnHeadings[-1][0:-1]
columnToIndexMapping = {}
i = Node()

iter = 0
for heading in columnHeadings:
    columnToIndexMapping[heading] = iter
    iter += 1
data = []
allPositive = True
allNegative = True
for line in trainingSetFile:
    line = line[0:-1]
    data.append(line.split(","))
    if data[-1][-1] == '1':
        allNegative = False
    if data[-1][-1] == '0':
        allPositive = False


    
    



