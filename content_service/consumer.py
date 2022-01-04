import pika

params = pika.URLParameters('amqps://vfovnnoi:nx0D9NyMn_Zk7TRe1JdWytJe5K_xCsSG@puffin.rmq2.cloudamqp.com/vfovnnoi')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
  print('Received in admin')
  print(body)

channel.basic_consume(queue='admin', on_message_callback=callback)

print('Started Consuming in content_service')

channel.start_consuming()

channel.close()