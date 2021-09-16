import paho.mqtt.client as mqtt
import time
import json
from proceso import muestra_general,muestra_caja

message_o='hola'

def on_connect(client, userdata, flags, rc):
      if rc==0:
          print("connected OK")
      else:
            print("Bad connection Returned code= ",rc)
      
def on_log(client,userdata,level,buf):
      print("log: ",buf)

opcion=''

def on_message(client, userdata, message):
    global message_o
    global opcion
    #print(msg.topic+" "+str(msg.payload))
    #print(type(message.payload.decode("utf-8")))
    try:
        message_o = json.loads(message.payload.decode("utf-8"))
        print(message_o)
        
        if 'objects' in message_o:
            opcion=1
        else:
            opcion=2
        mues_datos(message_o,opcion)
    except IndexError:
        print("No hay personas haciendo cola en la caja.")
    
    
def mues_datos(mensaje_cod,n):
    if n==1:
        message_n=mensaje_cod['objects']  
        print(message_n)
        oid=message_n[0]['oid']
        print("__________________________")
        
    if n==2:
        message_n=mensaje_cod['counts']

    pro_message(message_n,n)

def pro_message(mensaje,n):
    if n==1:
        muestra_general(mensaje)
        print("::__________________________::")
    if n==2:
        muestra_caja(mensaje)

def inicio(broker,tiempo):
     #broker="192.168.0.104"
    client=mqtt.Client('WEB1')
    client.on_message=on_message
    client.on_connect=on_connect
    client.on_log=on_log
    print("Connecting to broker: ",broker)
    client.connect(broker)
    client.loop_start()
    client.subscribe("/merakimv/Q2FV-NX7G-MNB2/779685685488517302")
    time.sleep(tiempo)
    client.loop_stop()
    client.disconnect()
    return message_o


def general(broker,tiempo):
    client=mqtt.Client('WEB1')
    client.on_message=on_message
    client.connect(broker)
    client.loop_start()
    client.subscribe("/merakimv/Q2FV-NX7G-MNB2/779685685488517302")