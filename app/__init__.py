from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import Connection


app = Flask(__name__)
CORS(app)

db = Connection('flask_mongo_db')

items = []

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

@app.route('/signup')
def signup():
  username = request.form['username']
  password = request.form['password']
  email = request.form['email']
  firstName = request.form['firstName']
  lastName = request.form['lastName']
  user = User(username, password, email, firstName, lastName)

  return render_template('signup.html')

from users import *
from auth import *