from flask import Flask, render_template
from flask_cors import CORS

from db import Connection


app = Flask(__name__)
CORS(app)

db = Connection('flask_mongo_db')

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

from users import *
from auth import *