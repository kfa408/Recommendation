#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib
import justext
from gensim.parsing.preprocessing import STOPWORDS
import re
import datetime

class ParserError(Exception):
    '''Base class for exceptions in the parser module'''
    pass


class URLRetrievalError(ParserError):
    '''Exception raised for errors in the URL input.
    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
        e    -- the original exception that was raised
    '''

    def __init__(self, expr, msg, e=None):
        self.expr = expr
        self.msg = msg
        self.e = e


class DocumentParsingError(ParserError):
    '''Exception raised for errors in the parsing of the URL.
    Attributes:
        expr -- input expression in which the error occurred
    '''

    def __init__(self, msg):
        self.msg = msg

def scrapeurl(urlin):

    print('start' + str(datetime.datetime.now().time()))

    req = urllib.request.Request(urlin, headers={'User-Agent': 'Mozilla/5.0'})

    try:
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        raise URLRetrievalError(urlin, str(e.code), e)

    except urllib.error.URLError as e:
        raise URLRetrievalError(urlin, str(e.reason), e)

    else:
        print('url good to go' + str(datetime.datetime.now().time()))


        page = urllib.request.urlopen(req).read()
        print('read done' + str(datetime.datetime.now().time()))

        textout = ''

        paragraphs = justext.justext(page, justext.get_stoplist("English"))
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                textout += ' ' + paragraph.text

        print('justext done' + str(datetime.datetime.now().time()))


    lettersonly =  re.sub("[^a-zA-Z'\-]", " ", textout)

    words = lettersonly.lower().split()

    print('re and lower split done' + str(datetime.datetime.now().time()))

    truetext = [w for w in words if not w in STOPWORDS]

    print('stopwords done' + str(datetime.datetime.now().time()))

    return truetext


def scrapeurltitle(urlin):

    try:
        urllib.request.urlopen(urlin)
    except urllib.error.HTTPError as e:
        raise URLRetrievalError(urlin, str(e.code), e)

    except urllib.error.URLError as e:
        raise URLRetrievalError(urlin, str(e.reason), e)

    else:
        page = urllib.request.urlopen(urlin).read()
        soup = BeautifulSoup(page, 'lxml')

    if soup.title is not None:
        return soup.title.string
    else:
        return 'Title Unavailable'
