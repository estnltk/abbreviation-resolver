# -*- coding: utf8 -*-
import logging

import pandas as pd
from estnltk import Text as EstnltkText

from . import config
from . abmodel import Model as AbbreviationModel
from . word2vec import Word2VecContextModel, Word2VecMockContextModel
from . abdisambiguation import Word2VecDisambiguator


log = logging.getLogger(__name__)
ABR = 'abr'
config = config.Config()
ab_disambiguator = Word2VecDisambiguator(
                       AbbreviationModel(pd.read_csv(config.ABBREVIATION_MODEL, encoding='utf8')),
                       Word2VecContextModel(config.WORD2VEC_MODEL))


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
        return self.ends(ABRs)
    
    
    def tokenize_abr(self):
        """ Add `abr`-layer annontations."""
        dicts = []
        for snt in self.split_by_sentences():
            snt_words = [w.lower() for w in snt.word_texts]
            for i, w in enumerate(snt.words):
                expansions, context_fitness = ab_disambiguator.process(snt_words, i)
                if expansions:
                    dicts.append({START:             w[START], 
                                  END:               w[END],
                                  TEXT:              w[TEXT],
                                  'expansions':      expansions,
                                  'context_fitness': context_fitness})
        text[ABR] = dicts
        
    
    