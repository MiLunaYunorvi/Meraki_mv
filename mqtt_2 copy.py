import paho.mqtt.client as mqtt
import time
import json
from proceso import cont,muestra

def on_connect(client, userdata, flags, rc):
      if rc==0:
          print("connected OK")
      else:
            print("Bad connection Returned code= ",rc)
      
def on_log(client,userdata,level,buf):
      print("log: ",buf)

def on_message(client, userdata, message):
    #print(msg.topic+" "+str(msg.payload))
    #print(type(message.payload.decode("utf-8")))
    message_n=(json.loads(message.payload.decode("utf-8")))['objects']  
    print(message_n)
    oid=message_n[0]['oid']
    print("El ID de la persona es: ",oid)
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    print("__________________________")
    n=cont(message_n)
    muestra(n,message_n)

broker="192.168.0.104"
client=mqtt.Client("PYTHON1")
client.on_message=on_message
client.on_connect=on_connect
client.on_log=on_log

print("Connecting to broker: ",broker)

client.connect(broker)
client.loop_start()
client.subscribe("/merakimv/Q2FV-NX7G-MNB2/raw_detections")

time.sleep(20)
client.loop_stop()
client.disconnect()