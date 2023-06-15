from app import app, db
from flask import render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import check_password_hash

from model import User


# secret string generated with code: node -e "console.log(require('crypto').randomBytes(256).toString('base64'));"
app.config['SECRET_KEY'] = 'Vgy/agSz7ABlTJKjD6uzWStfaPWYXDeruhipj7CxfEpy0enf8h9S6zdmoHV0ADYJdl+Az9biF6VFpSGRI/CK25a697F+j/QvB6PTBH7IckunkaOlU0X/QJXt7S2Qt5szKA7ssj6fjnOPqBSBMx1bBciBEVoMrmqkaL+tbKb0aK1en19FBfRPphYq9EJVSLpoKphXNQSOeLaTnkb20EBqtcG6fk1z7JuXICKsSi/OXT4BPcBYNkFXU6m4jM11Id50QWUgKIJrEGxPlTGX3kBkceO4ZMPd5Z4MDQZ9q0eYT03wkP7dPiUkkDd3B0FSCJjgVXUR0JcXb9+V7nCxOkAbGA=='
jwt = JWTManager(app)

def authenticate(username, password):
    user = db.user.find_one({ 'username': username })
    if user:
      if user.get('username') == username and check_password_hash(user.get('password'), password):
        return user

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    user = authenticate(username, password)
    if user:
      token = create_access_token(identity=username)
      return jsonify({ 'token': token })
    return jsonify({ 'error': 'Invalid credentials' }), 401
  elif request.method =='GET':
    return render_template('login.html', title='Login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
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
    return render_template('signup.html', title='Sign Up')
