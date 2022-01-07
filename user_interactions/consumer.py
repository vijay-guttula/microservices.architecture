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
  try:
    db.session.add(object)
    db.session.commit()
    print(operation)
  except Exception as e:
    print("Operation failed with message {}".format(e))

def deleteFromDb(operation, object):
  try:
    db.session.delete(object)
    db.session.commit()
    print(operation)
  except Exception as e:
    print("Operation failed with message {}".format(e))

def callback(ch, method, properties, body):
  try:
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
  
  except Exception as e:
    print("Operation failed with message {}".format(e))

channel.basic_consume(queue='user_interactions', on_message_callback=callback)


print('Started Consuming in user_interaction_service')

channel.start_consuming()

channel.close()