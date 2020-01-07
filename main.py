import os
from sklearn.feature_extraction.text import TfidfVectorizer

from os.path import join
from typing import List

from jpype import (JClass, JString, getDefaultJVMPath, java, shutdownJVM,
                   startJVM)

def generateNoun(noun):
    number: List[JString] = [JString('A3sg'), JString('A3pl')]
    possessives: List[JString] = [
        JString('P1sg'), JString('P2sg'), JString('P3sg')
    ]
    cases: List[JString] = [JString('Dat'), JString('Loc'), JString('Abl')]

    morphology: TurkishMorphology = (
        TurkishMorphology.builder().setLexicon(noun).disableCache().build()
    )

    item = morphology.getLexicon().getMatchingItems(noun).get(0)

    for number_m in number:
        for possessive_m in possessives:
            for case_m in cases:
                for result in morphology.getWordGenerator().generate(
                        item, number_m, possessive_m, case_m
                ):
                   # print(str(result.surface))
                    controller(str(result.surface))
    return

def controller (word) :
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
        return
    if total == wordSum:
        print(word, values, total)
    elif total < wordSum:


        analysis: java.util.ArrayList = (
            morphology.analyzeAndDisambiguate(word).bestAnalysis()
        )
        for i, analysis in enumerate(analysis, start=1):
            if str(analysis.getPos()) == 'Noun':
                generateNoun(word)
            break
    return

path = "1150haber"
fileNames = []
wordList = []
wordLimit = 100000
wordSum = 100
letterValue = {'a': 1, 'b': 2, 'c': 3, 'ç': 4, 'd': 5, 'e': 6, 'f': 7, 'g': 8, 'ğ': 9, 'h': 10, 'ı': 11,
               'i': 12, 'j': 13, 'k': 14, 'l': 15, 'm': 16, 'n': 17, 'o': 18, 'ö': 19, 'p': 20, 'r': 21,
               's': 22, 'ş': 23, 't': 24, 'u': 25, 'ü': 26, 'v': 27, 'y': 28, 'z': 29}

fileNames = [subdir + os.path.sep + file for subdir, dirs, files in os.walk(path) for file in files]
# fileNames = [fileName.replace('\\','/') for fileName in fileNames ] # you may add this line for windows os

tfidfVectorizer = TfidfVectorizer(decode_error='ignore')
docTermMatrix = tfidfVectorizer.fit_transform((open(f, encoding="utf8").read() for f in fileNames))

wordList = [word[0] for i, word in zip(range(0, wordLimit), tfidfVectorizer.vocabulary_.items())]


ZEMBEREK_PATH: str = join('zemberek-full.jar')

startJVM(
    getDefaultJVMPath(),
    '-ea',
    f'-Djava.class.path={ZEMBEREK_PATH}',
    convertStrings=False
)
TurkishMorphology: JClass = JClass('zemberek.morphology.TurkishMorphology')
morphology: TurkishMorphology = TurkishMorphology.createWithDefaults()

for word in wordList:
   controller(word)
#generateVerb("ağlayan")
print('-----finished-----')
