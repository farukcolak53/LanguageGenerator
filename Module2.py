from random import randint
from jpype import shutdownJVM
from Reader import Reader


class Module2:
    if __name__ == '__main__':

        reader = Reader()  # Reader object

        path = "1150haber"  # A corpus of documents

        # Dictionaries which will contain words
        adj_dict = {}
        noun_dict = {}
        verb_dict = {}

        # Key counters of the dictionaries
        adj_key_counter = 1
        noun_key_counter = 1
        verb_key_counter = 1

        # Reads the words inside the documents and stores them inside appropriate dictionaries
        adj_dict, noun_dict, verb_dict, adj_key_counter, noun_key_counter, verb_key_counter = reader.readWords(adj_dict, noun_dict, verb_dict, adj_key_counter, noun_key_counter, verb_key_counter, path)

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
