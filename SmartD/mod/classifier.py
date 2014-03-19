# 1.3M words 10k news documents
# 90 topics, categories overlap with each other
# one article could fit more topics
#from nltk.corpus import reuters as cop
# huge corpus, 1.15M words, tagged and categorized
from nltk.corpus import brown as cop
import nltk
import random
# the switch of DEBUGGING
DEBUG = False


# the frequency of all appeared words
# also corpus dependent
all_words = nltk.FreqDist(w.lower() for w in cop.words())
# most frequent 2000 words, or hand tuning toward different corpus
word_feature = all_words.keys()[200:500]

def documents_fetures(document):
    '''
    The basic idea is the frequency of the words
    determines the category of the document

    This function extract existence of the words in a document
    and returned as a dictionary
    '''
    # make sure the words in passed-in documents are not sequenced
    random.shuffle(document)
    # checking words in set is much faster than in list
    document_words = set(document)
    feature = {}
    for word in word_feature:
        feature[word] = (word in document_words)
        
    return feature

    
# the list of tuples constructed by containing words and the category
documents = [(list(cop.words(fileid)), category) for category in cop.categories() for fileid in cop.fileids(category)]

# ================ For debugging use =================
# ++++ used for listing the categories of the corpus ++++++
if DEBUG:
    value = ''
    for (d,c) in documents:
        former_value = c
        if former_value is not value:
            print c
        value = c
# =====================================================
    
# a dictionary that maps from “feature names” to “feature values”
featureset = [(documents_fetures(d), c) for (d,c) in documents]
# make the training data and testing data
train_data, test_data = featureset[100:], featureset[:100]

classifier = nltk.NaiveBayesClassifier.train(train_data)

print nltk.classify.accuracy(classifier, test_data)
print classifier.show_most_informative_features(5)

