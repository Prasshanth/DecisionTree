import math
import sys

class Node:
    attribute = ""
    leftNode = None
    rightNode = None
    label = ""

    def __init__(self, attribute, leftNode, rightNode, label):
        self.attribute = attribute
        self.leftNode = leftNode
        self.rightNode = rightNode
        self.label = label


#Input: S is a list of entries in the data for which the entropy is to be calculated
#Output: Entropy for the list of entries given as input
def entropy(S):
    numZeros = 0
    numOnes = 0
    total = 0.0
    for value in S:
        total += 1
        if value[-1] == '0':
            numZeros += 1
        else:
            numOnes += 1
    valueOne = 0
    valueZero = 0
    if numOnes != 0:
        valueOne = numOnes/total * math.log(numOnes/total, 2)
    if numZeros != 0:
        valueZero = numZeros/total * math.log(numZeros/total, 2)
    
    return -valueOne - valueZero  

#Input: S is a list of entries, an attribute, and value for the AttributeError
#Output: list of entries which have the the value for the attribute
def attributeSubset(S, attribute, value):
    subset = []
    indexOfAttribute = columnToIndexMapping[attribute]
    for entry in S:
        if entry[indexOfAttribute] == value:
            subset.append(entry)
    return subset

#def columnToIndexMapping(attribute, attributes):
 #   index = 0
  #  for value in attributes:
   #     if value == attribute:
    #        return index
     #   else:
      #      index += 1
    #print "Attribute not in list"
    #print attribute
    #print attributes
    #return -1

#Input: List of entries S, attribute for which information gain is to be calculated
#Output: Information gain for the attribute calculated on the given entries
def informationGain(S, attribute):
    indexOfAttribute = columnToIndexMapping[attribute]
    sEntropy = entropy(S)
    subsetOne = attributeSubset(S, attribute, '0')
    subsetZero = attributeSubset(S, attribute, '1')
    #if len(subsetOne) == 0 or len(subsetZero) == 0:
     #   print S
      #  print attribute
       # print attributes
    
    return sEntropy - len(subsetOne)/len(S) * entropy(subsetOne) - len(subsetZero)/len(S) * entropy(subsetZero)

#Input: List of entries S 
#Output: True if class for all entries is positive, False if not
def allSamplesPositive(S):
    for entry in S:
        if entry[-1] == '0':
            return False
    return True

#Input: List of entries S 
#Output: True if class for all entries is negative, False if not
def allSamplesNegative(S):
    for entry in S:
        if entry[-1] == '1':
            return False
    return True

#Input: List of entries S
#Output: Most common class in all the entries
def mostCommonClass(S):
    numOnes = 0
    numZeros = 0
    for entry in S:
        if entry[-1] == "1":
            numOnes += 1
        if entry[-1] == "0":
            numZeros += 1
    if numOnes >= numZeros:
        return '1'
    else:
        return '0'

#Input: List of entries S, list of attributes
#Ouput: Attribute in list of attributes with highest information gain
def bestAttribute(S, attributes):
    bestAttribute = attributes[0]
    bestInfoGain = informationGain(S, bestAttribute)
    for attribute in attributes:
        attributeInfoGain = informationGain(S, attribute)
        if attributeInfoGain > bestInfoGain:
            bestInfoGain = attributeInfoGain
            bestAttribute = attribute
    #print "best attribute = " + bestAttribute
    return bestAttribute

#Input: List of entries S, list of attributes
#Output: Decision tree for the list of entries
def ID3(S, attributes):
    rootNode = Node("", None, None, "")
    if allSamplesPositive(S):
        rootNode.label = "1"
        return rootNode
    if allSamplesNegative(S):
        rootNode.label = "0"
        return rootNode
    if len(attributes) == 0:
        rootNode.label = mostCommonClass(S)
        return rootNode
    
    A = bestAttribute(S, attributes)
    rootNode.attribute = A
    attributes.remove(A)

    SViLeft = attributeSubset(S, A, "0")
    if len(SViLeft) == 0:
        rootNode.leftNode = Node("", None, None, mostCommonClass(S))
    else:
        rootNode.leftNode = ID3(SViLeft, list(attributes))

    SViRight = attributeSubset(S, A, "1")
    if len(SViRight) == 0:
        rootNode.rightNode = Node("", None, None, mostCommonClass(S))
    else:
        rootNode.rightNode = ID3(SViRight, list(attributes))
    
    return rootNode

def parse(treeRoot):
    parseTree(treeRoot, 0)

def parseTree(treeRoot, depth):
    if treeRoot.label != "":
        sys.stdout.write(treeRoot.label)
        sys.stdout.flush()
    else:
        sys.stdout.write("\n")
        for i in range(depth):
            sys.stdout.write('| ')
        sys.stdout.write(treeRoot.attribute + " = 0: ")
        sys.stdout.flush()
        parseTree(treeRoot.leftNode, depth + 1)
        sys.stdout.write("\n")
        for i in range(depth):
            sys.stdout.write('| ')
        sys.stdout.write(treeRoot.attribute + " = 1: ")
        sys.stdout.flush()
        parseTree(treeRoot.rightNode, depth + 1) 

def returnPrediction(treeRoot, entry):
    #print "label: " + treeRoot.label
    #print treeRoot.label != ""
    if treeRoot.label != "":
        #print treeRoot.label
        return treeRoot.label
    else:
        currentAttribute = treeRoot.attribute
        #print "currentAttribute = " + treeRoot.attribute
        currentAttributeIndex = columnToIndexMapping[currentAttribute]
        #print "currentAttributeIndex = " + str(currentAttributeIndex)
        #print "entry[currentAttributeIndex] = " + entry[currentAttributeIndex]
        if entry[currentAttributeIndex] == "0":
            return returnPrediction(treeRoot.leftNode, entry)
        else:    
            return returnPrediction(treeRoot.rightNode, entry)


trainingSetFile = open("training_set.csv", "r")
columnHeadings = trainingSetFile.readline().split(",")
columnHeadings = columnHeadings[0:-1]
columnToIndexMapping = {}

iter = 0
for heading in columnHeadings:
    columnToIndexMapping[heading] = iter
    iter += 1
data = []
for line in trainingSetFile:
    line = line[0:-1]
    data.append(line.split(","))

decisionTree = ID3(data, columnHeadings)

outfile = open("outputfile.txt", "w")
with outfile as f:
    sys.stdout = f
    parse(decisionTree)
sys.stdout = sys.__stdout__

testingSetFile = open("test_set.csv", "r")
testingSetFile.readline()
testData = []
for line in testingSetFile:
    line = line[0:-1]
    testData.append(line.split(","))

i = 0
c = 0.0
for sample in testData:
    i += 1
    print returnPrediction(decisionTree, sample) + " " + sample[-1]
    if returnPrediction(decisionTree, sample) == sample[-1]:
        c += 1

print "total = " + str(i)
print "numCorrect = " + str(c)
print "accuracy = " + str(c/i * 100)

    

    
    



