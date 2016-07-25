#!/usr/bin/env python

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import gensim
from gensim import corpora, models, similarities

dictionary = corpora.Dictionary.load('speechdict.dict')
corpus = corpora.MmCorpus('speechcorp.mm')

print(corpus)

tfidf = models.TfidfModel(corpus)

corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel(corpus_tfidf, id2word = dictionary, num_topics = 150)

corpus_lsi = lsi[corpus_tfidf]

lsi.print_topics(10)

lsi.save('speech.lsi')

index = similarities.MatrixSimilarity(lsi[corpus])

index.save('speechsimindex.index')
