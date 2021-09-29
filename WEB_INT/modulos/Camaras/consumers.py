#import requests
from requests.models import Response
from channels.generic.websocket import WebsocketConsumer
from random import randint
import time
import requests  
from time import sleep
from statistics import mode
#import requests_async as requests
#from modulos.Camaras.mqtt import *
#import Camaras.mqtt.mqtt_2
#from mqtt.mqtt_2 import inicio
#from mqtt.mqtt_2 import *
#from MV_SENSE.Meraki_mv.proceso import *
import json
import paho.mqtt.client as mqtt

##########REQUEST INFO#################

url = "https://api.meraki.com/api/v1/devices/Q2FV-NX7G-MNB2/camera/generateSnapshot"
payload = '''{ "fullframe": true }'''
url2 = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/client-health"
payload2 = '''{ }'''

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": "0d7a8b4276fb04606fe0659a37e52dbba345e805"
}
headers2 = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Auth-Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI2MTIzZGEzMTdiM2FhOTA2ZWQwYjJiMzIiLCJhdXRoU291cmNlIjoiaW50ZXJuYWwiLCJ0ZW5hbnROYW1lIjoiVE5UMCIsInJvbGVzIjpbIjVlNWE0MzI2NzUxNjEyMDBjYzRhYzk2MyJdLCJ0ZW5hbnRJZCI6IjVlNWE0MzI1NzUxNjEyMDBjYzRhYzk1YyIsImV4cCI6MTYzMjA5ODI0NiwiaWF0IjoxNjMyMDk0NjQ2LCJqdGkiOiJjZDJmYzBjZi01ZjBlLTRiYWItYTg5Zi01ZGMwMzI1NDY1ZDEiLCJ1c2VybmFtZSI6ImRldm5ldHVzZXIifQ.GdMIGXunk1b_FMNENKDIRyqhagARP6562ZmkekrOcGt9zfScRoT3TCG4CMg0h0aI6-i0AUom1ErzokinhKF6e3SWhEBb93LNSFc31mBAb-ijfagmnJal3-E0WnD7zVHG62SlB77j9sXyIJeEcpvLTQh9XjqvgYHbDCUScRoOA4V5UhQx9mNzHKqSycoJb2fV7mudlhdQTdcnnwry0sJEyfn5-lrzbKpRKdbNHQVjFpRz-rIGgwLkDlTlL9tQoFX4yDLDiMm8kjXO73Z9L_SE6sfowYCEkzVoLsXdzdkrynzHs4E3BJomIAUWZcpAu18K7WKaimBBg4U6oFsfkrWDhA"
}
########################################
################### VARIABLES GLOBALES ################

opcion=''
message_o=0
message_c=0
message_co=0
nf=0

acumulado =[]
default={'caja':[],'cola':[]}

old = ' '

res='https://spn21.meraki.com/stream/jpeg/snapshot/1f54bfb972cb2352VHY2RkZjZhYjRjZTdjNjJiODMzYTBiYmRlNTYzZTkwZDQ1OGNjYTgzZmE3MTMyM2VlYTZhMzQ4NDA2NmFjNDQ5NXxjwk5I0u5EHPymoMzcGuf2_aIZ6o2TvgWtmjCfZeDWxlKsCTWgK8zSiP48WEG3T-kKUMecboiNbmxBBYcy4-tow6N3cJPDYM6EI7vosIRqy7l8CSjgujA_i-wZ0WuIDxrJSJp7G4Ivgh19cpJ5hOAYHMRX4voBlz-e8EPIe6dk70_sgS2w9BvM9O-ZmLK73vM88yz8t9bSsneZKLNIiYI'
#######################################################

#################### FUNCIONES MQTT ###################

def on_connect(client, userdata, flags, rc):
      if rc==0:
          print("connected OK")
      else:
            print("Bad connection Returned code= ",rc)
      
def on_log(client,userdata,level,buf):
      print("log: ",buf)


def on_message1(client, userdata, message):
    global message_c
    global opcion
    global acumulado
    #print(msg.topic+" "+str(msg.payload))
    #print(type(message.payload.decode("utf-8")))
    try:
        message = json.loads(message.payload.decode("utf-8"))
        print(message)
        if 'objects' in message:
            n = len(message['objects'])
            for i in range(n):
                if message['objects'][i]['confidence'] >= 90:
                    nf=nf+1
            acumulado.append(nf)
            message_c= mode(acumulado)
            print(acumulado,message_c)
        else:
            n=(message['counts'])['person']
            acumulado.append(n)
            message_c=mode(acumulado)
            print(acumulado,message_c)
        #mues_datos(message_o,opcion)
    except IndexError:
        print("No hay personas haciendo cola en la caja.")

