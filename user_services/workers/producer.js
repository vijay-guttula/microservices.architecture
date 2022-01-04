var amqp = require('amqplib/callback_api');
let channel;
const CONN_URL =
  'amqps://vfovnnoi:nx0D9NyMn_Zk7TRe1JdWytJe5K_xCsSG@puffin.rmq2.cloudamqp.com/vfovnnoi';

amqp.connect(CONN_URL, function (error0, connection) {
  if (error0) {
    throw error0;
  }
  connection.createChannel(function (error1, ch) {
    if (error1) {
      throw error1;
    }
    channel = ch;
  });
});

const publish = async (data) => {
  channel.sendToQueue(
    'user_service_content',
    Buffer.from(JSON.stringify(data))
  );
};

process.on('exit', (code) => {
  channel.close();
  console.log(`Closing rabbitmq channel`);
});

module.exports = publish;
