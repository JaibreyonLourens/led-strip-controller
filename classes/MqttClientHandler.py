from classes.MessageHandler import MessageHandler
from classes.LedController import *
import paho.mqtt.client as mqtt
import random
import json
import time
websocketPort = 8884
subTopic = "ledCommands"
messageHandler = MessageHandler()

credentialsData = None

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def readCredentials():
    credentialsFile = open("credentials.json")
    credentialsdata = json.load(credentialsFile)

    credentialsFile.close()
    return credentialsdata


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    messageHandler.messageHandler(client ,msg.topic, msg.payload.decode())


def connect_mqtt() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client("", None, mqtt.MQTTv5)
    client.on_connect = on_connect
    credentialsData = readCredentials()
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    client.username_pw_set(credentialsData["username"], credentialsData["password"])

    client.on_message = on_message

    
    client.connect(credentialsData['broker'], credentialsData['port'])

    return client


def subscribe(client: mqtt):
    client.subscribe(subTopic)

def publish(client, topic, msg):
    result = client.publish(topic, msg)
    # result is 0(success) or 1(fail) 
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
      


