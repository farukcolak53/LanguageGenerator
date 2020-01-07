import os
from sklearn.feature_extraction.text import TfidfVectorizer

from os.path import join
from typing import List

from jpype import (JClass, JString, getDefaultJVMPath, java, startJVM)


def generateNoun(noun):  # For generating nouns

    # ***********************This part is from Zemberek***********************
    number: List[JString] = [JString('A3sg'), JString('A3pl')]
    possessives: List[JString] = [
        JString('P1sg'), JString('P2sg'), JString('P3sg')
    ]
    cases: List[JString] = [JString('Dat'), JString('Loc'), JString('Abl')]

    morphology: TurkishMorphology = (
        TurkishMorphology.builder().setLexicon(noun).disableCache().build()
    )
    # ***********************This part is from Zemberek***********************
    item = morphology.getLexicon().getMatchingItems(noun).get(0)

    for number_m in number:
        for possessive_m in possessives:
            for case_m in cases:
                for result in morphology.getWordGenerator().generate(
                        item, number_m, possessive_m, case_m
                ):
                    # After we generate new noun from source we look if this noun obeys the rule
                    controller(str(result.surface), recurrence=False)
                    # We call controller with recurrence = False because if we call it without giving this parameter
                    # Program will enter a recurrence relation that never ends.
    return


def generateVerb(verb):
    # ***********************This part is from Zemberek***********************
    positive_negatives: List[JString] = [JString(''), JString('Neg')]
    times: List[JString] = [
        'Imp', 'Aor', 'Past', 'Prog1', 'Prog2', 'Narr', 'Fut'
    ]
    people: List[JString] = [
        'A1sg', 'A2sg', 'A3sg', 'A1pl', 'A2pl', 'A3pl'
    ]

    verb = verbRootGenerator(verb)  # This function generates '-mek, -mak' type of the given verb

    morphology: TurkishMorphology = (
        TurkishMorphology.builder().setLexicon(verb).disableCache().build()
    )

    # ***********************This part is from Zemberek***********************

    stem = verbStemGenerator(verb)  # This function generates without '-mek, -mak' type of the given verb

    # ***********************This part is from Zemberek ***********************
    for pos_neg in positive_negatives:
        for time in times:
            for person in people:
                seq: java.util.ArrayList = java.util.ArrayList()
                if pos_neg:
                    seq.add(JString(pos_neg))
                if time:
                    seq.add(JString(time))
                if person:
                    seq.add(JString(person))
                results = list(morphology.getWordGenerator().generate(
                    JString(stem),
                    seq
                ))
                if not results:
                    continue
                # ***********************This part is from Zembere***********************
                for result in results:
                    # After we generate new verb from source we look if this verb obeys the rule
                    controller(str(result.surface), recurrence=False)
                    # We call controller with recurrence = False because if we call it without giving this parameter
                    # Program will enter a recurrence relation that never ends.
    return


def controller(word, recurrence=True):  # This function checks if the given input obeys the given input
    global wordCounter
    if wordCounter == numOfWords:
        exit(1)
    total = 0
    values = []
    cont = True
    for letter in word:
        if letter not in letterValue:
            cont = False
            continue
        values.append(letterValue[letter])
        total = total + letterValue[letter]
    if not cont:
        return
    if total == wordSum:
        wordCounter += 1
        if not recurrence:
            print(wordCounter, ": ", word, values, total, "(Generated word!)")
        else:
            print(wordCounter, ": ", word, values, total)

    elif total < wordSum and recurrence:  # If given input's value is less then wanted value and
        # this is not an recursive call
        # we generate new words from it
        analysis: java.util.ArrayList = (
            morphologyController.analyzeAndDisambiguate(word).bestAnalysis()
        )
        # We can only generate new nouns and verbs
        for i, analysis in enumerate(analysis, start=1):
            if str(analysis.getPos()) == 'Noun':
                generateNoun(word)
            elif str(analysis.getPos()) == 'Verb':
                generateVerb(word)
            break
    return


def verbRootGenerator(verb):  # For finding root of the verb with '-mek, -mak' at the end
    WordAnalysis: JClass = JClass('zemberek.morphology.analysis.WordAnalysis')

    results: WordAnalysis = morphologyVerbRoot.analyze(JString(verb))

    for result in results:
        ret = (str(result.formatLong())).split(':')[0][1:]

    return ret


def verbStemGenerator(verb):  # For finding root of the verb without '-mek, -mak'
    WordAnalysis: JClass = JClass('zemberek.morphology.analysis.WordAnalysis')

    results: WordAnalysis = morphologyVerbStem.analyze(JString(verb))

    for result in results:
        ret = result.getStems()[0]

    return ret


path = "1150haber"
wordLimit = 100000
wordCounter = 0

letterValue = {'a': 1, 'b': 2, 'c': 3, 'ç': 4, 'd': 5, 'e': 6, 'f': 7, 'g': 8, 'ğ': 9, 'h': 10, 'ı': 11,
               'i': 12, 'j': 13, 'k': 14, 'l': 15, 'm': 16, 'n': 17, 'o': 18, 'ö': 19, 'p': 20, 'r': 21,
               's': 22, 'ş': 23, 't': 24, 'u': 25, 'ü': 26, 'v': 27, 'y': 28, 'z': 29}

fileNames = [subdir + os.path.sep + file for subdir, dirs, files in os.walk(path) for file in files]

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
morphologyController: TurkishMorphology = TurkishMorphology.createWithDefaults()
morphologyVerbRoot: TurkishMorphology = TurkishMorphology.createWithDefaults()
morphologyVerbStem: TurkishMorphology = TurkishMorphology.createWithDefaults()

print("-----------------------------------")

numOfWords = int(input("Enter the number of words: "))
wordSum = int(input("Enter the value of the word: "))

for word in wordList:
    controller(word)
