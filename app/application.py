#!/usr/bin/env python

import os
from flask import Flask, json, jsonify, render_template, redirect, request
from flask_restful import Resource, Api, abort, reqparse

from recommender.base import Recommender
# Import the recommendation engines here to register them
from recommender.speechrec import SpeechRec
import scraper
import random
import time

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

import recordclicks

app = Flask(__name__)
api = Api(app)


client = MongoClient()
db = client.clickdb
clicks = db.clicks

print(client.address)

@app.route('/')
def enterurl():
    return render_template('enterurl.html')


@app.route('/', methods = ['POST'])
def show_rec():

    inputurl = request.form['inputurl']

    userecAPI = recommendAPI()
    userecAPI.reqparse.remove_argument('url')
    userecAPI.reqparse.add_argument('url', type = str, default = inputurl)
    #print(userecAPI.reqparse.parse_args())

    resultdata = userecAPI.get('speech')
    #print(resultdata)

    return render_template('sitelist.html', resultdata = resultdata)

@app.route('/api/click/v1.0/<source_id>/<recommendation_number>')
def redirecturl(source_id, recommendation_number):

    #print(source_id)

    newurl = clicks.find_one({'_id':ObjectId(source_id)}).get('response')[int(recommendation_number)][2]

    clicks.update({'_id': ObjectId(source_id)}, {'$push': {'clicks' : {'response_id': int(recommendation_number), 'time': time.time()}}})

    #print(newurl)
    return redirect(newurl)


class recommendAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url',
                                   type=str,
                                   required = True,
                                   help='url for document that requires content recommendation')
        # Prepare the list of available engines. This will find all engines
        # that are imported explicitly
        self.engine_classes = Recommender.__subclasses__()
        self.recommenders = dict()
        super(recommendAPI, self).__init__()

    def get(self, corpus_name):
        # Get the argument: a URL as a string
        start_time = time.time()
        args = self.reqparse.parse_args()
        # Check the input URL
        try:
            text_from_url = scraper.scrapeurl(args.url)
        except scraper.URLRetrievalError:
            abort(scraper.URLRetrievalError.e)
        except scraper.DocumentParsingError:
            abort(415)
        # Now, pick a recommendation engine. For now, this is done at random
        random_recommender = random.choice(self.engine_classes)
        if (random_recommender, corpus_name) not in self.recommenders:
            self.recommenders[(random_recommender, corpus_name)] = random_recommender(corpus_name)
        this_recommender = self.recommenders[(random_recommender, corpus_name)]
        recommendation = this_recommender.recommendation_for_text(text_from_url)

        response_time = time.time() - start_time
        #print(recordclicks.getdbdoc( corpus_name, args.url, response_time, recommendation ))
        recdbdoc = recordclicks.getdbdoc( corpus_name, args.url, response_time, recommendation )
        #if not clicks.find_one({"url": args.url}):
        post_id = clicks.insert_one(recdbdoc).inserted_id
        post_id_str = str(post_id)


        recommendation = [(item[0], item[1], '/api/click/v1.0/' + post_id_str + '/' + str(recommendation.index(item)), item[3]) for item in recommendation]

        return recommendation

#class ClickTrackingAPI(Resource):
#    def get(self, sourceid, recommendation_number):
#        return redirect(clicks.find_one({'_id':ObjectId(sourceid)}).get('url'))

api.add_resource(recommendAPI, '/api/recommend/v1.0/<corpus_name>')
#api.add_resource(ClickTrackingAPI, '/api/click/v1.0/<sourceid>/<recommendation_number>')

if __name__ == "__main__":
    app.run()
