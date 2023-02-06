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
    details = open("saved_details.json")
    data = json.load(details)
    details.close()
    return data


def initData(self, data):
    # print data
    print("data" + str(data['id']))
    self.led = ledController(
        pixels, data["id"], data["red"], data["green"], data["blue"], data["isOn"], data["pixel_count"])
    print("Led initialized")


def loadData(self):
    data = readData()
    initData(self, data)
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


def publishStatus(client, status, message, command, payload):
    data = {
        "status": status,
        "command": command,
        "message": message,
        "payload": payload
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
           
            print("Led initialized")
            self.led = ledController(pixels,
                                    payload['id'],
                                    payload['red'],
                                    payload['green'],
                                    payload['blue'],
                                    payload['pixel_count'],
                                    payload['isOn'],
                                    rainbow=False)
            self.led.led_on()
            publishStatus(client, "success", "Led initialized", command, {"isOn": self.led.isOn})
            self.ledIsInitialized = True
        except Exception as exception:
            #print error
            print(exception)
            publishStatus(client, "error",
                          "Led initialization failed", command, {})

    def toggleLed(self, client, command):
        try:
            self.led.toggle()
            publishStatus(client, "success", "Led toggled", command, {})
        except:
            publishStatus(client, "error", "Led is not Toggled", command, {})

    def changeColor(self, client, payload, command):
        try:
            self.led.change_color(
                payload['red'], payload['green'], payload['blue'])
            publishStatus(client, "success", "Led color changed", command, {
                            "red": payload['red'], "green": payload['green'], "blue": payload['blue']})
        except:
            publishStatus(client, "error", "Did not change color", command, {})

    def changePixelCount(self, client, payload, command):
        try:
            self.led.change_pixel_count(payload['pixel_count'])
            publishStatus(client, "success",
                          "Led pixel count changed", command, {})
        except:
            publishStatus(client, "error",
                          "Did not change pixel count", command, {})

    def rainbow(self, client, command):
        try:
            self.led.rainbow = True
            self.led.rainbow_cycle()
            publishStatus(client, "success", "Led rainbow", command, {})
        except Exception as exception:
            print(exception)
            publishStatus(client, "error", "Did not change color", command, {})
    
    def rainbowOff(self, client, command):
        try:
            self.led.rainbow = False
            self.led.led_on()
            publishStatus(client, "success", "Led rainbow off", command, {})
        except Exception as exception:
            print(exception)
            publishStatus(client, "error", "Did not change color", command, {})
            

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
                    if (command == "rainbow"):
                        self.rainbow(client, command)
                    if (command == "rainbowOff"):
                        self.rainbowOff(client, command)
                else:
                    publishStatus(client, "error",
                                  "Initialize the led first", command, {})
