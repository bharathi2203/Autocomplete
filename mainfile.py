#################################################
# TERM PROJECT --- TP3
#
# Your name: BHARATHI  SRIDHAR
# Your andrew id: bsridha2
#################################################

import math, copy, os, random, string
from collections import Counter
from cmu_112_graphics import *
import nltk 
from nltk.tokenize import sent_tokenize
from nltk.util import ngrams

#nltk.corpus.gutenberg.fileids() 

###################################################################
# PREPROCESSING
###################################################################

#All text is from https://www.gutenberg.org/
"""
f = open("testing.txt", "r", encoding='utf-8')
text = f.read()
f.close()

"""
#top 10k words in english language is from the following URL
#https://www.mit.edu/~ecprice/wordlist.10000

f = open("EnglistDictionary.txt", "r", encoding='utf-8')
engWords = f.read()
f.close()

#engWords = engWords.split(" ")
#wordList = text.split(" ")
#rawtext = text

def cleanText(text):
    punc = "!#$%&'()*+,-/:;<=>?@[\]^_`{|}~—" + "“" + "\n" + "”" + "’"
    new = ""
    for x in text:
        if x in punc:
            new += " "
        else:
            new += x 
    return new

#text = cleanText(text)

def getSentences(text):
    new = ''
    for x in text:
        if x == '\n':
            new += ' '
        else:
            new += x
    temp = sent_tokenize(new)
    return temp 

def writeSentencesIntoFile(sents):
    f = open('sentences.txt', 'a+')
    new = ''
    for x in sents:
        t = x.split(' ')
        if 8< len(t) < 17:
            try:
                new = x + '\n'
                f.write(new)
            except:
                pass
    #new = new.strip()
    
    #f.write(new)
    f.close()
    print('DONE WRITING SENTENCES!')

#dispSentence = getSentences(rawtext)
#writeSentencesIntoFile(dispSentence)
#sentences = getSentences(text)

def fileToSentences():
    f = open('sentences.txt', 'r')
    sent = f.read()
    f.close()
    sent = sent.split('\n')
    return sent

dispSentence = fileToSentences()
print('SENTENCES PROCESSED!')

#TOKENIZING
def getTokens(textString):
    tokens = nltk.word_tokenize(textString)
    L = []
    for x in tokens:
        L.append(x.lower())
    return L

#tokens = getTokens(text)
#print("No of tokens: ", len(tokens))

#TAGGING
def getTags(tokens):
    tags = nltk.pos_tag(tokens)
    return tags

tagDict = {'CC': 'oordinating conjunction','CD': 'cardinal digit','DT': 'determiner','EX': 'existential there',
            'FW': 'foreign word', 'IN': 'preposition','JJ': 'adjective','JJR': 'comparitive adjective',
            'JJS': 'superlative adjective','NN': 'noun','NNS': 'plural noun', 'NNP': 'proper noun', 
            'NNPS': 'plural proper noun','PDT': 'predeterminer','POS': 'possessive noun','PRP': 'personal pronoun',
            'PRP$': 'possessive pronoun','RB': 'adverb','RBR': 'adverb','RBS': 'adverb','VB': 'verb',
            'VBD': 'verb, past tense','VBN': 'past participle','VBP': 'verb, present'}


from nltk.probability import ConditionalFreqDist
# from nltk documentation https://www.nltk.org/_modules/nltk/probability.html
def build_cfdist(tokens):
    cfdist = ConditionalFreqDist()
    for t in tokens:
        cfdist[len(t)][t] += 1
    return cfdist

#cfdist = build_cfdist(tokens)
#print(cfdist[7], type(cfdist[7]))
#fdw = cfdist[7]
#print(cfdist[7].freq("because"))
#print(cfdist[7]["because"])

def freqdistToDic(freqdist, tokens):
    d = {}
    for t in tokens:
        if t in freqdist:
            if t not in d:
                d[t] = 1 
            else:
                d[t] += 1 
    return d 

#print(freqdistToDic(cfdist[14], tokens))

def buildFreqDist(words):
    d = {} 
    for x in words:
        if x not in d:
            d[x] = 1 
        else:
            d[x] += 1 
    return d 


#altfreq = Counter(tokens)
#print(altfreq.most_common(10))
#print(altfreq)

#~~~~~N-GRAMS~~~~~~
#https://web.stanford.edu/~jurafsky/slp3/slides/LM_4.pdf (theory stuff)

def get_ngrams(text, n, sentences):
    print("ngram-ming")
    result = []
    for line in sentences:
        t = ngrams(nltk.word_tokenize(line), n) #return zip file 
        ngrams_list = []
        for x in t:
            ngrams_list.append(' '.join(x))
        result += ngrams_list
    L = []
    for x in result:
        L.append(x.lower())
    return L

