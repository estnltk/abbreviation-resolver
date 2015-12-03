# -*- coding: utf8 -*-
import unittest

from ..text import Text


class Test(unittest.TestCase):

    def test_text(self):
        # For now, make sure methods work
        t = Text(u'kolmas p palavik. püsib p pahhüpleuraalne ladestus')
        t.tokenize_abr()
        t.abr_expansions
        t.abr_scores
        t.abr_texts
        t.abr_spans
        t.abr_starts
        t.abr_ends
        t.tag('abr')
        t.split_by('abr')


if __name__ == "__main__":
    unittest.main()