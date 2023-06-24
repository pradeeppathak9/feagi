from datetime import datetime
import pickle
import itertools
import logging
import zmq


class PubSub:
    def __init__(self):
        self.context = zmq.Context()

    def send(self, topic, message):
        print(f"Sent - {topic}, {message}")
        self.socket.send_multipart(
            [ topic.encode('utf-8'), pickle.dumps(message) ]
        )
            
    def receive(self):
        [topic, message] = self.socket.recv_multipart()
        topic = topic.decode('utf-8')
        message = pickle.loads(message)
        print(f"Receive - {topic}, {message}")
        return topic, message

    def terminate(self):
        self.socket.close()
        
    def destroy(self):
        self.context.destroy()
        
        
class Pub(PubSub):
    
    def __init__(self, address, bind=True):
        PubSub.__init__(self)
        print(f"Pub -- Add - {address}, Bind - {bind}")
        self.socket = self.context.socket(zmq.PUB)
        self.socket.setsockopt(zmq.SNDHWM, 0)
        self.socket.bind(address) if bind else self.socket.connect(address)


        
class Sub(PubSub):
    
    def __init__(self, address, bind=False, topic=''):
        PubSub.__init__(self)
        print(f"Sub -- Add - {address}, Bind - {bind}, Topic - {topic}")
        self.socket = self.context.socket(zmq.SUB)
        self.socket.setsockopt(zmq.SUBSCRIBE, topic.encode('utf-8'))
        # self.socket.setsockopt(zmq.CONFLATE, 1) # keeps only last message in the queue
        self.socket.bind(address) if bind else self.socket.connect(address)