def preprocess(text, sentences):
    ngramsAll = get_ngrams(text,2, sentences) + get_ngrams(text,3, sentences) 
    #ngramsAll += get_ngrams(text,4, sentences) 
    #ngramsAll += get_ngrams(text,5, sentences)
    print("preprocessing")
    return ngramsAll

#ngramsList = preprocess(text,sentences)

def writeNgrams(fpath, ngramsList):
    print("writing")
    f = open(fpath, "w", encoding='utf-8')
    temp = ""
    for i in range(len(ngramsList)):
        temp += ngramsList[i] + "\n" 
        if i%1000 == 0:
            print(i, len(ngramsList))
    f.write(temp)
    f.close()
    return True

def txtfileToNgrams(fpath):
    f = open(fpath, "r", encoding='utf-8')
    text = f.read()
    ngramsList = text.split('\n')
    f.close()
    return ngramsList 

#writeNgrams("ngrams.txt", ngramsList)
#print("Done writing into file")


#f = open("ngrams.txt", "r", encoding='utf-8')
#ngramsList = f.read().split("\n")
#f.close()
#print("Ngrams read!")


###################################################################
# PROBABILITY + FREQUENCY & MARKOV CHAIN PREP
###################################################################
#https://www.nltk.org/_modules/nltk/parse/generate.html (nltk documentation)
#https://web.stanford.edu/~jurafsky/slp3/3.pdf (more theory)

#~~~~~~~~~~~BUILDING MARKOV MODEL~~~~~~~~~~~~

#set up probabilities
def buildRelativeFreq(ngramsList):
    d = {}
    for phrase in ngramsList:
        phrase.strip()
        for i in range(1,len(phrase)-2):
            m = len(phrase)**.25
            temp = phrase.split(" ")[:i]
            first = temp[0]
            rest = " ".join(temp[1:])
            if first not in d:
                temp = {}
                d[first] = temp 
                d[first][rest] = 1*m
            else:
                if rest in d[first]:
                    d[first][rest] += 1*m
                else:
                    d[first][rest] = 1*m
    #print(d)
    return d

def convertFreqtoProb(d):
    for phrase in d:
        partSum = 0
        for temp in d[phrase]:
            if temp != '':
                partSum += d[phrase][temp] 
        for temp in d[phrase]:
            if temp != '':
                d[phrase][temp] = d[phrase][temp]/partSum
    return d

#probDist = convertFreqtoProb(buildRelativeFreq(ngramsList))
#print("pDist processed!")

#~~~~~~~~~~~Reading\Writing probDist into file~~~~~~~~~~~~~~~~~~~~
def dictToStr(d):
    s = ""
    for key in d:
        s += key + "," + str(d[key]) + "*"
    return s[:len(s)-1]

def strToDict(s):
    d = {}
    lines = s.split("*")
    for t in lines:
        t = t.split(",")
        d[t[0]] = float(t[1])
    return d

def twoDdictToStr(d):
    s = ""
    i = 0
    for key in d:
        i += 1
        if len(d[key]) != 0: 
            s += key + ":" + dictToStr(d[key]) + "\n"
        print(i, len(probDist))
    s.strip()
    return s

def strTo2dDict(s):
    d = {}
    for line in s.split("\n"):
        temp = line.split(":")
        if len(temp) == 2:
            try:
                d[temp[0]] = strToDict(temp[1])
            except:
                print(d[temp[0]],temp[1])
    return d  


def writePdistToFile(path, probDist):
    t = twoDdictToStr(probDist)
    f = open(path, "w")
    for x in t:
        try: 
            f.write(x)
        except:
            f.write(" ")
    f.close()
    print("Done WRITING PDIST IN DOC")

#writePdistToFile("probdist.txt", probDist)

f1 = open("probdist.txt", "r")
pdist = f1.read()
f1.close()

probDist = strTo2dDict(pdist)

print("pdist processed!")

#invProbDist = getInvDist(probDist)
#print(len(probDist), len(invProbDist))

#~~~~~~~~~~~~~~~~BUILDING REVERSE PROB DIST~~~~~~~~~~~~~~~~~~~~~~~~


def reverseFreqDist(ngramsList):
    d = {}
    for phrase in ngramsList:
        phrase.strip()
        for i in range(len(phrase)-2,1,-1):
            m = len(phrase)**.25
            temp = phrase.split(" ")[:i]
            rest = temp[0]
            last = " ".join(temp[1:])
            if last not in d:
                temp = {}
                d[last] = temp 
                d[last][rest] = 1*m
            else:
                if rest in d[last]:
                    d[last][rest] += 1*m
                else:
                    d[last][rest] = 1*m
    return d

