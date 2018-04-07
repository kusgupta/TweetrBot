"""


A graph class for the underlying implementation of the Markov Model


"""

class Graph(object):

    def __init__(self):
        self.dictionary = {}

    # Pass only nodes in
    def addNode(self, node):
        if self.dictionary.get(node.value) is None:
            self.dictionary[node.value] = node
        return self.dictionary[node.value]

    def calculateProbability(self):
        for key, value in self.dictionary.items():
            value.updateProbabilities()

    def getNode(self, value):
        return self.dictionary[value]


class Node(object):

    def __init__(self, value):
        self.edgeDict = {}
        self.value = value
        self.count = 0
        self.listOfEdges = []

    def addEdge(self, value, label, nextNode, sentenceEnder=False):
        if value not in self.edgeDict:
            self.edgeDict[value] = Edge(label, nextNode.value, sentenceEnder)
        else:
            self.edgeDict[value].updateFrequency()
        self.count += 1

    def updateProbabilities(self):
        for key, value in self.edgeDict.items():
            value.probability = value.frequency / self.count

    def getEdge(self, value):
        return self.edgeDict[value]


class Edge(object):

    def __init__(self, label, nextNode, sentenceEnder):
        self.frequency = 1
        self.probability = 1
        self.label = label
        self.nextNode = nextNode
        self.sentenceEnder = sentenceEnder

    def updateFrequency(self):
        self.frequency = self.frequency + 1

    def getToken(self):
        return self.label

    def getProbability(self):
        return self.probability

    def getNextNode(self):
        return self.nextNode