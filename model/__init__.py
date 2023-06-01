from uuid import uuid1
from werkzeug.security import generate_password_hash


class User:
  def __init__(self, username, password, email, firstname, lastName):
    self._id = str(uuid1().hex)
    self.username = username
    self.password = generate_password_hash(password)
    self.email = email
    self.firstName = firstname
    self.lastName = lastName
