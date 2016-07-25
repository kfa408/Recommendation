#!/usr/bin/env python

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import gensim
from gensim import corpora, models, similarities
import re


import scraper

dictionary = corpora.Dictionary.load('speechdict.dict')
corpus = corpora.MmCorpus('speechcorp.mm')
lsi = models.LsiModel.load('speech.lsi')
index = similarities.MatrixSimilarity.load('speechsimindex.index')

def lsirecommend(inputurl):

    inputtext = scraper.scrapeurl( inputurl )
    vec_bow = dictionary.doc2bow(inputtext)
    vec_lsi = lsi[vec_bow]

    #index = similarities.MatrixSimilarity(lsi[corpus])
    sims = index[vec_lsi]

    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    return sims[:5]
