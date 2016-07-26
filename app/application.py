#!/usr/bin/env python

import os
from flask import Flask, json, jsonify, render_template, redirect, request
from flask_restful import Resource, Api, abort, reqparse

from recommender.base import Recommender
# Import the recommendation engines here to register them
from recommender.speechrec import SpeechRec
import scraper
import random

app = Flask(__name__)
api = Api(app)


@app.route('/')
def enterurl():
    return render_template('enterurl.html')


@app.route('/', methods = ['POST'])
def show_rec():

    inputurl = request.form['inputurl']

    userecAPI = recommendAPI()
    userecAPI.reqparse.remove_argument('url')
    userecAPI.reqparse.add_argument('url', type = str, default = inputurl)
    print(userecAPI.reqparse.parse_args())

    resultdata = userecAPI.get('speech')
    print(resultdata)

    return render_template('sitelist1.html', resultdata = resultdata)


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
        return recommendation

api.add_resource(recommendAPI, '/api/recommend/v1.0/<corpus_name>')


if __name__ == "__main__":
    app.run()
