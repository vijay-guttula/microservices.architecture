import pika, json
from django.conf import settings
import django
from content_service.settings import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()

# import app models
from books.models import *
from books.serializers import *

params = pika.URLParameters('amqps://vfovnnoi:nx0D9NyMn_Zk7TRe1JdWytJe5K_xCsSG@puffin.rmq2.cloudamqp.com/vfovnnoi')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='content_service')

def convertToJson(body):
  data = json.loads(body)
  return data
  

def callback(ch, method, properties, body):
  print('Received in content service')
  data = convertToJson(body)
  print(data)
  operation = data['operation']
  user_data = {
      'user_id': data['user_id'],
      'email_id': data['email_id']
    }
  if  operation == 'user_created':
    user_serializer = UsersSerializer(data=user_data)
    user_serializer.is_valid(raise_exception=True)
    user_serializer.save()
  
  elif operation == 'user_deleted':
    user = UsersModel.objects.get(user_id=data['user_id'])
    user.delete()
  
  elif operation == 'book_liked':
    pass
  
  elif operation == 'book_read':
    pass

# channels
channel.basic_consume(queue='content_service', on_message_callback=callback)

print('Started Consuming in content_service')

channel.start_consuming()

channel.close()