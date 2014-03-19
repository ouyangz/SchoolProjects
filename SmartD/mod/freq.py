import pickle
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
pos_map = {'VBP':'VERB','VB':'VERB','VBD':'VERB','VBG':'VERB','VBN':'VERB','VBZ':'VERB', 'NN':'NOUN', 'NNS':'NOUN','NNP':'NOUN','NNPS':'NOUN','JJ':'ADJ', 'JJR':'ADJ', 'JJS':'ADJ', 'RB':'ADV','RBR':'ADV','RBS':'ADV', 'DT':'DT', 'RP':'PP'}

def freq_prepare():
    freq = dict()
    prob = dict()
    total = 0.0

    for word, tag in brown.tagged_words(simplify_tags=True):
        word = normalize(word, tag)
        if not freq.has_key(word):
            freq[word] = 0.0
        freq[word] += 1
        total += 1

    for word, count in freq.items():
        prob[word] = count / total

    print prob['the']
    print prob['to']
    print prob['dictionary']

    outfile = open('word_frequency.dat', 'w')
    pickle.dump(prob, outfile)
    outfile.close()

def normalize(word, tag=None):
    word = word.lower()
    if pos_map.has_key(tag):
        tag = pos_map[tag]
    normalized = None
    if (tag == 'V' or tag == 'VERB'):
        normalized = wn.morphy(word, wn.VERB)
    elif (tag == 'N' or tag == 'NOUN'):
        normalized = wn.morphy(word, wn.NOUN)
    else:
        normalized = wn.morphy(word)
    if normalized != None:
#        print word, normalized
        return normalized
    else:
#        print word, word
        return word
    
def test_load(filename):
    infile = open(filename, 'r')
    prob = pickle.load(infile)

    for word, p in prob.items():
        if p > 0.001:
            print word
    
# freq_prepare()
# test_load('word_frequency.dat')
