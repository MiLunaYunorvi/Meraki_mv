#import requests
from requests.models import Response
from channels.generic.websocket import WebsocketConsumer
import time
import requests  
from time import sleep
#import requests_async as requests
#from modulos.Camaras.mqtt import *
#import Camaras.mqtt.mqtt_2
#from mqtt.mqtt_2 import inicio
#from mqtt.mqtt_2 import *
#from MV_SENSE.Meraki_mv.proceso import *
import json
import paho.mqtt.client as mqtt


# class WSConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#         for i in range(1000):
#             self.send(json.dumps({'message':randint(1,100)}))
#             sleep(1)

def on_connect(client, userdata, flags, rc):
      if rc==0:
          print("connected OK")
      else:
            print("Bad connection Returned code= ",rc)
      
def on_log(client,userdata,level,buf):
      print("log: ",buf)

opcion=''

def on_message1(client, userdata, message):
    global message_c
    global opcion
    #print(msg.topic+" "+str(msg.payload))
    #print(type(message.payload.decode("utf-8")))
    try:
        message = json.loads(message.payload.decode("utf-8"))
        print(message)
        if 'objects' in message:
            opcion=1
            n = len(message['objects'])
            message_c=n
        else:
            opcion=2
            message_c=(message['counts'])['person']
        #mues_datos(message_o,opcion)
    except IndexError:
        print("No hay personas haciendo cola en la caja.")

def on_message(client, userdata, message):
    global message_o
    global opcion
    #print(msg.topic+" "+str(msg.payload))
    #print(type(message.payload.decode("utf-8")))
    try:
        message = json.loads(message.payload.decode("utf-8"))
        print(message)
        if 'objects' in message:
            opcion=1
            n = len(message['objects'])
            message_o=n
        else:
            opcion=2
            message_o=(message['counts'])['person']
        #mues_datos(message_o,opcion)
    except IndexError:
        print("No hay personas haciendo cola en la caja.")


message_o='hola'
message_c='caja'
def inicio(broker,tiempo):
     #broker="192.168.0.104"
    client=mqtt.Client('WEB1')
    client.on_message=on_message
    client.on_connect=on_connect
    client.on_log=on_log
    print("Connecting to broker: ",broker)
    client.connect(broker)
    client.loop_start()
    client.subscribe("/merakimv/Q2FV-NX7G-MNB2/raw_detections")
    time.sleep(tiempo)
    client.loop_stop()
    #client.disconnect()
    return message_o

def inicio2(broker,tiempo):
    client=mqtt.Client('WEB1')
    client.on_message=on_message1
    client.on_connect=on_connect
    client.on_log=on_log
    client.connect(broker)
    client.loop_start()
    client.subscribe("/merakimv/Q2FV-NX7G-MNB2/779685685488517301")
    time.sleep(tiempo)
    client.loop_stop()
    return message_c

url = "https://api.meraki.com/api/v1/devices/Q2FV-NX7G-MNB2/camera/generateSnapshot"
payload = '''{ "fullframe": true }'''

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": "0d7a8b4276fb04606fe0659a37e52dbba345e805"
}

def snapshot():
    #import requests
    global headers
    global payload
    response = requests.request('POST', url, headers=headers, data = payload)
    res=(response.json())['url']
    print('URL', type(res),res)
    return res
old = ' '

class WSConsumer(WebsocketConsumer):
     def connect(self):
         global old
         url=''
         self.accept()
         broker = '192.168.0.105'
         for i in range(10):
            cadena= inicio(broker,2)
            cadena_caja= inicio2(broker,2)
            if cadena!=old:
                url=snapshot()
            print("recibí: ",cadena)
            self.send(json.dumps({'message':cadena,'url':url,'caja':cadena_caja}))
            #self.send(json.dumps({'url':url}))
            old=cadena
            





