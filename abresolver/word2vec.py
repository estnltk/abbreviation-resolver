import re

import gensim
import six
import numpy as np
import random
from bisect import bisect_right
from numpy import exp, log, prod, dot


class OutOFVocabularyException(Exception):
    pass


class Word2VecMockContextModel(object):
    
    
    def get_score(self, term, i, sentence):
        return np.random.rand()
    
    
    def get_context_fitness(self, term, i, sentence, sample_size=30):
        """ returns area, rank, rank_p"""
        rank = np.random.randint(0, sample_size)
        rank_p = float(rank) / sample_size * 100.
        area = rank_p / 100.
        return area, rank, rank_p
    
    
class Word2VecContextModel(object):
    OOV_SCORE = 1e-100
    
    def __init__(self, model_fnm, window=5):
        self.model = Word2VecModel(model_fnm)
        self.window = window
    
    def get_score(self, term, i, sentence):
        context = sentence[i-self.window:i] + sentence[i+1:i+1+self.window]
        return self.cp(term, context)
    
    def __contains__(self, term):
        return term in self.model.model.vocab
    
    def cp(self, w, context):
        if w not in self:
            return self.OOV_SCORE
        ps = []
        for w1 in context:
            try:
                p = self.model.cwp(w, w1)
            except OutOFVocabularyException:
                pass
            else:
                ps.append(p)
        return exp(sum(log(p) for p in ps))
    
    
    def get_context_fitness(self, term, i, sentence, sample_size=30):
        context = sentence[:i] + sentence[i+1:]
        
        sample_ws = random.sample(self.model.vocabulary, sample_size)
        sample_ps = [self.cp(w, context) for w in sample_ws]
        sample_ps.sort()
        
        p = self.cp(term, context)
        idx = bisect_right(sample_ps, p)
        area = sum(sample_ps[idx:]) / sum(sample_ps)
        rank = len(sample_ps) - idx
        rank_p = 100. * rank / float(len(sample_ps))
        return area, rank, rank_p


class Word2VecModel(object):
    
    
    def __init__(self, model):
        if isinstance(model, six.string_types):
            self.model = gensim.models.Word2Vec.load(model)
        else:
            self.model = model
    
    
    @property
    def vocabulary(self):
        return self.model.vocab.keys()
    
    
    def cwp(self, w, w1):
        '''
        Computes P[ W(i+n) | W(i) ] = P(w1 | w) 
        
        Parameters:
        -----------
        w - str: target word
        w1 - str: context word 
        '''
        
        try:
            W = self.model.vocab[w]
        except KeyError:
            raise OutOFVocabularyException(w)
        
        try:
            W1 = self.model.vocab[w1]
        except KeyError:
            raise OutOFVocabularyException(w1)
        
        l1 = self.model.syn0[W.index]
        l2a = self.model.syn1[W1.point]
        code = np.array([-1 if c == 1 else 1 for c in W1.code])
        x = dot(l1, l2a.T) * code
        fa = 1.0 / (1.0 + exp(-x))
        return prod(fa)
    
    
    def cp(self, w, context):
        """
        Computes context probability
        P(c|w) = P(w1|w)*P(w2|w)*...*P(wn|w)
        
        Parameters
        ----------
        w: str
            target word
        context: list
            list of context words
        """
        
        return exp(sum(log(self.cwp(w, w1)) for w1 in context))
    
    
    def get_word_rank(self, w, context, sample_size=100):
        """
        Get the rank of P(context|w) in a sample of probabilities P(context|r)
        for random words in vocabulary.
        """
        sample_ws = random.sample(self.vocabulary, sample_size)
        sample_ps = [self.cp(w, context) for w in sample_ws]
        sample_ps.sort()
        
        p = self.cp(w, context)
        w_idx = bisect_right(sample_ps, p)
        area = sum(sample_ps[w_idx:]) / sum(sample_ps)
        rank = sample_size - w_idx
        rank_p = 100. * rank / float(sample_size)
        return rank, rank_p, area
    
    
    def top_context_words(self, w, n=100):
        """
        Finds n words with maximal P(word|w) values.
        """
        words = sorted(self.model.vocab.items(), key=lambda item: -item[1].count)[:n]
        words = [w[0] for w in words]
        probs = [self.cwp(w, w1) for w1 in words]
        return words, probs


class SentenceIterator(object):
    
    def __init__(self, fname, n=np.Inf):
        self.fname = fname
        self.n = n
        
    def __iter__(self):
        snt = []
        for i, ln in enumerate(open(self.fname, encoding='utf8', errors="surrogateescape")):
            if i >= self.n:
                break
            
            if i % 100000 == 0:
                print(i)
            
            snt = ln.rstrip().split()
            yield snt
            

class T3SentenceIterator(object):
    
    def __init__(self, fname, n=np.Inf, use_lemmas=True):
        self.fname = fname
        self.n = n
        if use_lemmas:
            self.pat = re.compile(r'\s{4}(?P<lemma>.+?)\s//', flags=re.U)
            self.parse_line = self.parse_line_lemma
        else:
            self.pat = re.compile(r'^(?P<word>.+?)\s{4}', flags=re.U)
            self.parse_line = self.parse_line_word
        
    def parse_line_word(self, line):
        w = self.pat.search(line).group('word')
        return w.lower()
        
    def parse_line_lemma(self, line):
        lemma = self.pat.search(line).group('lemma')
        lemma = lemma.split("+")[0].split("//")[0].replace('=', '').replace("_", " ")
        return lemma.lower()
    
    def __iter__(self):
        snt = []
        for i, ln in enumerate(open(self.fname, encoding='utf8', errors="surrogateescape")):
            if i >= self.n:
                break
            
            if i % 100000 == 0:
                print(i)
            
            ln = ln.rstrip()
            if not ln.startswith('<'):
                try:
                    lem = self.parse_line(ln)
                except AttributeError:
                    print('Error in line: "%s"' % ln)
                    raise
                snt.append(lem)
            elif ln == '</s>':
                yield snt
                snt = []
    