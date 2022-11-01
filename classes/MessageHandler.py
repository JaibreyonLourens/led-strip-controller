import json
import paho.mqtt.client as mqtt
from classes.LedController import *

resultTopic = "ledResults"


def saveData(id, data):
    Led = {
        "id": id,
        "data": data
    }

    with open('saved_details.json', 'w') as outfile:
        json.dump(Led, outfile)

def readData():
    with open('saved_details.json') as json_file:
        data = json.load(json_file)
        return data

def loadData(self):
    data = readData()
    self.led = ledController(data["data"]["red"], data["data"]["green"], data["data"]["blue"], data["data"]["isOn"], data["data"]["pixel_count"]) 
    sendLedState(self.client, self.led)
    publishStatus(self.client, "success", "Led details loaded", "loadData")


def sendLedState(client, led):
    data = {
        "ledState": {
            "id": led.id,
            "red": led.red,
            "green": led.green,
            "blue": led.blue,
            "isOn": led.isOn,
            "pixel_count": led.pixel_count
        }
    }
    client.publish(resultTopic, json.dumps(data))


def publishStatus(client, status, message, command):
    data = {
        "status": status,
        "command": command,
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
        try:
            dataOut = json.loads(msgPayload)
        except:
            dataOut = None

        return dataOut

    def initLed(self, client, payload, command):
        try:
            self.led = ledController(pixels,
                                     payload['id'],
                                     payload['red'],
                                     payload['green'],
                                     payload['blue'],
                                     payload['pixel_count'],
                                     payload['isOn'],)
            self.led.led_on()
            publishStatus(client, "success", "Led initialized", command)
            self.ledIsInitialized = True
        except:
            publishStatus(client, "error",
                          "Led initialization failed", command)

    def toggleLed(self, client, command):
        try:
            self.led.toggle()
            publishStatus(client, "success", "Led toggled", command)
        except:
            publishStatus(client, "error", "Led is not Toggled", command)

    def changeColor(self, client, payload, command):
        try:
            self.led.change_color(
                payload['red'], payload['green'], payload['blue'])
            publishStatus(client, "success", "Led color changed", command)
        except:
            publishStatus(client, "error", "Did not change color", command)

    def changePixelCount(self, client, payload, command):
        try:
            self.led.change_pixel_count(payload['pixel_count'])
            publishStatus(client, "success",
                          "Led pixel count changed", command)
        except:
            publishStatus(client, "error",
                          "Did not change pixel count", command)

    def messageHandler(self, client, topic, payload):
        if topic == "ledCommands":
            data = self.convertPayload(payload)
            if data != None:
                command = data["command"]
                commandPayload = data['payload']
                print(commandPayload)
                if (command == "initLed"):
                    self.initLed(client, commandPayload, command)
                elif (command == "save"):
                    saveData(commandPayload['id'], self.led.saveLedDetails())
                elif (command == "load"):
                    loadData(self)
                if (self.ledIsInitialized):
                    if (command == "toggle"):
                        self.toggleLed(client, command)

                    if (command == "changeColor"):
                        self.changeColor(client, commandPayload, command)
                    if (command == "changePixelCount"):
                        self.changePixelCount(client, commandPayload, command)
                    if (command == "getLedState"):
                        sendLedState(client, self.led)
                else:
                    publishStatus(client, "error",
                                  "Initialize the led first", command)
