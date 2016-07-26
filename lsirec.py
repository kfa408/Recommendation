#!/usr/bin/env python

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import gensim
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

    print('start' + str(datetime.datetime.now().time()))

    inputtext = scraper.scrapeurl( inputurl )

    print('scraper done' + str(datetime.datetime.now().time()))

    vec_bow = dictionary.doc2bow(inputtext)

    print('vec done' + str(datetime.datetime.now().time()))

    vec_lsi = lsi[vec_bow]

    print('proj done' + str(datetime.datetime.now().time()))

    #index = similarities.MatrixSimilarity(lsi[corpus])
    sims = index[vec_lsi]

    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    print('sims and sort complete' + str(datetime.datetime.now().time()))

    topresults = sims[:5]

    print('sims and sort complete' + str(datetime.datetime.now().time()))

    #resultdata = [ ('Source' , scraper.scrapeurltitle(inputurl), inputurl, 'Source link' )]
    resultdata = []

    print('result data initialized' + str(datetime.datetime.now().time()))

    for i in range(0,5):
        nowid = 'id'+ str(topresults[i][0])
        a_vect =  (nowid, data[nowid]['title'], data[nowid]['url'], str(topresults[i][1]) )
        resultdata.append(a_vect)

    return resultdata
