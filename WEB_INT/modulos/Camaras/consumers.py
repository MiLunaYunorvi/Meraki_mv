from channels.generic.websocket import WebsocketConsumer
from random import randint
from time import sleep
import json

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        for i in range(1000):
            self.send(json.dumps({'message':randint(1,100)}))
            sleep(1)
