from flask_jwt_extended import jwt_required
from app import app, db
from flask import request

from model import User


@app.get('/users')
def get_users():
  users = db.user.find({})
  return {  'data': list(users) }, 200

@app.get('/users/<user_id>')
@jwt_required()
def get_user(user_id):
  user = db.user.find_one({ '_id': user_id })

  if not user:
    return { 'message': 'User not found...' }, 404
  return { 'data': user }, 200

@app.delete('/users/<user_id>')
@jwt_required()
def delete_user(user_id):
  result = db.user.delete_one({ '_id': user_id })

  if not result.deleted_count:
    return { 'message': 'Failed to delete...' }, 500
  return {  'message': 'Delete success...' }, 200

@app.put('/users/<user_id>')
@jwt_required()
def update_user(user_id):
  content = {'$set': dict(request.json)}
  result = db.user.update_one({ '_id': user_id }, content)

  if not result.matched_count:
    return { 'message': 'Failed to update: user not found...' }, 404
  elif not result.modified_count:
    return { 'message': 'Failed to update: no changes applied...' }
  return { 'message': 'Update success...' }, 200
