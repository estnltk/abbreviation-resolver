# -*- coding: utf-8 -*-
import os
import sys
from six.moves.configparser import ConfigParser


class Config(object):
    
    
    def __init__(self):
        config_file = os.environ.get('CONFIG')
        if config_file is None:
            print('Environment variable "CONFIG" not defined.')
            sys.exit(0)
        config = ConfigParser()
        config.read(config_file)
        
        self.ABBREVIATION_MODEL = config.get('MODEL', 'ABBREVIATION_MODEL')
        self.WORD2VEC_MODEL = config.get('MODEL', 'WORD2VEC_MODEL')
        