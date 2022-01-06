from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from dataclasses import dataclass
from producer import publish


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/user_interactions'

CORS(app)



db = SQLAlchemy(app)

@dataclass
class Books(db.Model):
  __tablename__ = 'books'
  book_id: int
  
  book_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
  UniqueConstraint('book_id', name='books_unique')

@dataclass
class Users(db.Model):
  __tablename__ = 'users'
  user_id: str
  email_id: str
  
  user_id = db.Column(db.String(200), primary_key=True)
  email_id = db.Column(db.String(200))
  
  UniqueConstraint('user_id','email_id', name='users_user_id_unique')

@dataclass  
class LikesReads(db.Model):
  __tablename__ = 'likes_reads'
  like_read_id: int
  user_id: str
  book_id: int
  like: bool
  read: bool
  
  like_read_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.String(200), db.ForeignKey('users.user_id',ondelete='CASCADE'))
  book_id = db.Column(db.Integer, db.ForeignKey('books.book_id',ondelete='CASCADE'))
  like = db.Column(db.Boolean, default=False)
  read = db.Column(db.Boolean, default=False)  
  
  UniqueConstraint('user_id', 'book_id', name='user_book_unique')

@app.route('/api/v1/users')
def users():
  return jsonify(Users.get.all())

@app.route('/api/v1/books')
def books():
  return jsonify(Books.get.all())

@app.route('/api/v1/book', methods=['POST'])
def like():
  request_data = request.get_json()
  user_id = request_data['user_id']
  book_id = request_data['book_id']
  operation = request_data['operation']
  
  likeread = LikesReads.query.filter_by(user_id=user_id, book_id=book_id).first()
  
  print(likeread)
  
  if likeread:
    if operation == 'like':
      likeread.like = True
    else:
      likeread.read = True
    
  else:
    if operation == 'like':
      likeread = LikesReads(user_id=user_id, book_id=book_id, like=True)
    else:
      likeread = LikesReads(user_id=user_id, book_id=book_id, read=True)
    db.session.add(likeread)
    
  db.session.commit()
    
  return jsonify({
    'message':'success',
  }) 
  
  


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')