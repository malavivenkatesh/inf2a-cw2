# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *
from collections import defaultdict

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def noun_stem_threes(s):
    stem = ""
    if (re.match("^has$", s)):
        stem = 'have'    
    elif (re.match("^[^aeiou]ies$", s)):
        stem = s[:-1]
    #any word ending in a y not preceded by a vowel
    elif (re.match("^.*[^aeiou]ies$", s)):
        stem = (s[:-3] + 'y')    
    elif (re.match("^.*[aeiou]y$", s)):
        stem = s[:-1]
    elif (re.match("^.*y$",s[:-1])):
        stem = s[:-1]    
    elif (re.match("^.*(o|x|ch|sh|ss|zz)es$", s)):
        stem = s[:-2]
    elif (re.match("^.*es$", s)):
        stem = s[:-1]
    elif (re.match("^.*s$",s)):
        stem = s[:-1]
    return stem

def unchanging_plurals():
    nouns = []
    dict = {}
    with open("sentences.txt", "r") as f:
        for line in f:
            words = line.split(" ")
            for word_tag in words:
                word_tag = word_tag.split("|")
                if(dict.has_key(word_tag[0])):
                    add(dict[word_tag[0]], word_tag[1])
                else:
                    dict[word_tag[0]] = []
                    add(dict[word_tag[0]], word_tag[1])
    for word in dict.keys():
        if ("NN" in dict[word] and "NNS" in dict[word]):
            add(nouns, word)
    return nouns

unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    # add code here
    if (s in unchanging_plurals_list):
        return s
    elif (re.match(".*men", s)):
        return s[:-3] + "man"
    else:
        if (noun_stem_threes(s) in unchanging_plurals_list):
            return ""
        else:
            return noun_stem_threes(s)
    

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    possible_tags = []
    if wd in function_words:
        for (word, tag) in function_words_tags:
            if (word == wd):
                add(possible_tags, tag)
        return possible_tags
    
    ns = noun_stem(wd)
    vs = verb_stem(wd)

    if (wd in lx.getAll('P')):
        add(possible_tags,'P')
    if (wd in lx.getAll('N')):
        #do some checks
        if (ns == wd):
            add(possible_tags, 'Ns')
            add(possible_tags, 'Np')
        elif (ns != ""):
            add(possible_tags, 'Np')
        else:
            add(possible_tags, 'Ns')
    elif (ns in lx.getAll('N')):
        add (possible_tags,'Np')
    if (wd in lx.getAll('A')):
        add(possible_tags,'A')
    if (wd in lx.getAll('I')):
        if (vs == wd):
            add(possible_tags, 'Is')
            add(possible_tags, 'Ip')
        elif (vs != ""):
            add(possible_tags, 'Is')
        else:
            add(possible_tags, 'Ip')
    elif (vs in lx.getAll('I')):
            add(possible_tags, 'Is')
    if (wd in lx.getAll('T')):
        if (vs == wd):
            add(possible_tags, 'Ts')
            add(possible_tags, 'Tp')
        elif (vs != ""):
            add(possible_tags, 'Ts')
        else:
            add(possible_tags, 'Tp')
    elif (vs in lx.getAll('T')):
        add(possible_tags, 'Ts')

    return possible_tags

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]


if __name__ == "__main__":
    # code for a simple testing, feel free to modify
    print (noun_stem("ashes"))
# End of PART B.