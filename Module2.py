import os

from random import randint
from jpype import JClass, getDefaultJVMPath, java, shutdownJVM, startJVM
from sklearn.feature_extraction.text import TfidfVectorizer
from Zemberek import Zemberek


class Module2:
    if __name__ == '__main__':

        path = "1150haber"  # A corpus of documents

        # Dictionaries which will contain words
        adj_dict = {}
        noun_dict = {}
        verb_dict = {}

        # Key counters of the dictionaries
        adj_key_counter = 1
        noun_key_counter = 1
        verb_key_counter = 1

        wordLimit = 100000

        letterValue = {'a': 1, 'b': 2, 'c': 3, 'ç': 4, 'd': 5, 'e': 6, 'f': 7, 'g': 8, 'ğ': 9, 'h': 10, 'ı': 11,
                       'i': 12, 'j': 13, 'k': 14, 'l': 15, 'm': 16, 'n': 17, 'o': 18, 'ö': 19, 'p': 20, 'r': 21,
                       's': 22, 'ş': 23, 't': 24, 'u': 25, 'ü': 26, 'v': 27, 'y': 28, 'z': 29}

        fileNames = [subdir + os.path.sep + file for subdir, dirs, files in os.walk(path) for file in files]
        tfidfVectorizer = TfidfVectorizer(decode_error='ignore')
        docTermMatrix = tfidfVectorizer.fit_transform((open(f, encoding="utf8").read() for f in fileNames))

        wordList = [word[0] for i, word in zip(range(0, wordLimit), tfidfVectorizer.vocabulary_.items())]

        print("Storing the words inside the dictionaries...")

        # For every word in the wordList, analyses it morphologically and stores it in the appropriate dictionary
        # These dictionaries have two values, first one is word itself and the second one is the value of the word
        for word in wordList:
            sentence: str = word

            analysis: java.util.ArrayList = (
                Zemberek.morphology.analyzeAndDisambiguate(sentence).bestAnalysis()
            )

            # Computes the value of the word
            total = 0
            values = []
            cont = True
            for letter in word:
                if letter not in letterValue:
                    cont = False
                    continue
                values.append(letterValue[letter])
                total = total + letterValue[letter]

            for i, analysis in enumerate(analysis, start=1):

                if str(analysis.getPos()) == 'Adjective':
                    adj_dict[adj_key_counter] = [word, total]
                    adj_key_counter = adj_key_counter + 1
                elif str(analysis.getPos()) == "Noun":
                    noun_dict[noun_key_counter] = [word, total]
                    noun_key_counter = noun_key_counter + 1
                elif str(analysis.getPos()) == "Verb":
                    verb_dict[verb_key_counter] = [word, total]
                    verb_key_counter = verb_key_counter + 1

        sentenceCounter = 0  # Counts the number of generated sentences which has the requested value

        numOfSentences = int(input("Enter the number of the sentences: "))
        sentenceTotal = int(input("Enter the value of the sentences: "))
        print("---------------------------------------")

        #  'break' and random statements is added to vary the words in the sentences
        for noun in noun_dict:  # Traverses the noun_dict dictionary
            noun = randint(1, noun_key_counter)
            for adj in adj_dict:
                adj = randint(1, adj_key_counter)
                for verb in verb_dict:
                    if sentenceCounter < numOfSentences:  # Generates sentences until the given number of sentences is reached
                        sentence = str(noun_dict[noun][0]).capitalize() + " " + str(adj_dict[adj][0]) + " " + str(
                            verb_dict[verb][0])  # Concatenation
                        mySum = noun_dict[noun][1] + adj_dict[adj][1] + verb_dict[verb][
                            1]  # Computes the value of the sentence
                        if mySum == sentenceTotal:  # If the value of the current sentence is equal to the input value
                            print(sentenceCounter+1, ": ", sentence, " | ", mySum)
                            sentenceCounter += 1
                            break
                    elif sentenceCounter == numOfSentences:  # If the number of sentences is reached to the input value, exit
                        exit(1)
                    else:
                        print("No matches found!")
                break
        shutdownJVM()
