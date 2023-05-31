from flask import Flask, render_template, request
from db import Connection

from uuid import uuid1


app = Flask(__name__)
db = Connection('flask_mongo_db')

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')


@app.post('/user')
def add_user():
  _id = str(uuid1().hex)

  content = dict(request.json)
  content.update({'_id': _id})

  result = db.user.insert_one(content)
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

@app.get('/user/<user_id>')
def get_user(user_id):
  query = {
    'id': user_id
  }
  user = db.user.find_one(query)

  if not user:
    return {
      'message': 'User not found...'
    }, 404

  return {
    'data': user
  }, 200

@app.delete('/user/<user_id>')
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

@app.put('/user/<user_id>')
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

if __name__ == '__main__':
  app.run()