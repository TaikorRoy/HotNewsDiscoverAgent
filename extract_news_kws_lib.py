# -*- coding: utf-8 -*-
__author__ = 'Taikor'

import pynlpir


def extract_news_kws(hot_news):
    pynlpir.open()
    s = hot_news
    kw_list = pynlpir.segment(s, pos_tagging=False)
    kws = ""
    for kw in kw_list:
        kws = kws + kw + " "
    kws = kws.strip()
    return kws
