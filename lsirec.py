#!/usr/bin/env python

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
import re
import scraper
import os
import json
import datetime

dictionary = corpora.Dictionary.load('speechdict.dict')
corpus = corpora.MmCorpus('speechcorp.mm')
lsi = models.LsiModel.load('speech.lsi')
index = similarities.MatrixSimilarity.load('speechsimindex.index')

dbsite = os.path.realpath(os.path.dirname(__file__))
#Loads the file with the sites data.
json_file = open(os.path.join(dbsite, 'SiteList.json'))
data = json.load(json_file)
json_file.close()


def lsirecommend(inputurl):

    inputtext = scraper.scrapeurl( inputurl )

    vec_bow = dictionary.doc2bow(inputtext)

    vec_lsi = lsi[vec_bow]

    #index = similarities.MatrixSimilarity(lsi[corpus])
    sims = index[vec_lsi]

    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    topresults = sims[:5]

    #resultdata = [ ('Source' , scraper.scrapeurltitle(inputurl), inputurl, 'Source link' )]
    resultdata = []

    for i in range(0,5):
        nowid = 'id'+ str(topresults[i][0])
        a_vect =  (nowid, data[nowid]['title'], data[nowid]['url'], str(topresults[i][1]) )
        resultdata.append(a_vect)

    return resultdata
