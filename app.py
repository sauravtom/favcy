from flask import Flask, request, jsonify, redirect, render_template
import json
import random
import requests
import os
import pyrebase

app = Flask(__name__, static_url_path="/static")
url = 'http://184.107.80.44:8080/examples/servlets/getanalytics?limit=300'
url_arr = []
marker = 0
first = True

config = {
    "apiKey": "AIzaSyB74UF2Phk6AiBUsOthxQYKCFDj39Nphzk",
    "authDomain": "tempimage-5b31b.firebaseapp.com",
    "databaseURL": "https://tempimage-5b31b.firebaseio.com",
    "storageBucket": "tempimage-5b31b.appspot.com",
}

firebase = pyrebase.initialize_app(config)


@app.route('/')
def index():
    response = requests.get(url).json()
    global url_arr, marker, first
    if first:
        url_arr = [i['article']['url'] for i in response['response']]
        first = False
    return render_template('Dashboard.html', next_news=url_arr[marker], news_id=marker)


@app.route('/tokenize/<id>/<tag_list>', methods=['POST', 'GET'])
def tokenize(id, tag_list):
    global marker, url_arr
    # Push url and tags to Firebase
    data = {
        "news_url" : url_arr[marker],
        "tags" : tag_list[:-1]
    }
    db = firebase.database()
    db.push(data)

    marker += 1
    return redirect('/')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
