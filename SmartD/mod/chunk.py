import nltk
from nltk.corpus import wordnet as wn

# ************** for debugging use ****************
#sentence = 'I previously booked the nice flight.'
#sentence = 'I bought a book.'

#sentence = 'I turn on the bright light.'

#sentence = 'Peter sold the farmer rice and put the computer monitor on.'
#sentence = 'He puts the cloth on.'

#sentence = 'Peter sold the car dealer computer monitor.'
#sentence = 'The computer monitor is broken.'

#word = 'booked'
#word = 'turn'
#word = 'puts'      # --> 'put' or 'put_on'
#word = 'farmer'   # --> 'farmer' not 'farmer rice'
#word = 'computer' # --> 'computer_monitor' or 'car_dealer'

#tokens = nltk.word_tokenize(sentence)
#tokens = ['Peter', 'sold', 'the', 'farmer', 'computer', 'monitor', '.']
#tagged = nltk.pos_tag(tokens)
#tagged = [('Peter', 'NNP'), ('sold', 'VBD'), ('the', 'DT'), ('farmer', 'NN'), ('computer', 'NN'), ('monitor', 'NN'), ('.', '.')]

# *************************************************

pos_map = {'VBP':'VERB','VB':'VERB','VBD':'VERB','VBG':'VERB','VBN':'VERB','VBZ':'VERB', 'NN':'NOUN', 'NNS':'NOUN','NNP':'NOUN','NNPS':'NOUN','JJ':'ADJ', 'JJR':'ADJ', 'JJS':'ADJ', 'RB':'ADV','RBR':'ADV','RBS':'ADV', 'DT':'DT', 'IN':'PP', 'RP':'PP'}

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
    # determine the pos of the word
    word_tag = [item[1] for item in tagged if item[0] == word][0]
    # if combining all rules in one grammar,
    # previous ones has higher priority.
    # The former rules will forbid the later ones' detection.
    # Since the reg_exp parser is efficient,
    # use different grammars as knowledge to parse saparetly

    # handle the verb phrase
    if word_tag[0] == 'V':
        grammar_V_PP = "_VP: {<%s><DT|PP\$>?<JJ>*<NN|NNP|NNS|NNPS>*<IN|RP>}  # verb noun-phrase pp" % word_tag
        cp = nltk.RegexpParser(grammar_V_PP)
        result = list(cp.parse(tagged))
        # ****************FOR DEBUGING******************
        print result
        # **********************************************
        
        for item in result:
            # such pattern existed
            if type(item) is nltk.tree.Tree:
                # the searched word in such chunk
                if (word, word_tag) in list(item):
                    # find the possible pp
                    pp = [item[0] for item in list(item) if (item[1] == 'IN' or item[1] == 'RP')][0]
                    # Normalize word ('puts'-> 'put')
                    normalized = wn.morphy(word, wn.VERB)
                    if normalized != None:
                        word = normalized
                    possible_chunk = word+'_'+pp
                    # ****************FOR DEBUGING******************
                    #print possible_chunk
                    # **********************************************
                    # in case the consecutive Noun is not a phrase
                    if wn.synsets(possible_chunk) == []:
                        return word
                    else:
                        return possible_chunk

    # handle the noun phrase
    if word_tag[0] == 'N':
        grammar_NOUNS = "_NP: {<NN>+} # consecutive nouns"
        cp = nltk.RegexpParser(grammar_NOUNS)
        result = list(cp.parse(tagged))
        # ****************FOR DEBUGING******************
        print result
        # **********************************************
        
        for item in result:
            # such pattern existed
            if type(item) is nltk.tree.Tree:
                print item
                # the searched word in such chunk
                if (word, word_tag) in list(item):
                    noun_list = [x[0] for x in list(item)]
                    l = len(noun_list)
                    for i in range(l - 1):
                        for j in range(l - i):
                            if i < l-j-1:
                                possible_chunk = '_'.join([k for k in noun_list[i:l-j]])
                                if word in noun_list[i:l-j] and wn.synsets(possible_chunk) != []:
                                    return possible_chunk

    return word

# ****************FOR DEBUGING******************
#print chunktaged(tokens, tagged, word)

            
