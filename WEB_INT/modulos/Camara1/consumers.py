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
message_o='hola'
message_c='caja'
message_co='cola'

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
    global message_o,message_co
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
            message_co=(message['counts'])['person']
        #mues_datos(message_o,opcion)
    except IndexError:
        print("No hay personas haciendo cola en la caja.")





def inicio(broker,tiempo):
     #broker="192.168.0.104"
    client0=mqtt.Client('WEB1')
    client0.on_message=on_message
    client0.on_connect=on_connect
    client0.on_log=on_log
    print("Connecting to broker: ",broker)
    client0.connect(broker)
    client0.loop_start()
    client0.subscribe("/merakimv/Q2FV-NX7G-MNB2/raw_detections")
    time.sleep(tiempo)
    client0.loop_stop()
    #client.disconnect()
    return message_o

def inicio2(broker,tiempo):
    client=mqtt.Client('CAJA')
    client.on_message=on_message1
    client.on_connect=on_connect
    client.on_log=on_log
    client.connect(broker)
    client.loop_start()
    client.subscribe("/merakimv/Q2FV-NX7G-MNB2/779685685488517301")
    time.sleep(tiempo)
    client.loop_stop()
    return message_c
    ######################################3

def inicio3(broker,tiempo):
    client2=mqtt.Client('COLA')
    client2.on_message=on_message
    client2.on_log=on_log
    client2.connect(broker)
    client2.loop_start()
    client2.subscribe("/merakimv/Q2FV-NX7G-MNB2/779685685488517302")
    time.sleep(tiempo)
    client2.loop_stop()
    return message_co

url = "https://api.meraki.com/api/v1/devices/Q2FV-NX7G-MNB2/camera/generateSnapshot"
payload = '''{ "fullframe": true }'''

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": "0d7a8b4276fb04606fe0659a37e52dbba345e805"
}
res='https://spn21.meraki.com/stream/jpeg/snapshot/1f54bfb972cb2352VHY2RkZjZhYjRjZTdjNjJiODMzYTBiYmRlNTYzZTkwZDQ1OGNjYTgzZmE3MTMyM2VlYTZhMzQ4NDA2NmFjNDQ5NXxjwk5I0u5EHPymoMzcGuf2_aIZ6o2TvgWtmjCfZeDWxlKsCTWgK8zSiP48WEG3T-kKUMecboiNbmxBBYcy4-tow6N3cJPDYM6EI7vosIRqy7l8CSjgujA_i-wZ0WuIDxrJSJp7G4Ivgh19cpJ5hOAYHMRX4voBlz-e8EPIe6dk70_sgS2w9BvM9O-ZmLK73vM88yz8t9bSsneZKLNIiYI'
def snapshot():
    #import requests
    global headers
    global payload
    global res
    response = requests.request('POST', url, headers=headers, data = payload)
    res=(response.json())['url']
    print('URL', type(res),res)
    return res
old = ' '

class WSConsumer(WebsocketConsumer):
     def connect(self):
         global old
         url='https://spn21.meraki.com/stream/jpeg/snapshot/1f54bfb972cb2352VHY2RkZjZhYjRjZTdjNjJiODMzYTBiYmRlNTYzZTkwZDQ1OGNjYTgzZmE3MTMyM2VlYTZhMzQ4NDA2NmFjNDQ5NXxjwk5I0u5EHPymoMzcGuf2_aIZ6o2TvgWtmjCfZeDWxlKsCTWgK8zSiP48WEG3T-kKUMecboiNbmxBBYcy4-tow6N3cJPDYM6EI7vosIRqy7l8CSjgujA_i-wZ0WuIDxrJSJp7G4Ivgh19cpJ5hOAYHMRX4voBlz-e8EPIe6dk70_sgS2w9BvM9O-ZmLK73vM88yz8t9bSsneZKLNIiYI'
         self.accept()
         broker = '192.168.0.105'
         for i in range(15):
            cadena= inicio(broker,1)
            cadena_caja = inicio2(broker,1)
            cadena_cola = inicio3(broker,1)
            #print("La caja: ", cadena_caja, "La cola: ",cadena_cola)
            if cadena!=old:
                url=snapshot()
            print("recibí: ",cadena)
            self.send(json.dumps({'message':cadena,'url':url,'caja':cadena_caja,'cola':cadena_cola}))
            #self.send(json.dumps({'url':url}))
            old=cadena
            





