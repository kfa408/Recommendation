#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib
import justext
from gensim.parsing.preprocessing import STOPWORDS
import re

def scrapeurl(urlin):

    try:
        urllib.request.urlopen(urlin)
    except urllib.error.HTTPError as e:
        #raise Exception('HTTP Error ' + str(e.code))
        print('http error')
        return None
    except urllib.error.URLError as e:
        #raise Exception('URL Error' + str(e.reason))
        print('http error')
        return None
    else:
        page = urllib.request.urlopen(urlin).read()

        textout = ''

        paragraphs = justext.justext(page, justext.get_stoplist("English"))
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                textout += ' ' + paragraph.text

    lettersonly =  re.sub("[^a-zA-Z'\-]", " ", textout)

    words = lettersonly.lower().split()

    truetext = [w for w in words if not w in STOPWORDS]

    return truetext


def scrapeurltitle(urlin):

    try:
        urllib.request.urlopen(urlin)
    except urllib.error.HTTPError as e:
        #raise Exception('HTTP Error ' + str(e.code))
        print('http error')
        return None
    except urllib.error.URLError as e:
        #raise Exception('URL Error' + str(e.reason))
        print('http error')
        return None
    else:
        page = urllib.request.urlopen(urlin).read()
        soup = BeautifulSoup(page, 'lxml')

    if soup.title is not None:
        return soup.title.string
    else:
        return 'Title Unavailable'
