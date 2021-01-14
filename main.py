from collections import defaultdict, Counter
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import stopwords, brown
import re

category = 'news'
stop_Words = stopwords.words("english")
# Normalization
''' text level ---> segmentation, tokenization, delete stop-words
    word level ---> splite,extract,delete,replace string 
    character level ---> case
'''

#01 Segmentation

sentences = brown.sents(categories=category)


tokens = brown.words(categories=category)
new_token = []
for w in tokens:
    word = re.sub(r'[-[_\],`.!?():{}&$#@%*+;/\'"\t\n\b0-9]', r'', w.lower())
    if word != '' and word not in stop_Words:
        new_token.append(word)

row_text = ' '.join(new_token)
#unsupervised learning ML alogrithm to detect end of sentences (EOS)
custom_sent_tokenizer = PunktSentenceTokenizer(row_text)
tokenized = custom_sent_tokenizer.tokenize(row_text)
last_text = ' '.join(tokenized)
#prediction Algorithm
def markov_chain(text):
    words = text.split(' ')
    myDict = defaultdict(list)
    for currentWord, nextWord in zip(words[0:-1], words[1:]):
        myDict[currentWord].append(nextWord)
    myDict = dict(myDict)
    return myDict

markov_return = markov_chain(last_text)
numOfKeys = len(markov_return)
listOfKeys = list(markov_return)

inputText = input("Enter your line: ")
input_tokens = inputText.split(' ')
input_tokens.insert(0, '<start>')

tokens = last_text.split(' ')
biGrams = []
i = 0
tempOfKeys = int(numOfKeys)
prediction = []
while tempOfKeys > 0:
    if input_tokens[-1] == listOfKeys[tempOfKeys - 1]:
        prediction = markov_return[listOfKeys[tempOfKeys - 1]]
        print(set(prediction))
    tempOfKeys = tempOfKeys - 1
    item = tokens[i] + ' ' + tokens[i + 1]
    biGrams.append(item)
    i = i + 1

if len(prediction) != 0:
    count = Counter(biGrams)
    tempNumOfPre = int(len(prediction))
    listOfFinal = []
    y = 0
    while tempNumOfPre > 0:
        predAndInput = input_tokens[-1] + ' ' + prediction[y]
        listOfFinal.append(predAndInput)
        y = y + 1
        tempNumOfPre = tempNumOfPre - 1


#Smoothing
    x = 0
    dic = dict()
    keys = []
    values = []
    numOfPrediction = len(prediction)
    z = 0
    counter_ = len(biGrams)
    while numOfPrediction > 0:
        while counter_ > 0:
            if listOfFinal[z] == biGrams[x]:
                keys.append(biGrams[x])
                values.append((count[biGrams[x]] + 1) / (numOfPrediction + numOfKeys))
            x = x + 1
            counter_ = counter_ - 1
        numOfPrediction = numOfPrediction - 1
        z = z + 1

    if (len(values) != 0):
        for x,y in zip(keys,values):
            dic[x] = y
        result = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1])}
        print('We recommend this word to you : ', str(list(result)[-1]).split()[-1])
else:
    print('No Predictions')
