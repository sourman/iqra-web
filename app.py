#!/usr/bin/env python
from flask import Flask, jsonify, abort, request, render_template, redirect
from flask_seasurf import SeaSurf
from config import APIKEY
import os
import requests


app = Flask(__name__, static_folder="./static", template_folder="./templates")
app.config.from_object('config')
csrf = SeaSurf(app)
API_ROUTE = 'https://api.iqraapp.com'


@app.route('/static/<path:path>')
def sendStatic(path):
    return send_from_directory('static', path)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/app', methods=['GET'])
def webapp():
    return render_template('app.html')


@app.route('/download', methods=['GET'])
def download():
    return redirect(
        "https://play.google.com/store/apps/details?id=com.mmmoussa.iqra",
        code=302
    )


@app.route('/search', methods=['POST'])
def getSearchResult():
    if not request.json:
        abort(400)
    reqJSON = request.json
    reqJSON['apikey'] = APIKEY
    res = requests.post(API_ROUTE + '/api/v3.0/search', json=reqJSON)
    return jsonify(res.json())


@app.errorhandler(400)
def badRequest(error):
    return render_template('error.html')


@app.errorhandler(404)
def notFound(error):
    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)