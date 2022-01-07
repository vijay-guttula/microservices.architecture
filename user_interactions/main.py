from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from dataclasses import dataclass
from producer import publish

# app initialization
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/user_interactions'

# CORS
CORS(app)

# db
db = SQLAlchemy(app)

# db models
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


# Routes
@app.route('/api/v1/users')
def users():
  try:
    users = Users.query.all()
    return jsonify({
    'status':'OK',
    'data':users
    })
  except Exception as e:
    print(e)
    abort(400, 'Error fetching users \n{}'.format(e))

@app.route('/api/v1/books')
def books():
  try:
    books = Books.query.all()
    return jsonify({
    'status':'OK',
    'data':books
    })
  except Exception as e:
    print(e)
    abort(400, 'Error fetching books \n{}'.format(e))

@app.route('/api/v1/book', methods=['POST'])
def like_read():
  try:
    request_data = request.get_json()
    user_id = request_data['user_id']
    book_id = request_data['book_id']
    operation = request_data['operation']
    
    likeread = LikesReads.query.filter_by(user_id=user_id,book_id=book_id).first()
    print(likeread)
    if likeread:
      if operation == 'like':
        if likeread.like == True:
          abort(400, "You already liked this book")
        likeread.like = True
      else:
        if likeread.read == True:
          abort(400, 'You already read this book')
        likeread.read = True
    else:
      if operation == 'like':
        likeread = LikesReads(user_id=user_id, book_id=book_id, like=True)
      else:
        likeread = LikesReads(user_id=user_id, book_id=book_id, read=True)
      db.session.add(likeread)
      
    db.session.commit()
    
    publish(routing_key='content_service',body={
      'operation':'book_liked' if operation == 'like' else 'book_read','like_read_id': likeread.like_read_id,
      'user_id':likeread.user_id,
      'book_id':likeread.book_id,
      'like':likeread.like,
      'read':likeread.read
      })
    
    return jsonify({
      'message':'success',
      'data':{
        'like_read_id': likeread.like_read_id,
        'user_id':likeread.user_id,
        'book_id':likeread.book_id,
        'like':likeread.like,
        'read':likeread.read
        }
      })
    
  except Exception as e:
    print(e)
    abort(400, 'Error processing this request \n{}'.format(e))

@app.route('/api/v1/books/interactions')
def like_reads_all():
  try:
    request_data = request.get_json()
    user_id = request_data['user_id']
    
    like_reads = LikesReads.query.filter_by(user_id=user_id).all()
    
    return jsonify({
      'status':'OK',
      'data':like_reads
      })
  except Exception as e:
    print(e)
    abort(400, 'Error Processing the request with message \n{}'.format(e))

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')