#revProbDist = convertFreqtoProb(reverseFreqDist(ngramsList))

#writePdistToFile("revprobdist.txt", revProbDist)

f1 = open("revprobdist.txt", "r")
revpdist = f1.read()
f1.close()
revProbDist = strTo2dDict(revpdist)

print("revprobdist processed!")


###########################################################
#SENTENCE GENERATION
###########################################################

def pseudoRandomSentenceGenerator(dispSentence):
    s = "s"
    try:
        while (not (8 < len(s.split(" ")) < 17)):
            s = random.choice(dispSentence)
        return s
            #return s.replace('\n', " ")
    except:
        return pseudoRandomSentenceGenerator(dispSentence)
    """
    s = "s"
    while (7 < len(s.split(" ")) < 15):
        try:
            s = random.choice(dispSentence)
            return s.replace('\n', " ")
        except:
            return pseudoRandomSentenceGenerator(dispSentence)
    """
   

#takes in distribution of n-grams, and sentence in progress
#returns given sentence + predicted phrase 
def pickNextPhrase(probDist , prev):
    if prev not in probDist:
        return random.choice(probDist.items())
    new = probDist[prev]
    temp = Counter(new)
    temp = temp.most_common(5)
    choices = []
    for (choice, prob) in temp:
        if choice != '':
            choices.append(choice)
    return random.choice(choices)

def generateSentence(probDist, n, starting):
    sentence = starting + " "
    while len(sentence) < n:
        temp = sentence.split()[-1]
        sentence += pickNextPhrase(probDist, temp)
        sentence += " "
    return sentence

###################################################################
# AUTOCOMPLETE
#https://en.wikipedia.org/wiki/Markov_chains_on_a_measurable_state_space
#https://en.wikipedia.org/wiki/Hidden_Markov_model 
#https://web.stanford.edu/~jurafsky/slp3/A.pdf (lots of imp ideas & theory)
###################################################################

#w = preprocess(text) 
#w = Counter(tokens)
#w = buildFreqDist(tokens)

def findPossibilities(w, p):
    result = set()
    for key in w:
        if p == (key[0:len(p)]):
            result.add(key)
    return result 

def miniauto(w):
    p = ""
    new = "a"
    while (new.isalpha() or new.isspace()):
        new = str(str(input(f"Enter letter:        {p}")))
        p = p + new
        t = (findPossibilities(w, p))
        #print(t)
        if len(t) == 1:
            return t 
        elif len(t) == 0:
            if p not in set(engWords):
                return "Invalid word."
        elif len(t) < 10:
            print(t)
    return t 

