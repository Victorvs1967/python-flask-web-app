from app import app, db
from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import check_password_hash


app.config['SECRET_KEY'] = 'secret_key'

jwt = JWTManager(app)

def authenticate(username, password):
    user = db.user.find_one({ 'username': username })
    if user:
      if user.get('username') == username and check_password_hash(user.get('password'), password):
        return user

@app.post('/login')
def login():
  username = request.json.get('username')
  password = request.json.get('password')
  user = authenticate(username, password)
  if user:
    token = create_access_token(identity=username)
    return jsonify({ 'token': token })
  return jsonify({ 'error': 'Invalid credentials' }), 401
