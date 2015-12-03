# -*- coding: UTF-8 -*-
"""
The class Text extends estnltk's class Text and adds abbreviation layer.

Usage:
    
    >> from abresolver import Text
    >> t = Text(u'kolmas p palavik')
    >> t.tokenize_abs()
    [{
      'text': 'p',
      'start': 7,
      'end': 8,
      'expansions': ['päev',
                     'parem',
                     'parietaalne',
                     'pupill',
                     'pool'],
      'scores': [0.99974249284129602,
                 0.00013896032431022265,
                 0.00010385371199489893,
                 9.3145225880433136e-06,
                 5.3785998108879645e-06],
      }]
"""
import logging

import pandas as pd
from estnltk import Text as EstnltkText
from estnltk.names import START, END, TEXT
from cached_property import cached_property

from . import config
from .abmodel import Model as AbbreviationModel
from .word2vec import Word2VecContextModel
from .abdisambiguation import Word2VecDisambiguator


log = logging.getLogger(__name__)
config = config.Config()
ab_disambiguator = None

ABR = 'abr'
EXPANSIONS = 'expansions'
SCORES = 'scores'


def get_disambiguator():
    global ab_disambiguator
    if ab_disambiguator is None:
        log.debug('Loading models...')
        ab_disambiguator = Word2VecDisambiguator(
                       AbbreviationModel(pd.read_csv(config.ABBREVIATION_MODEL, encoding='utf8')),
                       Word2VecContextModel(config.WORD2VEC_MODEL))
    return ab_disambiguator


class Text(EstnltkText):
    
    
    def __init__(self, *args, **kwargs):
        super(Text, self).__init__(*args, **kwargs)
        
    
    @cached_property
    def layer_tagger_mapping(self):
        mapping = super(Text, self).layer_tagger_mapping
        mapping[ABR] = self.tokenize_abr
        return mapping
    
    
    @cached_property
    def abr(self):
        """ A list of personally identifiable information in `abr` layer """
        if not self.is_tagged(ABR):
            self.tokenize_abr()
        return self[ABR]
    
    
    @cached_property
    def abr_texts(self):
        """The list of words representing `abr` layer elements."""
        if not self.is_tagged(ABR):
            self.tokenize_abr()
        return [pii[TEXT] for pii in self[ABR]]
    
    @cached_property
    def abr_spans(self):
        """The list of spans representing `abr` layer elements."""
        if not self.is_tagged(ABR):
            self.tokenize_abr()
        return self.spans(ABR)
    
    
    @cached_property
    def abr_starts(self):
        """The list of start positions representing `abr` layer elements."""
        if not self.is_tagged(ABR):
            self.tokenize_abr()
        return self.starts(ABR)
    
    
    @cached_property
    def abr_ends(self):
        """The list of end positions representing `abr` layer elements."""
        if not self.is_tagged(ABR):
            self.tokenize_abr()
        return self.ends(ABR)
    
    
    @cached_property
    def abr_expansions(self):
        if not self.is_tagged(ABR):
            self.tokenize_abr()
        return [item[EXPANSIONS] for item in self[ABR]]
    
    
    @cached_property
    def abr_scores(self):
        if not self.is_tagged(ABR):
            self.tokenize_abr()
        return [item[SCORES] for item in self[ABR]]
    
       
    def tokenize_abr(self):
        """ Add `abr`-layer annotations."""
        items = []
        for snt, snt_start in zip(self.split_by_sentences(), self.sentence_starts):
            snt_words = [w.lower() for w in snt.word_texts]
            for i, w in enumerate(snt.words):
                expansions, context_fitness = get_disambiguator().process(snt_words, i)
                if expansions:
                    items.append({START:      snt_start + w[START], 
                                  END:        snt_start + w[END],
                                  TEXT:       w[TEXT],
                                  EXPANSIONS: [e.term for e in expansions],
                                  SCORES:     [e.score for e in expansions],
                                  })
        self[ABR] = items
        return items
        
    
    