############################################
# MAKE SENTENCES
############################################
def makeBrokenSentence(s, n):
    temp = s.split()
    print(temp)
    i = 0
    answer = ''
    try:
        try:
            while i < n:
                a = random.randint(2,len(temp) - 2)
                word = temp[a]
                if 3 < len(reformatWord(word)) < 8:
                    i += 1
                    answer = word
                    temp[a] = "_"*(len(temp[a])*3//2)
            new = ""
            for t in temp:
                new += t + " "
            new = new.strip()
            print(new)
            return new, answer
                
        except:
            #return makeBrokenSentence(pseudoRandomSentenceGenerator(dispSentence), n)
            return makeBrokenSentence(s, n)
    except:
        return makeBrokenSentence(pseudoRandomSentenceGenerator(dispSentence), n)

#makeBrokenSentence(pseudoRandomSentenceGenerator(dispSentence), 1)

############################################
#AUTOCOMPLETE
############################################

def prevGuessHelper(prev, n):
    L = []
    if prev not in probDist:
        l = list(probDist.keys())
        return [random.choice(l)]
    new = probDist[prev]
    temp = Counter(new)
    temp = temp.most_common(n)
    for (choice, prob) in temp:
        if choice != '' and choice not in string.punctuation:
            L.append(choice)
    return L 

def postGuessHelper(prev, post):
    temp = prevGuessHelper(prev, 100)
    new = []
    for guess in temp:
        part = prevGuessHelper(guess, 20)
        #print(part)
        if post in part:
            new.append(guess)
    if len(new) < 2:
        l = list(probDist.keys())
        new.append(random.choice(l))
    return new


def guessPhrase(preWord, postWord, n):
    new, temp = [], []
    pre, post = prevGuessHelper(preWord, 10) , postGuessHelper(preWord, postWord)
    if len(pre) >= len(post):
        for x in pre:
            if x in post:
                new.append(x)
            else:
                temp.append(x)
    else:
        for x in post:
            if x in pre:
                new.append(x)
            else:
                temp.append(x)
    while len(new) <= n:
        l = random.choice(list(probDist.keys()))
        t = random.choice(l)
        new.append(t)
    return new

def autocomplete(s, n):
    new = ""
    temp = s.split()
    for i in range(0, len(temp)):
        if "_" in temp[i]:
            change = guessPhrase(temp[i-1],temp[i+1], n)
    return change 

#autocomplete(makeBrokenSentence(pseudoRandomSentenceGenerator(dispSentence), 1),n)

#Normal mode function variants
def optionAutocomplete(s, n):
    new = ""
    temp = s.split()
    for i in range(0, len(temp)):
        if "_" in temp[i]:
            change = guessPhrase(temp[i-1],temp[i+1], n)
    temp = set(change)
    L = []
    for x in temp:
        if len(x) > 2:
            L.append(x)
    while len(L) < 3:
        l = list(probDist.keys())
        L.append(random.choice(l))
    return L 

#HARDMODE function variants

def autocomplete(s, n):
    new = ""
    temp = s.split()
    for i in range(0, len(temp)):
        if "_" in temp[i]:
            change = guessPhrase(temp[i-1],temp[i+1], n)
    temp = set(change)
    L = []
    for x in temp:
        if len(x) > 2:
            L.append(x)
    while len(L) < 6:
        l = list(probDist.keys())
        L.append(random.choice(l))
    return L 

####################################################################
#           TP3 UPDATED AUTOCOMPLETE SYSTEM
####################################################################

def reformatWord(word):
    t = string.punctuation  + "‘"  +"“" + "”"
    new = ''
    for letter in word:
        if letter not in t:
            new += letter
    if "’" in new and new.index("’") != 0:
        new = new.replace("’", " ")
    new = new.strip()
    if new.isalpha() == False:
        l = list(probDist.keys())
        while (new.isalpha() == False):
            new = random.choice(l)
    return new.lower()

def fetchPreGuesses(pre):
    #uses probDist
    if pre in probDist:
        temp = probDist[pre]
        return temp
    else:
        print(pre, len(pre), "pre is randomized")
        l = list(probDist.keys())
        temp = probDist[random.choice(l)]
        return temp

def fetchPostGuess(post):
    #uses revProbDist
    if post in revProbDist:
        temp = revProbDist[post]
        return temp
    else:
        print(post, len(post),"post is randomized")
        l = list(revProbDist.keys())
        temp = revProbDist[random.choice(l)]
        return temp

def filterGuesses(preGuesses, postGuesses, n):
    d = {}
    for x in preGuesses:
        if len(x) == 1:
            d[x] = preGuesses[x]
    for y in postGuesses:
        if y in d and len(y) == 1:
            d[y] += postGuesses[y]
        else:
            d[y] = postGuesses[y]
    temp = Counter(d)
    new = temp.most_common(n)
    return new 


def combineDictionaries(d1, d2):
    for key in d1:
        d2[key] = d1[key]
    return d2

#normal mode - generate upto x options 
def ezAutocomplete(s):
    L = []
    temp = s.split(' ')
    for i in range(len(temp)):
        target = temp[i]
        if "_" in target:
            pre = temp[i-1]
            post = temp[i+1]
            print("pre and post <before formatting>:   ", pre, post)
            pre = reformatWord(pre)
            post = reformatWord(post)
            preGuesses = fetchPreGuesses(pre)
            postGuesses = fetchPostGuess(post)
            break
    L = filterGuesses(preGuesses, postGuesses, 20) #returns list of tuples
    new = []
    for (word, p) in L:
        if len(word) > 3:
            new.append(word)
    return new

# TESTING accuracy

def testAccuracy(n):
    a = 0
    for i in range(n):
        try:
            rsen, target = makeBrokenSentence(pseudoRandomSentenceGenerator(dispSentence), 1)
            target = reformatWord(target)
            guesses = ezAutocomplete(rsen)
            print(target, guesses)
            if target.lower() in guesses:
                a+=1 
        except:
            rsen, target = makeBrokenSentence(pseudoRandomSentenceGenerator(dispSentence), 1)
            target = reformatWord(target)
            guesses = ezAutocomplete(rsen)
            print(target, guesses)
            if target.lower() in guesses:
                a+=1
    print(a/n)
#testAccuracy(100)

#note: RUN GRPAHICS.PY TO TEST PROGRAM, NOT THIS FILE.