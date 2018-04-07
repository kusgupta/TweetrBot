"""


A tweet bot based off of past Donald Trump tweets.

Credit to Arthur Peters and Calvin Lin for the assignment.

I modified the initial assignment of a Markov Model to be an automatic Twitter bot that tweets at random times and
different length tweets consistently.

Function name outlines and name for class, generate function, generate file function, save and load pickle,
train_url, and trainIterable given by Arthur Peters

Function windowed given to me by Arthur Peters


"""

import pickle
import random
from graph import *
import requests


class MarkovChain(object):

    def __init__(self, level, tokenization=None):
        self.graph = Graph()
        self.tokenization = tokenization
        self.level = level
        self.sentenceEnders = ["!", "?", ".", "..."]

    # Generates words
    def generate(self):
        currentData = self.graph.dictionary[random.choice(list(self.graph.dictionary))]
        while (True):
            randomNumber = random.random()
            if currentData.edgeDict:
                for key, edge in currentData.edgeDict.items():
                    probability = edge.getProbability()
                    if randomNumber <= probability:
                        if self.level == 0:
                            currentData = self.graph.dictionary[random.choice(list(self.graph.dictionary))]
                        else:
                            currentData = self.graph.dictionary[(edge.getNextNode())]
                        yield edge.getToken()
                        break
                    else:
                        randomNumber = randomNumber - probability
            else:
                currentData = self.graph.dictionary[random.choice(list(self.graph.dictionary))]

    # Best to generate sentences with values of 2 or greater to prevent sentences too short like "We like U.S."
    def generateSentences(self, numSentences):
        sentenceAt = 0
        paragraph = ""
        g = self.generate()
        while(sentenceAt != numSentences):
            paragraph += str(next(g)) + " "
            # Checks if the last character in the sequence is punctuation that can end a sentence.
            if paragraph.split()[-1][-1] in self.sentenceEnders:
                sentenceAt += 1

        # Capitalizes first letter of the sentence.
        paragraph[0][0].capitalize()
        return paragraph


    # Pickles the markov model
    def save_pickle(self, filename_or_file_object):

        with open(str(filename_or_file_object), 'wb') as model:
            pickle.dump(self, model)


    # Loads a given markov model
    @classmethod
    def load_pickle(cls, filename_or_file_object):
        with open(str(filename_or_file_object), "rb") as model:
            markovModel = pickle.load(model)
        if isinstance(markovModel, MarkovChain):
            return markovModel
        else:
            raise TypeError()


    # Trains the model further using links. Will be used to train off most recent tweets with a greater weight given
    # to those tweets, not currently implemented
    def trainTweetsLive(self, url):
        r = requests.get(url=str(url))
        self.trumpTrainer(r.content.decode(encoding="utf-8", errors="strict"))


    # Function given by Arthur Peters, creates the window that slides over iterable training data
    def windowed(self, iterable, size):
        if size < 1:
            size = 1
        window = list()
        for v in iterable:
            if len(window) < size:
                window.append(v)
            else:
                window.pop(0)
                window.append(v)
            if len(window) == size:
                yield tuple(window)


    # The function that actually trains the model
    def trumpTrainer(self, data):
        prevNode = None
        data = self.tokenizeWord(data)
        for value in self.windowed((data), self.level):
            token = value[-1]
            node = Node(value)
            node = self.graph.addNode(node)
            if prevNode is not None:
                if token[-1] in ".!?":
                    prevNode.addEdge(value, token, node, True)
                else:
                    prevNode.addEdge(value, token, node)
            if self.level != 0:
                prevNode = node
            else:
                node.addEdge(value, token, node)
        self.graph.calculateProbability()

    # A tokenization for words
    def tokenizeWord(self, data):
        return data.split()
