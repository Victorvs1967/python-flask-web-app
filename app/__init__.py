from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import Connection


app = Flask(__name__)
CORS(app)

db = Connection('flask_mongo_db')

@app.route('/protected')
@jwt_required()
def protected():
  current_user = get_jwt_identity()
  return jsonify({ 'message': f'Hello, {current_user}. This route protected!' })

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

from users import *
from auth import *