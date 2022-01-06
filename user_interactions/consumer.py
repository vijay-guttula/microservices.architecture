import pika, json
from main import Books, Users, db

params = pika.URLParameters('amqps://vfovnnoi:nx0D9NyMn_Zk7TRe1JdWytJe5K_xCsSG@puffin.rmq2.cloudamqp.com/vfovnnoi')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='user_interactions')

def convertToJson(body):
  data = json.loads(body)
  return data

def addToDb(operation, object):
  db.session.add(object)
  db.session.commit()
  print(operation)

def deleteFromDb(operation, object):
  db.session.delete(object)
  db.session.commit()
  print(operation)

def callback(ch, method, properties, body):
  print('Received in user_interaction')
  data = convertToJson(body)
  print(data)
  
  if data['operation'] == 'user_created':
    user = Users(user_id=data['user_id'], email_id=data['email_id'])
    addToDb(data['operation'],user)
  
  elif data['operation'] == 'user_deleted':
    user = Users.query.get(data['user_id'])
    deleteFromDb(data['operation'],user)
  
  elif data['operation'] == 'book_created':
    book = Books(book_id=data['book_id'])
    addToDb(data['operation'],book)
  
  elif data['operation'] == 'book_deleted':
    book = Books.query.get(data['book_id'])
    deleteFromDb(data['operation'], book)
  

channel.basic_consume(queue='user_interactions', on_message_callback=callback)


print('Started Consuming in user_interaction_service')

channel.start_consuming()

channel.close()