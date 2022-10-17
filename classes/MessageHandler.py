import json
import paho.mqtt.client as mqtt
from classes.LedController import *

resultTopic = "ledResults"

def saveData(id,data):
    Led = {
        "id": id,
        "data": data
    }
    with open('saved_details.json', 'w') as outfile:
        json.dump(data, outfile)

def publisStatus(client, status, message):
    data = {
        "status": status,
        "message": message
    }
    client.publish(resultTopic, json.dumps(data))

class MessageHandler:
    def __init__(self, ):
        self.led = None
        self.ledIsInitialized = False

    def __del__(self):
        print("Destructor called, MessageHandler deleted.")

    @staticmethod
    def convertPayload(msgPayload):
        dataOut = json.loads(msgPayload)
        return dataOut
    
    def initLed(self, client, payload):
        try:
            self.led = ledController(pixels, 
            payload['red'], 
            payload['green'], 
            payload['blue'], 
            payload['pixel_count'])
            self.led.led_on()
            publisStatus(client, "success", "Led initialized")
            self.ledIsInitialized = True
        except:
            publisStatus(client, "error", "Led initialization failed")
    def toggleLed(self, client):
        try:
            self.led.toggle()
            publisStatus(client, "success", "Led toggled")
        except:
            publisStatus(client, "error", "Led is not Toggled")
    def changeColor(self, client, payload):
        try:
            self.led.change_color(payload['red'], payload['green'], payload['blue'])
            publisStatus(client, "success", "Led color changed")
        except:
            publisStatus(client, "error", "Did not change color")
    def changePixelCount(self, client, payload):
        try:
            self.led.change_pixel_count(payload['pixel_count'])
            publisStatus(client, "success", "Led pixel count changed")
        except:
            publisStatus(client, "error", "Did not change pixel count")

    def messageHandler(self,client, topic, payload):
        if topic == "ledCommands":
            data = self.convertPayload(payload)
            command = data["command"]
            commandPayload = data['payload']
            print(commandPayload)
            if (command == "initLed"):
                self.initLed(client, commandPayload)
            elif (command == "save"):
                saveData(commandPayload['id'], self.led.saveLedDetails())
            if(self.ledIsInitialized):
                if (command == "toggle"):
                  self.toggleLed(client)
                
                if (command == "changeColor"):
                    self.changeColor(client, commandPayload)
                if (command == "changePixelCount"):
                    self.changePixelCount(client, commandPayload)
            else:
                publisStatus(client, "error", "Initialize the led first")
                
                
