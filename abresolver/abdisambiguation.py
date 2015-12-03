import operator as op
from collections import namedtuple
import numpy as np


AbbreviationExpansion = namedtuple('AbbreviationExpansion', 'term am_score cm_score score')
ContextFitness = namedtuple('ContextFitness', 'area rank rank_p')


class Word2VecDisambiguator(object):
    
    
    def __init__(self, am, cm):
        self.am = am
        self.cm = cm
    
    
    def process(self, sentence, i):
        a = sentence[i]
        expansions, cf = None, None
        if a in self.am:
            terms = self.am.get_expansions(a)
            am_scores = [self.am.get_p_term_given_abbreviation(t, a) for t in terms]
            cm_scores = [self.cm.get_score(t, i, sentence) for t in terms]
            scores = np.multiply(am_scores, cm_scores)
            scores /= sum(scores)
            
            expansions = list(zip(terms, am_scores, cm_scores, scores))
            expansions = [AbbreviationExpansion(*e)
                          for e in zip(terms, am_scores, cm_scores, scores)]
            expansions.sort(key=op.attrgetter('score'), reverse=True)
            
            top_term = expansions[0].term
            area, rank, rank_p = self.cm.get_context_fitness(top_term, i, sentence)
            cf = ContextFitness(area, rank, rank_p)
        
        return expansions, cf


class AbbreviationDisambiguator(object):
    
    
    def __init__(self, m, cm):
        self.model = m
        self.cm = cm
    
    
    def process(self, sentence):
        """
        sentence: list of words
        """
        _sentence = []
        m, cm = self.model, self.cm
        
        for i, a in enumerate(sentence):
            _token = {'term':   a}
            if m.has_abbreviation(a):
                candidate_terms = m.get_expansions(a)
                cm_scores = cm.get_raw_scores(candidate_terms, i, sentence)
#                 cm_scores = [1. for c in candidate_terms]
                am_scores = [ m.get_p_term_given_abbreviation(c, a) for c in candidate_terms ]
#                 am_scores = [ 1. for c in candidate_terms ]
                norm = sum(a*b for a, b in zip(cm_scores, am_scores))
                scores = [ lm_s * m_s / norm for lm_s, m_s in zip(cm_scores, am_scores) ]
                scored_candidates = list(zip(candidate_terms, scores, am_scores, cm_scores))
                scored_candidates.sort(key=op.itemgetter(1), reverse=1)
                _token['expansions'] = scored_candidates
            _sentence.append(_token)
        return _sentence
    