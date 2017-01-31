# @Author: Sagar Makwana

from sys import argv
import re
import json

def getPrior(labels):
    result = {}
    for label in labels:
        if label in result:
            result[label] = result[label] + 1
        else:
            result[label] = 1
    
    for label in result:
        result[label] = result[label]*1.0/len(labels)
        
    return result


def getClassCorpus(corpus,labels,classLabel):
    resultCorpus = []
    labeliter = iter(labels)
    for entry in corpus:
        if labeliter.next() == classLabel:
            resultCorpus.append(entry)
    
    return resultCorpus

    
def buildBagofWordsModel(corpus):
    model = {}
    for entry in corpus:
        words = entry.split(' ')
        for word in words:
            if word not in model:
                word = word.strip()
                model[word] = {}
                model[word]['truthful'] = 0 
                model[word]['deceptive'] = 0
                model[word]['positive'] = 0
                model[word]['negative'] = 0
        
    return model  
    
    
    
def buildModelForClass(model,classCorpus,classLabel):
    wordcount = 0
    for entry in classCorpus:
        words = entry.split(' ')
        for word in words:
            word = word.strip()
            model[word][classLabel] += 1
            wordcount += 1
     
    for key in model:
        model[key][classLabel] = (model[key][classLabel] + 1.0)/(wordcount + len(model))
    



#File Loc
trainTextFileLoc = argv[1]
trainLabelFileLoc = argv[2]

#Raw file input
corpus = [re.sub(r'[^\w\s]','',line.rstrip('\n')).lower().split(' ', 1)[1] for line in open(trainTextFileLoc)]
trainLabel = [line.rstrip('\n') for line in open(trainLabelFileLoc)]

#List of labels
truthLabel = [line.split(' ')[1] for line in trainLabel]
sentimentLabel = [line.split(' ')[2] for line in trainLabel]

#Dictionaries of prior counts
truthPriorDict = getPrior(truthLabel)
sentimentPriorDict = getPrior(sentimentLabel)

#All class Corpuses
truthfulCorpus = getClassCorpus(corpus,truthLabel,'truthful')
deceptiveCorpus = getClassCorpus(corpus,truthLabel,'deceptive') 
positiveCorpus = getClassCorpus(corpus,sentimentLabel,'positive')
negativeCorpus = getClassCorpus(corpus,sentimentLabel,'negative')


model = buildBagofWordsModel(corpus)
buildModelForClass(model, truthfulCorpus, 'truthful')
buildModelForClass(model, deceptiveCorpus, 'deceptive')
buildModelForClass(model, positiveCorpus, 'positive')
buildModelForClass(model, negativeCorpus, 'negative')

with open('nbmodel.txt', 'w') as fp:
    json.dump(model, fp)