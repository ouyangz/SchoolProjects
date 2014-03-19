import nltk
from nltk.corpus import wordnet as wn

# ************** for debugging use ****************
#sentence = 'I previously booked the nice flight.'
#sentence = 'I bought a book.'

#sentence = 'I turn on the bright light.'

#sentence = 'Peter sold the farmer rice and put the computer monitor on.'
#sentence = 'He puts the cloth on near the desk.'

#sentence = 'Peter sold the farmer rice.'
#sentence = 'The computer monitor is broken.'

#word = 'booked'
#word = 'turn'
#word = 'puts'      # --> 'put' or 'put_on'
#word = 'farmer'   # --> 'farmer' not 'farmer rice'
#word = 'computer' # --> 'computer_monitor'

#tokens = nltk.word_tokenize(sentence)
#tagged = nltk.pos_tag(tokens)
# *************************************************

pos_map = {'VBP':'VERB','VB':'VERB','VBD':'VERB','VBG':'VERB','VBN':'VERB','VBZ':'VERB', 'NN':'NOUN', 'NNS':'NOUN','NNP':'NOUN','NNPS':'NOUN','JJ':'ADJ', 'JJR':'ADJ', 'JJS':'ADJ', 'RB':'ADV','RBR':'ADV','RBS':'ADV', 'DT':'DT', 'RP':'PP'}

def chunktaged(tokens, tagged, word):
    '''
    Extract the meaningful chunk (phrase) from the sentence.
    Also can be imagined as a phrase detection.

    PARAMETER LIST:
    tokens is a list of the words in the sentence:
    ['I', 'previously', 'booked', 'the', 'nice', 'flight', '.']
    tagged is a list of tuples consisting of word and POS:
    [('I', 'PRP'), ('previously', 'RB'), ('booked', 'VBD'), ('the', 'DT'), ('nice', 'JJ'), ('flight', 'NN'), ('.', '.')]
    word is what we look up for:
    'booked'

    The return value should be a phrase like 'turn_on' or just the origin word.

    # the rules as our knowledge:
    # 1, consecutive nouns
    # 2, verb before a preposition
    '''

    word_index = tokens.index(word)
    
    if (pos_map.has_key(tagged[word_index][1])):
        word_pos = pos_map[tagged[word_index][1]]
    else:
        return word

    if (word_pos == 'VERB' and (wn.morphy(word, wn.VERB) != None)):
        word = wn.morphy(word, wn.VERB)
    elif (word_pos == 'NOUN' and (wn.morphy(word, wn.NOUN) != None)):
        word = wn.morphy(word, wn.NOUN)
    
    if word_index == len(tokens) - 1:
        return word

    if (pos_map.has_key(tagged[word_index + 1][1])):
        next_word_pos = pos_map[tagged[word_index + 1][1]]
    else:
        return word

    if (word_pos == 'VERB' and next_word_pos == 'PP') or \
       (word_pos == 'NOUN' and next_word_pos == 'NOUN'):
        possible_chunk = word + '_' + tokens[word_index+1]
        # in case the consecutive Noun is not a phrase
        if wn.synsets(possible_chunk) == []:
            return word
        else:
            return possible_chunk
    else:
        return word


# ****************FOR DEBUGING******************
#print chunktaged(tokens, tagged, word)

