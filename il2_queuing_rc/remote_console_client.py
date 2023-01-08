import pika
import uuid
import random

class RemoteConsoleRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', heartbeat=10)) 

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None
    
    def reset(self):
        '''
        initialize again the connection (in case of Streamlost error for instance)
        '''
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', heartbeat=10)) 

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='')
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, msg):
        print(" [x] Requesting %r" % msg)
        self.response = None
        self.corr_id = str(uuid.uuid4())
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key='rpc_queue',
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id,
                ),
                body=msg)
            self.connection.process_data_events(time_limit=None)
            print(" [.] Got %r" % self.response)
        except pika.exceptions.StreamLostError:
            print('connection closed... and restarted')
            self.reset()
            self.call(msg)

        return self.response

if __name__ == '__main__': 
    IL2RC_rpc = RemoteConsoleRpcClient()

    for i in range(500):
        msg = random.choice(["getplayerlist", "serverinput deactivate_ai", "serverstatus", "cutchatlog"])
        response = IL2RC_rpc.call(msg)
