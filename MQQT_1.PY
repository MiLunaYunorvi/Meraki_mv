import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/merakimv/Q2FV-NX7G-MNB2/raw_detections")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    #print(msg.topic+" "+str(msg.payload))
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

client = mqtt.Client()
#client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.104", 1883, 5)
client.subscribe("/merakimv/Q2FV-NX7G-MNB2/raw_detections")

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
