#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 15:06:34 2022

@author: bogdanolena
"""
import os, os.path
path = os.path.expanduser('~/nltk_data')
import nltk.data
path in nltk.data.path


"""
Method 1 to uncover ngrams conssits in relying on the existing corpora / new corpora
"""

from nltk.corpus.reader.api import *
from nltk.corpus.reader.util import *
from nltk.tokenize import *

class PlaintextCorpusReader(CorpusReader):
    """
    Reader for corpora that consist of plaintext documents.  Paragraphs
    are assumed to be split using blank lines.  Sentences and words can
    be tokenized using the default tokenizers, or by custom tokenizers
    specified as parameters to the constructor.

    This corpus reader can be customized (e.g., to skip preface
    sections of specific document formats) by creating a subclass and
    overriding the ``CorpusView`` class variable.
    """

    CorpusView = StreamBackedCorpusView
    """The corpus view class used by this reader.  Subclasses of
       ``PlaintextCorpusReader`` may specify alternative corpus view
       classes (e.g., to skip the preface sections of documents.)"""

    def __init__(
        self,
        root,
        fileids,
        word_tokenizer=WordPunctTokenizer(),
        sent_tokenizer=nltk.data.LazyLoader("tokenizers/punkt/english.pickle"),
        para_block_reader=read_blankline_block,
        encoding="utf8",
    ):
        r"""
        Construct a new plaintext corpus reader for a set of documents
        located at the given root directory.  Example usage:

            >>> root = '/usr/local/share/nltk_data/corpora/webtext/'
            >>> reader = PlaintextCorpusReader(root, '.*\.txt') # doctest: +SKIP

        :param root: The root directory for this corpus.
        :param fileids: A list or regexp specifying the fileids in this corpus.
        :param word_tokenizer: Tokenizer for breaking sentences or
            paragraphs into words.
        :param sent_tokenizer: Tokenizer for breaking paragraphs
            into words.
        :param para_block_reader: The block reader used to divide the
            corpus into paragraph blocks.
        """
        CorpusReader.__init__(self, root, fileids, encoding)
        self._word_tokenizer = word_tokenizer
        self._sent_tokenizer = sent_tokenizer
        self._para_block_reader = para_block_reader


    def words(self, fileids=None):
        """
        :return: the given file(s) as a list of words
            and punctuation symbols.
        :rtype: list(str)
        """
        return concat(
            [
                self.CorpusView(path, self._read_word_block, encoding=enc)
                for (path, enc, fileid) in self.abspaths(fileids, True, True)
            ]
        )


    def sents(self, fileids=None):
        """
        :return: the given file(s) as a list of
            sentences or utterances, each encoded as a list of word
            strings.
        :rtype: list(list(str))
        """
        if self._sent_tokenizer is None:
            raise ValueError("No sentence tokenizer for this corpus")

        return concat(
            [
                self.CorpusView(path, self._read_sent_block, encoding=enc)
                for (path, enc, fileid) in self.abspaths(fileids, True, True)
            ]
        )


    def paras(self, fileids=None):
        """
        :return: the given file(s) as a list of
            paragraphs, each encoded as a list of sentences, which are
            in turn encoded as lists of word strings.
        :rtype: list(list(list(str)))
        """
        if self._sent_tokenizer is None:
            raise ValueError("No sentence tokenizer for this corpus")

        return concat(
            [
                self.CorpusView(path, self._read_para_block, encoding=enc)
                for (path, enc, fileid) in self.abspaths(fileids, True, True)
            ]
        )


    def _read_word_block(self, stream):
        words = []
        for i in range(20):  # Read 20 lines at a time.
            words.extend(self._word_tokenizer.tokenize(stream.readline()))
        return words

    def _read_sent_block(self, stream):
        sents = []
        for para in self._para_block_reader(stream):
            sents.extend(
                [
                    self._word_tokenizer.tokenize(sent)
                    for sent in self._sent_tokenizer.tokenize(para)
                ]
            )
        return sents

    def _read_para_block(self, stream):
        paras = []
        for para in self._para_block_reader(stream):
            paras.append(
                [
                    self._word_tokenizer.tokenize(sent)
                    for sent in self._sent_tokenizer.tokenize(para)
                ]
            )
        return paras
    
    
"""
Testing possible corpora : I keep Ofxord corpus for the final analysis


