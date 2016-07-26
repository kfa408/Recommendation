#!/usr/bin/env python

import os
from flask import Flask, json, jsonify, render_template, redirect, request
from flask_restful import Resource, Api, abort, reqparse

import lsirec
import scraper


app = Flask(__name__)
api = Api(app)


@app.route('/')
def enterurl():
    return render_template('enterurl.html')


@app.route('/', methods = ['POST'])
def show_rec():

    inputurl = request.form['inputurl']

    resultdata = lsirec.lsirecommend(inputurl)

    return render_template('sitelist.html', resultdata = resultdata)


class recommendAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url',
                                   type=str,
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
        except parser.URLRetrievalError:
            abort(415)
        except parser.DocumentParsingError:
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
    app.run(debug = True)
