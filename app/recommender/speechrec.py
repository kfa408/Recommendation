#!/usr/bin/env python

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from recommender.base import Recommender
from gensim import corpora, models, similarities
import scraper
import os
import json

class SpeechRec(Recommender):

    recommender_id = 'speechrec'

    def __init__(self, corpus_name):
        self.load_corpus(corpus_name)
        pass

    def load_corpus(self, corpus_name):
        self.corpus_name = corpus_name
        self.dictionary = corpora.Dictionary.load( corpus_name + '.dict')
        self.corpus = corpora.MmCorpus(corpus_name + '.mm')
        self.lsi = models.LsiModel.load(corpus_name  + '.lsi')
        self.index = similarities.MatrixSimilarity.load(corpus_name + '.index')

        dbsite = os.path.realpath(os.path.dirname(__file__))
        json_file = open(os.path.join(dbsite, corpus_name + 'url.json'))
        self.data = json.load(json_file)
        json_file.close()

    def recommendation_for_corpus_member(self, article_id):
        # return a list of IDs of recommended articles
        raise NotImplementedError()

    def recommendation_for_text(self, inputtext):

        #inputtext = scraper.scrapeurl( inputurl )

        vec_bow = self.dictionary.doc2bow(inputtext)

        vec_lsi = self.lsi[vec_bow]
        #index = similarities.MatrixSimilarity(lsi[corpus])
        sims = self.index[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        topresults = sims[:5]
        #resultdata = [ ('Source' , scraper.scrapeurltitle(inputurl), inputurl, 'Source link' )]
        resultdata = []

        for i in range(0,5):
            nowid = 'id'+ str(topresults[i][0])
            a_vect =  (nowid, self.data[nowid]['title'], self.data[nowid]['url'], str(topresults[i][1]) )
            resultdata.append(a_vect)

        return resultdata