#Oxford corpus 

nltk.data.load('corpora/oxford/oxford.txt', format='raw')

corpus_root = os.path.expanduser('~/nltk_data/corpora/oxford')
corpus = PlaintextCorpusReader(corpus_root, '.*', encoding='latin1')
corpus.words()



#BRRD corpus 

    
nltk.data.load('corpora/BRRD/BRRD.txt', format='raw')

corpus_root = os.path.expanduser('~/nltk_data/corpora/BRRD')
corpus = PlaintextCorpusReader(corpus_root, '.*', encoding='latin1')
corpus.words()

#Financial reports 2002 corpus 
    
nltk.data.load('corpora/report_2/6_2002_1.txt', format='raw')

corpus_root = os.path.expanduser('~/nltk_data/corpora/report_2')
corpus = PlaintextCorpusReader(corpus_root, '.*', encoding='latin1')
corpus.words()

"""

#Upload Oxford corpus 

nltk.data.load('corpora/oxford/oxford.txt', format='raw')

corpus_root = os.path.expanduser('~/nltk_data/corpora/oxford')
corpus = PlaintextCorpusReader(corpus_root, '.*', encoding='latin1')
corpus.words()

#['THE', 'OXFORD', 'HANDBOOK', 'OF', 'FINANCIAL', ...]

from gensim.models.phrases import Phraser, Phrases
all_words=[corpus.words(x) for x in corpus.fileids()]

words=[]
for k in range(0, len(all_words[0])):
    words.append(all_words[0][k].upper())

#Uncovering all possible n-grams present in this corpus
from nltk import ngrams

bigram=list(ngrams(words,2))
trigram=list(ngrams(words,3))
fourgram=list(ngrams(words,4))
fivegram=list(ngrams(words,5))

for k in range(0, len(bigram)):
    bigram[k]=list(bigram[k])
    bigram[k]=' '.join(bigram[k])


for k in range(0, len(trigram)):
    trigram[k]=list(trigram[k])
    trigram[k]=' '.join(trigram[k])
    
for k in range(0, len(fourgram)):
    fourgram[k]=list(fourgram[k])
    fourgram[k]=' '.join(fourgram[k])
    
for k in range(0, len(fivegram)):
    fivegram[k]=list(fivegram[k])
    fivegram[k]=' '.join(fivegram[k])
    
bigToClassify=[]
trigToClassify=[]
fourgToClassify=[]
fivegToClassify=[]

#Determining possible bigrams that were not classified 

for k in range(0, len(NotClassified5)-1):
    if NotClassified5[k] + ' ' + NotClassified5[k+1] in bigram:
        big=NotClassified5[k] + ' ' + NotClassified5[k+1]
        bigToClassify.append(big)
        k+=2
    else:
        k+=1


#Keeping only unique bigrams 

bigr = []
for i in bigToClassify:
    if i not in bigr:
        bigr.append(i)

#len(bigr)=5190
    
        
#To determine possible trigrams that were not classified 
for k in range(0, len(NotClassified5)-2):
    if NotClassified5[k] + ' ' + NotClassified5[k+1] + ' ' + NotClassified5[k+2] in trigram:
        trig=NotClassified5[k] + ' ' + NotClassified5[k+1] + ' ' + NotClassified5[k+2]
        trigToClassify.append(trig)
        k+=3
    else: 
        k+=1

#To detect duplicates 

trig = []
for i in trigToClassify:
    if i not in trig:
        trig.append(i)

#len(trig)=1873

#To determine possible fourgrams that were not classified 
for k in range(0, len(NotClassified5)-3):
    if NotClassified5[k] + ' ' + NotClassified5[k+1] + ' ' + NotClassified5[k+2] + ' ' + NotClassified5[k+3] in fourgram:
        four=NotClassified5[k] + ' ' + NotClassified5[k+1] + ' ' + NotClassified5[k+2] + ' ' + NotClassified5[k+3]
        fourgToClassify.append(four)
        k+=4
    else: 
        k+=1

#To detect duplicates 

four = []
for i in fourgToClassify:
    if i not in four:
        four.append(i)

#len(four)=252


#To determine possible fivegrams that were not classified 
for k in range(0, len(NotClassified5)-4):
    if NotClassified5[k] + ' ' + NotClassified5[k+1] + ' ' + NotClassified5[k+2] + ' ' + NotClassified5[k+3] + ' ' + NotClassified5[k+4] in fivegram:
        five=NotClassified5[k] + ' ' + NotClassified5[k+1] + ' ' + NotClassified5[k+2] + ' ' + NotClassified5[k+3] + ' ' + NotClassified5[k+4] 
        fivegToClassify.append(five)
        k+=5
    else: 
        k+=1

#To detect duplicates 

five = []
for i in fivegToClassify:
    if i not in five:
        five.append(i)

#len(five)=21


"""
Method 2 to uncover ngrams conssits in looking for expressions that come ofter together in the text
"""



complete=" "
for i in range(0, len(dataset)):
    complete= complete + " " + dataset["text"].iloc[i]

from collections import Counter
from nltk.util import ngrams 


#Looking for 2-grams

classifier_complete = pd.read_csv('keys.csv',  sep=';',  header=0, encoding = 'latin1')

wordsToExclude=[]
for i in range(0, len(classifier_complete)): 
    if classifier_complete['category'][i] == 'LogicalConnectors':
        word= classifier_complete['key'][i].lower()
        wordsToExclude.append(word) 
    if classifier_complete['category'][i] == 'FunctionWords':
        word= classifier_complete['key'][i].lower()
        wordsToExclude.append(word) 
        
        
bigramAnalys=" "
for i in complete.split():
    if i not in wordsToExclude: 
        bigramAnalys=bigramAnalys + " " + i
        
        

n_gram = 2
bigrams=list(ngrams(bigramAnalys.split(), n_gram))
freq = nltk.FreqDist(bigrams)
result = sorted(bigrams, key = bigrams.count,
                                reverse = True)

bigramsM2=[]   
for bigram in list(freq.keys()):
    if result.count(bigram) > 10:
        big= bigram[0] + ' ' + bigram[1]
        bigramsM2.append(big)

for i in range(0, len(bigramsM2)):
    mystring= ' '
    for x in bigramsM2[i]:
        if type(x) != float:
            mystring += x.upper()
    bigramsM2[i]=mystring
    bigramsM2[i]=bigramsM2[i].strip()
    
#len(bigramsM2)=2947 

bigramList=[]
for i in range(0, len(bigramsM2)):
    if bigramsM2[i] not in listOfClassComplete:
        bigramList.append(bigramsM2[i])
        
#len(bigramList)=2860



#Saving in excel file 

bigramList=pd.Series(bigramList)
bigramList.to_excel('bigramsM2Final.xlsx')
bigramList.to_csv('bigramsM2Final.csv')

#Looking for 3-grams

wordsOff_3=["is", "are", "at", "any", "out", "from", "where", "can", "all", 
           "from", "an", "so", "but", "more", "no", "without",  
          "with", "over", "and", "by", "soon",  "on", "as", "was", "were", 
          "will", "which", "who", "whose", "this", "these", "those", "it", "a", "the", 
          "not", "for", "be", "when", "or", "se", "also", "has", "have", 
          "very", "only", "than", "would", "ii", "i", "iii", "iv", "v", "from","less", 
          "below", "above","some", "over", "all", "with", "may", "once", "yet", "does", 
          "its", "a", "b", "c","d", "e", "f","example", "such", "should", "had", "been", 
          "be", "however", "if", "between", "same", "and/or", "must", "among"]

trigrAnalys=" "
for i in complete.split():
    if i not in wordsOff_3: 
        trigrAnalys=trigrAnalys + " " + i
        

        
n_gram = 3
threegrams=list(ngrams(trigrAnalys.split(), n_gram))
freq = nltk.FreqDist(threegrams)
result = sorted(threegrams, key = threegrams.count,
                                reverse = True)

ThreegrM2=[]   
for threegram in list(freq.keys()):
    if result.count(threegram) > 10:
        three= threegram[0] + ' ' + threegram[1] + ' ' + threegram[2]
        ThreegrM2.append(three)

for i in range(0, len(ThreegrM2)):
    mystring= ' '
    for x in ThreegrM2[i]:
        if type(x) != float:
            mystring += x.upper()
    ThreegrM2[i]=mystring
    ThreegrM2[i]=ThreegrM2[i].strip()
    
#len(ThreegrM2)=1454
threegrList=[]
for i in range(0, len(ThreegrM2)):
    if ThreegrM2[i] not in listOfClassComplete:
        threegrList.append(ThreegrM2[i])
#len(threegrList)=1445
        

#Saving in excel file 

threegrList=pd.Series(threegrList)
threegrList.to_excel('threegrM2.xlsx')
threegrList.to_csv('threegrM2Final.csv')

#Looking for 4-grams

wordsOff_4=["is", "are", "any", "from", "where", "can", "all", 
            "an", "so", "but", "more",  "without",  
          "with", "over", "by", "soon",   "as", "was", "were", 
          "will", "which", "who", "whose", "this", "these", "those", "it", "a", 
          "not",  "be", "when", "or", "se", "also", "has", "have", 
          "very", "only", "than", "would", "ii", "i", "iii", "iv", "v", "from","less", 
          "below", "above","some", "over", "all", "with", "may", "once", "yet", "does", 
          "its", "a", "b", "c","d", "e", "f","example", "such", "should", "had", "been", 
           "however", "if", "between", "same", "and/or", "must", "among"]


fourAnalys=" "
for i in complete.split():
    if i not in wordsOff_4: 
        fourAnalys=fourAnalys + " " + i
    
n_gram = 4
fourgrams=list(ngrams(fourAnalys.split(), n_gram))
freq = nltk.FreqDist(fourgrams)
result = sorted(fourgrams, key = fourgrams.count,
                                reverse = True)

FourgrM2=[]   
for fourams in list(freq.keys()):
    if result.count(fourams) > 5:
        four= fourams[0] + ' ' + fourams[1] + ' ' + fourams[2] + ' ' + fourams[3]
        FourgrM2.append(four)

for i in range(0, len(FourgrM2)):
    mystring= ' '
    for x in FourgrM2[i]:
        if type(x) != float:
            mystring += x.upper()
    FourgrM2[i]=mystring
    FourgrM2[i]=FourgrM2[i].strip()
    
#len(FourgrM2)=229
fourgrList=[]
for i in range(0, len(FourgrM2)):
    if FourgrM2[i] not in listOfClassComplete:
        fourgrList.append(FourgrM2[i])
#len(fourgrList)=228

#Saving in excel file 

fourgrList=pd.Series(fourgrList)
fourgrList.to_excel('fourgrM2.xlsx')

#Looking for 5-grams

fiveAnalys=" "
for i in complete.split():
    fiveAnalys=fiveAnalys + " " + i
    
n_gram = 5
fivegrams=list(ngrams(fiveAnalys.split(), n_gram))
freq = nltk.FreqDist(fivegrams)
result = sorted(fivegrams, key = fivegrams.count,
                                reverse = True)

FivegrM2=[]   
for fivegr in list(freq.keys()):
    if result.count(fivegr) > 5:
        five= fivegr[0] + ' ' + fivegr[1] + ' ' + fivegr[2] + ' ' + fivegr[3] + ' ' + fivegr[4]
        FivegrM2.append(five)

for i in range(0, len(FivegrM2)):
    mystring= ' '
    for x in FivegrM2[i]:
        if type(x) != float:
            mystring += x.upper()
    FivegrM2[i]=mystring
    FivegrM2[i]=FivegrM2[i].strip()
    
#len(FivegrM2)=104
fivegrList=[]
for i in range(0, len(FivegrM2)):
    if FivegrM2[i] not in listOfClassComplete:
        fivegrList.append(FivegrM2[i])
#len(fivegrList)=104
        


#Saving in excel file 

fivegrList=pd.Series(fivegrList)
fivegrList.to_excel('fivergrM2.xlsx')