def on_message(client, userdata, message):
    global message_o,message_co
    global opcion
    global acumulado
    nf=0
    #print(msg.topic+" "+str(msg.payload))
    #print(type(message.payload.decode("utf-8")))
    try:
        message = json.loads(message.payload.decode("utf-8"))
        print(message)
        if 'objects' in message:
            n = len(message['objects'])
            for i in range(n):
                if message['objects'][i]['confidence'] >= 90:
                    nf=nf+1
            acumulado.append(nf)
            message_o= mode(acumulado)
            print(acumulado,message_o)
        else:
            n=(message['counts'])['person']
            acumulado.append(n)
            message_o=mode(acumulado)
            print(acumulado,message_o)
        #mues_datos(message_o,opcion)
    except IndexError:
        print("No hay personas haciendo cola en la caja.")

############### SUSCRIPCIONES MQTT ##################
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

#################################################################
######################## FUNCIONES ##############################
def snapshot():
    #import requests
    global headers
    global payload
    global res
    response = requests.request('POST', url, headers=headers, data = payload)
    res=(response.json())['url']
    print('URL', type(res),res)
    return res

def snapshot_estatico(n,per):
    urls=['https://i.imgur.com/JYUczkz.png','https://i.imgur.com/IUSmr2b.png',
    'https://i.imgur.com/GEBB9Jw.png','https://i.imgur.com/uI8z9ta.png',
    'https://i.imgur.com/TbpSIlB.png','https://i.imgur.com/NS2Q8SQ.png',
    'https://i.imgur.com/OMY9eyb.png','https://i.imgur.com/x5jVz30.png',
    'https://i.imgur.com/JeNcY0Z.png']
    if per<9:
        res=urls[per-1]
    else:
        res = 'https://i.imgur.com/JeNcY0Z.png'
    return res

def bot(num):
    url_sna = snapshot()
    url_webex = "https://webexapis.com/v1/messages"
    payload = json.dumps({
    "roomId": "Y2lzY29zcGFyazovL3VzL1JPT00vOWQ4NmVlNzAtMWE3ZS0xMWVjLTliNzAtNTM1NjYyZTVkYzIz",
    "text": '¡¡Se excedió el número de personas en la CAJA {}. ENVIEN REFUERZOS!!'.format(num),
    "files": ["{}".format(url_sna)]
    })
    headers = {
    'Authorization': 'Bearer YTg4OTVmYjktNWFkZS00YzA4LWFkNWItMjE5YTJkZDM1MjNmY2ZjOTFlZGItYmE1_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f',
    'Content-Type': 'application/json'
    }
    requests.request("POST", url_webex, headers=headers, data=payload)

def bot_cam(num,per):
    url_sna = snapshot_estatico(1,per)
    url_webex = "https://webexapis.com/v1/messages"
    print(url_sna)
    payload = json.dumps({
    "roomId": "Y2lzY29zcGFyazovL3VzL1JPT00vOWQ4NmVlNzAtMWE3ZS0xMWVjLTliNzAtNTM1NjYyZTVkYzIz",
    "text": '¡¡Se excedió el número de personas en la CAJA {}. ENVIEN REFUERZOS!!'.format(num),
    "files": ["{}".format(url_sna)]
    })
    headers = {
    'Authorization': 'Bearer YTg4OTVmYjktNWFkZS00YzA4LWFkNWItMjE5YTJkZDM1MjNmY2ZjOTFlZGItYmE1_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f',
    'Content-Type': 'application/json'
    }
    requests.request("POST", url_webex, headers=headers, data=payload)

def alarmas(diccionario):
    print(diccionario)
    for i in range(len(diccionario['caja'])):
        if(diccionario['caja'][i] != 0):
            r = (diccionario['cola'][i])/(diccionario['caja'][i])
            if r >=5 and i<=1:
                bot(i+1)
            elif r>=5 and i>1:
                bot_cam(i+1,diccionario['cola'][i])

