import os
import sys
import pandas as pd
import numpy as np
import sklearn
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

path = "/Users/evrim/PycharmProjects/cse3063f19p2_esahin_fcolak_fkuse_msenol/1150haber"
fileNames = []
wordList = []
wordLimit = 100000
wordSum = 17
letterValue = {'a': 1, 'b': 2, 'c': 3, 'ç': 4, 'd': 5, 'e': 6, 'f': 7, 'g': 8, 'ğ': 9, 'h': 10, 'ı': 11,
               'i': 12, 'j': 13, 'k': 14, 'l': 15, 'm': 16, 'n': 17, 'o': 18, 'ö': 19, 'p': 20, 'r': 21,
               's': 22, 'ş': 23, 't': 24, 'u': 25, 'ü': 26, 'v': 27, 'y': 28, 'z': 29}

fileNames = [subdir + os.path.sep + file for subdir, dirs, files in os.walk(path) for file in files]
# fileNames = [fileName.replace('\\','/') for fileName in fileNames ] # you may add this line for windows os

tfidfVectorizer = TfidfVectorizer(decode_error='ignore')
docTermMatrix = tfidfVectorizer.fit_transform((open(f, encoding="utf8").read() for f in fileNames))

wordList = [word[0] for i, word in zip(range(0, wordLimit), tfidfVectorizer.vocabulary_.items())]

for word in wordList:
    total = 0
    values = []
    cont = True
    for letter in word:
        if letter not in letterValue:
            cont = False
            continue
        values.append(letterValue[letter])
        total = total + letterValue[letter]
    if cont == False:
        continue
    if total == wordSum:
        print(word, values, total)
