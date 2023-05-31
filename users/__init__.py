from flask_jwt_extended import jwt_required
from app import app, db
from flask import request
from uuid import uuid1

from model import User


@app.post('/users')
def add_user():
  _id = str(uuid1().hex)

  content = dict(request.json)

  user = User(_id, content.get('username'), content.get('password'), content.get('email'), content.get('firstName'), content.get('lastName'))
  result = db.user.insert_one(user.__dict__)

  if not result.inserted_id:
    return {'message': 'Failed to add user...'}, 500

  return {
    'message': 'Success',
    'data': {
      '_id': result.inserted_id
    }
  }, 200

@app.get('/users')
def get_users():
  users = db.user.find({})
  return {
    'data': list(users)
  }, 200

@app.get('/users/<user_id>')
@jwt_required()
def get_user(user_id):
  query = {
    '_id': user_id
  }
  user = db.user.find_one(query)

  if not user:
    return {
      'message': 'User not found...'
    }, 404

  return {
    'data': user
  }, 200

@app.delete('/users/<user_id>')
@jwt_required()
def delete_user(user_id):
  query = {
    '_id': user_id
  }
  result = db.user.delete_one(query)

  if not result.deleted_count:
    return {
      'message': 'Failed to delete...'
    }, 500

  return {
    'message': 'Delete success...'
  }, 200

@app.put('/users/<user_id>')
@jwt_required()
def update_user(user_id):
  query = {
    '_id': user_id
  }
  content = {'$set': dict(request.json)}
  result = db.user.update_one(query, content)
  if not result.matched_count:
    return {
      'message': 'Failed to update: user not found...'
    }, 404
  if not result.modified_count:
    return {
      'message': 'Failed to update: no changes applied...'
    }

  return {
    'message': 'Update success...'
  }, 200
