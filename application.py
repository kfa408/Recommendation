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

    return render_template('sitelist1.html', resultdata = resultdata)



if __name__ == "__main__":
    app.run()
