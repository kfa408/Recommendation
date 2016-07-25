import os
import pandas, html5lib, requests, nltk
import json
from bs4 import BeautifulSoup
import urllib
import re
import scraper

def scrapeurljson(urlin):

    page = urllib.request.urlopen(urlin).read()
    soup = BeautifulSoup(page, 'lxml')

    with open('speechurl.json') as f:
        data = json.load(f)

    with open('speechtext.json') as g:
        datag = json.load(g)


    i = len(data) - 1

    for link in soup.find_all('a'):
        if link.get('href') is not None and 'speeches/' in link.get('href'):
            if 'mp3' not in link.get('href'):
                textreturn =  scraper.scrapeurl('http://www.americanrhetoric.com/' + link.get('href'))
                if textreturn is not None:
                    i += 1
                    titlereturn = scraper.scrapeurltitle('http://www.americanrhetoric.com/' + link.get('href'))
                    a_dict = { 'id'+str(i) : {'url' : 'http://www.americanrhetoric.com/' + link.get('href'), 'title' : titlereturn } }
                    b_dict = { 'id'+str(i) : {'url' : 'http://www.americanrhetoric.com/' + link.get('href'), 'text' : textreturn } }
                    data.update(a_dict)
                    datag.update(b_dict)

    with open('speechurl.json', 'w') as f:
        json.dump(data,f, sort_keys = True)

    with open('speechtext.json', 'w') as g:
        json.dump(datag,g, sort_keys = True)

    return 'done'