def estado_caja():
    #import requests
    global headers2
    global payload2
    response = requests.request('GET', url2, headers=headers2, data = payload2)
    print(response)
    estado=(((response.json())['response'])[0])['scoreDetail'][0]['clientCount']
    print('URL',estado)
    return estado

def estado_variable():
    global acumulado
    #------------cam1-----------------#
    broker = '192.168.0.107'
    acumulado=[]
    total_1 = int(inicio(broker,2))
    acumulado=[]
    caja_1 = int(inicio2(broker,1))
    cola_1= total_1 - caja_1
    cajae = 0
    colae= 0
    #_________________________________#
    global default
    default['caja'] = [caja_1,randint(0,1),0,randint(1,3),randint(2,3),randint(1,4)]
    default['cola'] = [cola_1,randint(0,4),randint(0,1),randint(5,10),8,randint(6,14)]
    return default

##################################################
################ WEBSOCKETS ######################           
class WSConsumer_camaras(WebsocketConsumer):
    def connect(self):
        global acumulado
        self.accept()
        l=[]
        for j in range(3):
            # for i in range(3):
            #     estado = estado_caja()
            #     l.append(int(estado))
            # if mode(l)<2:
            #     final = 'SI'
            # else:
            #     final='NO'
            cajas=estado_variable()
            acumulado=[]
            libre = cajas['cola'].index((min(cajas['cola']))) + 1
            llen = cajas['cola'].index((max(cajas['cola']))) + 1
            web_message=json.dumps({'caja1':cajas['caja'][0],
                                'caja2': cajas['caja'][1],
                                'caja3': cajas['caja'][2],
                                'caja4': cajas['caja'][3],
                                'caja5': cajas['caja'][4],
                                'caja6': cajas['caja'][5],
                                'cola1': cajas['cola'][0],
                                'cola2': cajas['cola'][1],
                                'cola3': cajas['cola'][2],
                                'cola4': cajas['cola'][3],
                                'cola5': cajas['cola'][4],
                                'cola6': cajas['cola'][5],
                                'min':libre,
                                'max':llen
                                })
            #print(web_message)
            self.send(web_message)
            alarmas(cajas)
            sleep(5)
        self.disconnect()
    def disconnect(self):
        print("Disconnecting")

class WSConsumer_cam1(WebsocketConsumer):
     def connect(self):
         global acumulado
         self.accept()
         broker = '192.168.0.107'
         url=snapshot()
         for i in range(4):
            acumulado=[]
            cadena= int(inicio(broker,1))
            acumulado=[]
            caja = int(inicio2(broker,1))
            cola = cadena - caja
            print("La caja: ", caja, "La cola: ",cola)
            if i>0 and (i % 2 )==0:
                url=snapshot()
                print(i)
            #print("recibí: ",cadena)
            self.send(json.dumps({'message':cadena,'url':url,'caja':caja,'cola':cola}))
            #self.send(json.dumps({'url':url}))
            sleep(5)
        
class WSConsumer_cams_pa(WebsocketConsumer):
     def connect(self):
         global acumulado
         caja=randint(1,2)
         cola=randint(1,5)
         global old
         url_s= snapshot_estatico(0,cola)
         self.accept()
         for i in range(12):
            acumulado=[]
            caja=randint(1,2)
            acumulado=[]
            cola=randint(1,5)
            total=cola+caja
            if i>0  and (i % 4 )==0:
                url_s=snapshot_estatico(0,cola)
                print(i,url_s)
            #print("recibí: ",cadena)
            self.send(json.dumps({'message':total,'url':url_s,'caja':caja,'cola':cola}))
            #self.send(json.dumps({'url':url}))
            sleep(3)

class WSConsumer_cams_im(WebsocketConsumer):
     def connect(self):
         global old
         url= '/static/img/caja2.jpg'
         self.accept()
         for i in range(17):
            caja=randint(1,3)
            cola=randint(9,14)
            total=cola+caja
            if i>0 and (i % 8 )==0:
                url=snapshot_estatico(0,cola)
                print(i)
            #print("recibí: ",cadena)
            self.send(json.dumps({'message':total,'url':url,'caja':caja,'cola':cola}))
            #self.send(json.dumps({'url':url}))
            sleep(3)
            

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        for i in range(5):
            self.send(json.dumps({'message':randint(1,100)}))
            sleep(3)
        self.disconnect()
    def disconnect(self):
        print("Disconnecting")



