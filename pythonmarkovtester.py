import TrumpModel
import pickle
import re
import string

rw = TrumpModel.MarkovChain(3, TrumpModel.Tokenization.word)
with open("Trump.txt") as f:
    string = f.read()
#string = re.sub(r'http\S+', '', string)

rw.trumpTrainer(string)
g = rw.generate()
print(rw.generateSentences(3))


## THIS IS JUST FOR A BUNCH OF WORDS
# rw.train_iterable(string)
# g = rw.generate()
# for x in range(500):
#     print(next(g) + " ", end="")




# rw = final.RandomWriter(2, final.Tokenization.character)
# rw.train_iterable("What a piece of work is man! how noble in reason! how infinite in faculty! in form and moving how express and admirable! "
#                   "in action how like an angel! in apprehension how like a god! the beauty of the world, the paragon of animals!")
# #blah = next(iter(dicto.keys()))

# g = rw.generate()
# for x in range(1, 100):
#     print(next(g) + " ")

#print(str(prevNode.value) + " " + str(prevNode.edgeDict))
#HOW TO TEST PROBABILITIES I'm so clueless...
#print(rando.graph.getNode(('A',)).edgeDict)
#print(rando.graph.getNode(('A',)).getEdge(('B',)).getProbability())
