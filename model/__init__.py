from werkzeug.security import generate_password_hash


class User:
  def __init__(self, id, username, password, email, firstname, lastName):
    self._id = id
    self.username = username
    self.password = generate_password_hash(password)
    self.email = email
    self.firstName = firstname
    self.lastName = lastName
