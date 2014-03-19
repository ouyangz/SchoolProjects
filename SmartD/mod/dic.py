"""
the initial code for smart dictionary
"""

import os
import sys
sys.path.append("..")
import nltk
import pickle
from nltk.corpus import wordnet as wn
from mod.chunk import *
from mod.freq import normalize

# mapping the tag to POS
pos_map = {'VBP':wn.VERB,'VB':wn.VERB,'VBD':wn.VERB,'VBG':wn.VERB,'VBN':wn.VERB,\
           'VBZ':wn.VERB, 'NN':wn.NOUN, 'NNS':wn.NOUN,'NNP':wn.NOUN,'NNPS':wn.NOUN,\
           'JJ':wn.ADJ, 'JJR':wn.ADJ, 'JJS':wn.ADJ, 'RB':wn.ADV,'RBR':wn.ADV,'RBS':wn.ADV}

word_freq_file = open('../mod/word_frequency.dat', 'r')
word_prob = pickle.load(word_freq_file)

# ************** for debugging use ****************
#sentence = 'I previously booked the nice flight.'
#sentence = 'I bought a book.'

#sentence = 'I turn on the bright light.'

#sentence = 'He puts the cloth on the desk.'
#sentence = 'He puts the cloth on near the desk.'

#sentence = 'Peter sold the farmer rice.'
#Sentence = 'The computer monitor is broken.'

#word = 'sold'
#word = 'booked'
#word = 'turn'
#word = 'farmer'
#word = 'put'      # --> 'put' or 'put_on'
#word = 'farmer'   # --> 'farmer'
#word = 'computer' # --> 'computer_monitor'
# *************************************************

# the returned value is the list containing tuple of word and all the accroding meaning
def Lookup (sentence, word):
    # tag every words in the original sentence
    tokens = nltk.word_tokenize(sentence)
    
    if word not in tokens:
        print ("invalid word")
        raise NameError
    
    tagged = nltk.pos_tag(tokens)
    print (tagged)

    # determine the pos of the word in the sentence
    word_tag = [item[1] for item in tagged if item[0] == word][0]

    # Chunk the input
    possible_chunk = chunktaged(tokens, tagged, word)

#    print possible_chunk
    
    # Rank
    if word_tag in pos_map:
        word_pos = pos_map[word_tag]
        synsets = wn.synsets(possible_chunk, pos = word_pos)
    else:
        synsets = wn.synsets(possible_chunk)
    synsets = Rank (tokens, tagged, possible_chunk, synsets)
    
    # Output
    word_expl = [(item.definition, item.lemma_names, item.examples) for item, rank in synsets]

    return (possible_chunk, word_expl)

def Rank (tokens, tagged, chunk, synsets):
    expanded_tokens = set()
    for i in range(len(tokens)):
        for synset in wn.synsets(normalize(tokens[i], tagged[i])):
            expanded_tokens.update(synset.lemma_names)
    chunk_tokens = chunk.split('_')
# ************** FOR debugging use ****************
#    print expanded_tokens
#    print tokens
#    print tagged
#    print chunk
#    print synsets
# *************************************************   
    rank = dict()
    for item in synsets:
        rank[item] = 0.0
        # Examples
        for example in item.examples:
            example_tokens = nltk.word_tokenize(example)
            example_tagged = nltk.pos_tag(example_tokens)
            for i in range(len(example_tokens)):
                example_tokens[i] = normalize(example_tokens[i], example_tagged[i])
            for example_word in example_tokens:
                if ((example_word in expanded_tokens) and (not (example_word in chunk_tokens)) and (word_prob.has_key(example_word))):
                    print (example_word)
                    rank[item] += 1.0 / word_prob [example_word]
        if item.examples != []:
            rank[item] /= len(item.examples)
            
        # Definition
        def_tokens = nltk.word_tokenize(item.definition)
        for i in range(len(def_tokens)):
            def_tokens[i] = normalize(def_tokens[i])
        for def_word in def_tokens:
            if ((def_word in expanded_tokens) and (not (def_word in chunk_tokens)) and (word_prob.has_key(def_word))):
                print (def_word)
                rank[item] += 1.0 / word_prob [def_word] / len(def_tokens)
        if rank[item] < 500:
            rank[item] = 0
    ranked_synsets = sorted(rank.items(), key=lambda x: x[1], reverse = True)
     
# ************** FOR debugging use ****************
    for i in range(len(ranked_synsets)):
        print (ranked_synsets[i][1], ranked_synsets[i][0].definition)
# *************************************************   
    return ranked_synsets

    
    
# ************** FOR debugging use ****************
#print Lookup(sentence, word)
# *************************************************


    
