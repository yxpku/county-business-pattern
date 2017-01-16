from flask import Flask
from flask import render_template
import json
import sqlite3
from model import Model
import sys, os


app = Flask(__name__)

con = sqlite3.connect('cbp.db')

model = Model(con)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get/<string:item>')
def get(item):
    if item == 'year':
        years = [str(y) for y in model.get_years()]
        return '[' + ','.join(years) + ']'
    elif item == 'industry':
        return json.dumps(model.get_industries())
    else:
        return '{}'


@app.route('/data/<string:naics>/<int:year>/<string:expr>')
def data(naics, year, expr):
    try:
        if expr == 'avgap':
            expr = 'ap * 1.0 / emp'
        return json.dumps(model.get_data(naics, year, expr))
    except:
        return '{}'

if __name__ == '__main__':
    app.run(debug=False)
