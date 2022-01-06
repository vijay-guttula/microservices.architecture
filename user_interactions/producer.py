import pika, json

params = pika.URLParameters('amqps://vfovnnoi:nx0D9NyMn_Zk7TRe1JdWytJe5K_xCsSG@puffin.rmq2.cloudamqp.com/vfovnnoi')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(routing_key, body):
  channel.basic_publish(exchange='', routing_key=routing_key, body=json.dumps(body))



