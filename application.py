#!/usr/bin/env python

import os
from flask import Flask, json, jsonify, render_template, redirect, request
from flask_restful import Resource, Api, abort, reqparse

import lsirec
import scraper

app = Flask(__name__)
api = Api(app)


dbsite = os.path.realpath(os.path.dirname(__file__))

#Loads the file with the sites data.
json_file = open(os.path.join(dbsite, 'SiteList.json'))
data = json.load(json_file)
json_file.close()

inputid = None


@app.route('/')
def enterurl():
    return render_template('enterurl.html')


@app.route('/', methods = ['POST'])
def show_rec():
    inputurl = request.form['inputurl']

    #here is the missing part where it talks to page suggestion, and returns suggestions

    #see if the input url is already in site list
    #Not the best now. Will think of way to fix.
    for items in data.items():
        if inputurl in items[1].get('url'):
            inputid = items[0]
            break
        else:
            inputid = 'idx'

    resultdata = [ (inputid , scraper.scrapeurltitle(inputurl), inputurl, 'Source link' )]

    resultlist = lsirec.lsirecommend(inputurl)

    for i in range(0,5):
        nowid = 'id'+ str(resultlist[i][0])
        a_vect =  (nowid, data[nowid]['title'], data[nowid]['url'], str(resultlist[i][1]) )
        resultdata.append(a_vect)

    print(resultlist)
    print(resultdata)

    return render_template('sitelist1.html', resultdata = resultdata, inputid = inputid)



if __name__ == "__main__":
    app.run()
