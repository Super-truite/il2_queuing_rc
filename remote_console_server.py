from remote_console import RemoteConsoleClient
import configparser
import time 
import pika
import codecs
import sys 

# connecting to rabbitmq
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
# declaring a queue
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

config = configparser.ConfigParser()
config.read('config.ini')
REMOTE_CONSOLE_IP =  config['DEFAULT']['REMOTE_CONSOLE_IP']
REMOTE_CONSOLE_PORT =  int(config['DEFAULT']['REMOTE_CONSOLE_PORT'])
LOGIN_REMOTE_CONSOLE =  config['DEFAULT']['LOGIN_REMOTE_CONSOLE']
PASSWORD_REMOTE_CONSOLE =  config['DEFAULT']['PASSWORD_REMOTE_CONSOLE']

# connecting to the remote console
r_con = RemoteConsoleClient(REMOTE_CONSOLE_IP, REMOTE_CONSOLE_PORT, LOGIN_REMOTE_CONSOLE, PASSWORD_REMOTE_CONSOLE)
while not r_con.connect():  # until connect
    time.sleep(4)

def on_request(ch, method, props, body):
    msg = body.decode()

    print(" Processing message: %s" % msg)
    r_con.send(msg)
    response = r_con.response_string 

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Ready, Awaiting RPC requests")
channel.start_consuming()






