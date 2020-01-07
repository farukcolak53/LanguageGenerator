import os
import sklearn

from os.path import join
from typing import List

from jpype import JClass, getDefaultJVMPath, java, shutdownJVM, startJVM
from sklearn.feature_extraction.text import TfidfVectorizer

if __name__ == '__main__':

    ZEMBEREK_PATH: str = join('bin', 'zemberek-full.jar')

    startJVM(
        getDefaultJVMPath(),
        '-ea',
        f'-Djava.class.path={ZEMBEREK_PATH}',
        convertStrings=False
    )

    TurkishMorphology: JClass = JClass('zemberek.morphology.TurkishMorphology')

    morphology: TurkishMorphology = TurkishMorphology.createWithDefaults()

    # my part #

    path = "1150haber"
    fileNames = []
    wordList = []

    adj_dict = {}
    noun_dict = {}
    verb_dict = {}
    adv_dict = {}
    num_dict = {}
    conj_dict = {}
    deter_dict = {}
    post_p_dict = {}

    adj_key_counter = 1
    noun_key_counter = 1
    verb_key_counter = 1
    adv_key_counter = 1
    num_key_counter = 1
    conj_key_counter = 1
    deter_key_counter = 1
    post_p_key_counter = 1

    wordLimit = 100000

    fileNames = [subdir + os.path.sep + file for subdir, dirs, files in os.walk(path) for file in files]
    tfidfVectorizer = TfidfVectorizer(decode_error='ignore')
    docTermMatrix = tfidfVectorizer.fit_transform((open(f, encoding="utf8").read() for f in fileNames))

    wordList = [word[0] for i, word in zip(range(0, wordLimit), tfidfVectorizer.vocabulary_.items())]

    for word in wordList:
        sentence: str = word

        analysis: java.util.ArrayList = (
            morphology.analyzeAndDisambiguate(sentence).bestAnalysis()
        )

        pos: List[str] = []

        for i, analysis in enumerate(analysis, start=1):
            
            print(
                f'\nAnalysis {i}: {analysis}',
                f'\nPrimary POS {i}: {analysis.getPos()}'
                f'\nPrimary POS (Short Form) {i}: {analysis.getPos().shortForm}'
            )

            if str(analysis.getPos()) == 'Adjective':
                adj_dict[adj_key_counter] = word
                adj_key_counter = adj_key_counter + 1
            elif str(analysis.getPos()) == "Noun":
                noun_dict[noun_key_counter] = word
                noun_key_counter = noun_key_counter + 1
            elif str(analysis.getPos()) == "Verb":
                verb_dict[verb_key_counter] = word
                verb_key_counter = verb_key_counter + 1
            elif str(analysis.getPos()) == "Adverb":
                adv_dict[adv_key_counter] = word
                adv_key_counter = adv_key_counter + 1
            elif str(analysis.getPos()) == "Numeral":
                num_dict[num_key_counter] = word
                num_key_counter = num_key_counter + 1
            elif str(analysis.getPos()) == "Conjunction":
                conj_dict[conj_key_counter] = word
                conj_key_counter = conj_key_counter + 1
            elif str(analysis.getPos()) == "Determiner":
                deter_dict[deter_key_counter] = word
                deter_key_counter = deter_key_counter + 1
            elif str(analysis.getPos()) == "PostPositive":
                post_p_dict[post_p_key_counter] = word
                post_p_key_counter = post_p_key_counter + 1

            pos.append(
                f'{str(analysis.getLemmas()[0])}'
                f'-{analysis.getPos().shortForm}'
            )

        # print(f'\nFull sentence with POS tags: {" ".join(pos)}')

    shutdownJVM()
