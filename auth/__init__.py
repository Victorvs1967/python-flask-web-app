from app import app, db
from flask import render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import check_password_hash

from model import User


app.config['SECRET_KEY'] = 'secret_key'

jwt = JWTManager(app)

def authenticate(username, password):
    user = db.user.find_one({ 'username': username })
    if user:
      if user.get('username') == username and check_password_hash(user.get('password'), password):
        return user

@app.route('/login', methods=['GET', 'POST'])
def login():
  # username = request.json.get('username')
  # password = request.json.get('password')

  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    user = authenticate(username, password)
    if user:
      token = create_access_token(identity=username)
      return jsonify({ 'token': token })
    return jsonify({ 'error': 'Invalid credentials' }), 401
  elif request.method =='GET':
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  # content = dict(request.json)
  # username = content.get('username')
  # password = content.get('password')
  # email = content.get('email')
  # firstName = content.get('firstName')
  # lastName = content.get('lastName')

  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    firstName = request.form['firstName']
    lastName = request.form['lastName']

    user = User(username, password, email, firstName, lastName)

    if db.user.find_one({ 'username': user.username }):
      return { 'message': 'Username alredy exist..' }, 500
    elif db.user.find_one({ 'email': user.email }):
      return { 'message': 'Email alredy exist..' }, 500

    result = db.user.insert_one(user.__dict__)

    if not result.inserted_id:
      return {'message': 'Failed to add user...'}, 500
    return {
      'message': 'Success',
      'data': { '_id': result.inserted_id }
    }, 200
  elif request.method == 'GET':
    return render_template('signup.html')
