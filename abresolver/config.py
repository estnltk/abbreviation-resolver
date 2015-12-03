# -*- coding:utf-8 -*-
import os
import sys
from ConfigParser import ConfigParser


class Config(object):
    
    #PROJECT_HOME = '/opt/home/sass/projects/lyhendid'
    #ABBREVIATION_MODEL = os.path.join(PROJECT_HOME, 'tasks/model/results/model.csv')
    #WORD2VEC_MODEL = os.path.join(PROJECT_HOME, 'data/corpus/rontgen_and_anamnees/corpus.t3.word.wvm')
    #WORD2VEC_MODEL = os.path.join(PROJECT_HOME, 'tasks/etl/results/word2vec_training_data/all.snts.word.wvm')
    
    def __init__(self):
        config_file = os.environ.get('CONFIG')
        if config_file is None:
            print('Environment variable "CONFIG" not defined.')
            sys.exit(0)
        config = ConfigParser()
        config.read(config_file)
        
        self.ABBREVIATION_MODEL = config.get('MODEL', 'ABBREVIATION_MODEL')
        self.WORD2VEC_MODEL = config.get('MODEL', 'WORD2VEC_MODEL')
        