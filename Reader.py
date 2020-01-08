import os

from sklearn.feature_extraction.text import TfidfVectorizer
from Zemberek import Zemberek
from jpype import java


class Reader:

    letterValue = {'a': 1, 'b': 2, 'c': 3, 'ç': 4, 'd': 5, 'e': 6, 'f': 7, 'g': 8, 'ğ': 9, 'h': 10, 'ı': 11,
                   'i': 12, 'j': 13, 'k': 14, 'l': 15, 'm': 16, 'n': 17, 'o': 18, 'ö': 19, 'p': 20, 'r': 21,
                   's': 22, 'ş': 23, 't': 24, 'u': 25, 'ü': 26, 'v': 27, 'y': 28, 'z': 29}

    # This function reads the given under the given path and documents, and then stores them in a list
    def readWords(self, path):
        wordLimit = 100000

        fileNames = [subdir + os.path.sep + file for subdir, dirs, files in os.walk(path) for file in files]
        tfidfVectorizer = TfidfVectorizer(decode_error='ignore')
        docTermMatrix = tfidfVectorizer.fit_transform((open(f, encoding="utf8").read() for f in fileNames))

        wordList = [word[0] for i, word in zip(range(0, wordLimit), tfidfVectorizer.vocabulary_.items())]

        return wordList

    # This function traverse the word list and stores them in appropriate dictionaries
    def storeWords(self, adj_dict, noun_dict, verb_dict, adj_key_counter, noun_key_counter, verb_key_counter, wordList):
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
                if letter not in self.letterValue:
                    cont = False
                    continue
                values.append(self.letterValue[letter])
                total = total + self.letterValue[letter]

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

        return adj_dict, noun_dict, verb_dict, adj_key_counter, noun_key_counter, verb_key_counter
