#!/usr/bin/env python

import json
from collections import defaultdict
import gensim
from gensim import corpora, similarities, models

urldata = json.load(open('speechurl.json'))
textdata = json.load(open('speechtext.json'))

textlist = []

for i in range(0, len(textdata)):
    textlist.append(textdata['id'+str(i)].get('text'))
    if ( i%50 == 0): print('Processed %d of %d\n' % (i, len(textdata)))

dictionary = corpora.Dictionary(textlist)
dictionary.save('speechdict.dict')

corpus = [dictionary.doc2bow(text) for text in textlist]

corpora.MmCorpus.serialize('speechcorp.mm', corpus)
