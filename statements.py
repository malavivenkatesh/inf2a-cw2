# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements
from nltk.corpus import brown
import re
from collections import defaultdict


def add(lst, item):
    if (item not in lst):
        lst.insert(len(lst), item)


corpus = set(brown.tagged_words())

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    # add code here

    def __init__(self):
        self.lex = {}

    def add(self, stem, cat):
        if (self.lex.has_key(cat)):
            add(self.lex[cat], stem)
        else:
            self.lex[cat] = []
            add(self.lex[cat], stem)

    def getAll(self, cat):
        # convert to a set to remove duplicates and then convert to a list again to print
        if (self.lex.has_key(cat)):
            return self.lex[cat]
        else:
            return []


class FactBase:
    """stores unary and binary relational facts"""

    def __init__(self):
        self.binary = {}
        self.unary = {}

    def addUnary(self, pred, e1):
        if (not (self.unary.has_key(pred))):
            self.unary[pred] = []
        add(self.unary[pred], e1)

    def addBinary(self, pred, e1, e2):
        if (not (self.binary.has_key(pred))):
            self.binary[pred] = []
        add(self.binary[pred], (e1,e2))

    def queryUnary(self, pred, e1):
        if (self.unary.has_key(pred)):
            return (e1 in self.unary[pred])
        else:
            return False

    def queryBinary(self, pred, e1, e2):
        if(self.binary.has_key(pred)):
            return ((e1,e2) in self.binary[pred])
        else:
            return False
        

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    stem = ''
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

    if((stem, "VB") in corpus) or ((s, "VBZ") in corpus) or stem in ['have', 'do', 'are']:
        return stem
    else:
        return ''


def add_proper_name(w, lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w, 'P')
        return ''
    else:
        return (w + " isn't a proper name")


def process_statement(lx, wlist, fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name(wlist[0], lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a', 'an']):
                lx.add(wlist[3], 'N')
                fb.addUnary('N_'+wlist[3], wlist[0])
            else:
                lx.add(wlist[2], 'A')
                fb.addUnary('A_'+wlist[2], wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add(stem, 'I')
                fb.addUnary('I_'+stem, wlist[0])
            else:
                msg = add_proper_name(wlist[2], lx)
                if (msg == ''):
                    lx.add(stem, 'T')
                    fb.addBinary('T_'+stem, wlist[0], wlist[2])
    return msg


if __name__ == "__main__":
    # code for a simple testing, feel free to modify
    lx = Lexicon()
    lx.add('John', 'P')
    lx.add('like', 'T')
    lx.add('John', 'P')
    lx.add('Mary', 'P')
    print lx.getAll('P')
    print lx.getAll('T')
    
    fb = FactBase()
    fb.addUnary("duck","John")
    fb.addBinary("love","John","Mary")
    fb.queryUnary("duck","John") # returns True
    fb.queryBinary("love","Mary","John") # returns False)

    print verb_stem("fixes")

# End of PART A.
