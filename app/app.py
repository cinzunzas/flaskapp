from typing import List, Dict
from flask import Flask, make_response, request, jsonify
import mysql.connector
import json

app = Flask(__name__)


def favorite_colors() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'knights'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM favorite_colors')
    results = [{name: color} for (name, color) in cursor]
    cursor.close()
    connection.close()

    return results


@app.route('/')
def index() -> str:
    return json.dumps({'favorite_colors': favorite_colors()})


@app.route("/wea")
def retorno_wea():
    return "Hello World2!"

@app.route("/cesar")
def retorno_cesar():
    headers = {"Content-Type": "application/json"}
    response = make_response('Test worked!', 200)
    response.headers['Content-Type'] = "application/json"
    return response


if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')