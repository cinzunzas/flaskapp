from typing import List, Dict
from flask import Flask, make_response, request, jsonify
import mysql.connector, os, pprint
import json
from app.libs.crypto import Crypto
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+os.environ['DB_USER']+':'+os.environ['DB_USER_PWD']+'@'+os.environ['DB_HOST']+':'+os.environ['DB_PORT']+'/'+os.environ['DB_SCHEMA']
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app.models import *


@app.route('/')
def index() -> str:
    return json.dumps({'favorite_colors': favorite_colors()})


@app.route("/wea")
def retorno_wea():

    return jsonify([
        {'id': color.id, 'name': color.name, 'color': color.color}
        for color in favorite_colors.query.all()
    ])


@app.route("/cesar")
def retorno_cesar():
    wea = Crypto()
    return wea.cesar("César", " si funciona la wea")
    #headers = {"Content-Type": "application/json"}
    #response = make_response('Test worked!', 200)
    #response.headers['Content-Type'] = "application/json"
    #return response


if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')